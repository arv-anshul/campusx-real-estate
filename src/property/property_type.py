from abc import ABC, abstractmethod
from pathlib import Path
from warnings import filterwarnings, warn

import dill
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from src.core import io
from src.core.errors import ModelNotFoundError
from src.database.schema_reader import SchemaReader
from src.ml import model_details, price_predictor
from src.property import _utils
from src.typing import DatasetType, ModelType, PropertyAlias

filterwarnings("ignore", category=UserWarning)


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    schema: SchemaReader
    prop_type: PropertyAlias
    _PROPERTY_TYPE: str

    @property
    def _ord_cols(self) -> dict[str, list[str | int]] | None:
        return {
            k: v
            for k in self.schema.CAT_COLS["ord_cols"]
            for i, v in _utils.ORD_COLS_MAPPING.items()
            if i == k
        }

    @abstractmethod
    def st_form(cls) -> None:
        ...

    @abstractmethod
    def extract_this_property(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    def dump_dataframe(
        self,
        df: pd.DataFrame,
        dataset_type: DatasetType,
        extend: bool,
    ) -> None:
        """For now store the data at `data/processed/props` directory."""
        fp = Path("data") / dataset_type / f"{self.prop_type}.csv"

        if fp.exists() and extend:
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
        preprocessor = price_predictor.get_preprocessor(
            self._ord_cols, self.schema.CAT_COLS["ohe_cols"]
        )
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

    def store_model_details(self, dataset_type: DatasetType, model_type: ModelType) -> None:
        model_path = self.get_model_path(dataset_type, model_type)
        df = io.read_csv(self.get_dataset_path(dataset_type))

        X = df.drop(columns=["PRICE"])
        y = np.log1p(df["PRICE"])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # Load model
        try:
            with open(model_path, "rb") as f:
                pipeline: Pipeline = dill.load(f)
        except FileNotFoundError:
            raise ModelNotFoundError(f"Model for {self.prop_type} is not trained yet.")

        scores = cross_val_score(estimator=pipeline, X=X_train, y=y_train, cv=5, scoring="r2")

        try:
            y_pred = np.expm1(pipeline.predict(X_test))
        except ValueError as e:  # When any/some predicted value become inf or NaN
            warn(str(e), category=UserWarning)
            y_pred = y_test

        details = model_details.ModelDetailsItem(
            class_name=pipeline.named_steps["reg_model"].__class__.__name__,
            r2_score_mean=round(scores.mean(), 3),
            r2_score_std=round(scores.std(), 3),
            mae=round(float(mean_absolute_error(np.expm1(y_test), y_pred)), 3),
        )

        model_details_path = model_details.get_model_details_file_path(dataset_type, model_type)
        model_details.append_details(model_details_path, self.prop_type, details)
