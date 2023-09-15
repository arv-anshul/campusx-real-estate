from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, TypeAlias

import dill
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.core import io
from src.core.errors import ModelNotFoundError
from src.database.schema_reader import SchemaReader
from src.ml import price_predictor
from src.typing import DatasetType, PropertyAlias

ModelType: TypeAlias = Literal["price_predictor"]


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    schema: SchemaReader
    prop_type: PropertyAlias
    _PROPERTY_TYPE: str
    _ord_cols: dict[str, list[str | int]] | None
    _ohe_cols: list[str] | None

    @abstractmethod
    def st_form(cls) -> None:
        ...

    @abstractmethod
    def extract_this_property(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    def dump_dataframe(self, df: pd.DataFrame) -> None:
        """For now store the data at `data/processed/props` directory."""
        fp = Path("data/processed/props") / f"{self.prop_type}.csv"

        if fp.exists():
            old_df = pd.read_csv(fp)
            df = pd.concat([old_df, df], axis="index").drop_duplicates(["PROP_ID"])

        df.to_csv(fp, index=False)

    def get_model_path(self, dataset_type: DatasetType, model_type: ModelType) -> Path:
        return Path("models/") / dataset_type / model_type / f"{self.prop_type}.dill"

    def get_dataset_path(self, dataset_type: DatasetType) -> Path:
        return Path("data") / dataset_type / f"{self.prop_type}.csv"

    def train_price_predictor(self, dataset_type: DatasetType) -> None:
        """
        Train a model to predict PRICE using `RandomForestRegressor`.

        **Note:** Use `np.expm1` function after prediction to get the real price because
        the PRICE feature is right skewed.
        """
        df = io.read_csv(self.get_dataset_path(dataset_type))
        X = df.drop(columns=["PRICE"])
        y = np.log1p(df["PRICE"])

        # Create pipeline and train the model
        preprocessor = price_predictor.get_preprocessor(self._ord_cols, self._ohe_cols)
        pipeline = price_predictor.create_pipeline(preprocessor=preprocessor)
        pipeline.fit(X, y)

        # Store the trained model
        model_path = self.get_model_path(dataset_type, "price_predictor")
        with open(model_path, "wb") as f:
            dill.dump(pipeline, f)

    def predict_price(self, df: pd.DataFrame, dataset_type: DatasetType) -> float:
        # Load the stored model
        model_path = self.get_model_path(dataset_type, "price_predictor")

        try:
            with open(model_path, "rb") as f:
                pipeline: Pipeline = dill.load(f)
        except FileNotFoundError:
            raise ModelNotFoundError(
                f"Price predictor model not found. Please try to train for `{self.prop_type}`."
            )

        pred_price = np.expm1(pipeline.predict(df))
        return pred_price[0]  # type: ignore
