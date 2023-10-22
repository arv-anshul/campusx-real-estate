from typing import Literal

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import FunctionTransformer, Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from src.core import io
from src.core.errors import ModelNotFoundError
from src.property import _utils as prop_utils
from src.property.property_type import PropertyType
from src.typing import DatasetType


class PricePredictor:
    model_type: Literal["price_predictor"] = "price_predictor"

    def __init__(self, obj: PropertyType, dataset_type: DatasetType) -> None:
        self.prop = obj
        self.dataset_type: DatasetType = dataset_type

    @staticmethod
    def preprocessor(
        ord_cols: dict[str, list[str | int]], ohe_cols: list[str]
    ) -> ColumnTransformer:
        transformers = [
            (
                "log1p_area",
                FunctionTransformer(
                    func=np.log1p, inverse_func=np.expm1, validate=True
                ),
                ["AREA"],
            ),
            (
                "ord",
                OrdinalEncoder(categories=list(ord_cols.values())),
                list(ord_cols.keys()),
            ),
            (
                "ohe",
                # FIXME: Improve the OneHotEncoding.
                # TODO: Remove `handle_unknown` parameter and do something else.
                OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
                ohe_cols,
            ),
        ]

        preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
        return preprocessor

    @staticmethod
    def pipeline(preprocessor: ColumnTransformer | None) -> Pipeline:
        pipe = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("reg_model", RandomForestRegressor(n_estimators=500)),
            ]
        )
        if preprocessor:
            pipe.steps.insert(0, ("preprocessor", preprocessor))
        return pipe

    def train(self) -> None:
        """
        Train a model to predict PRICE using `RandomForestRegressor`.

        **Note:** Use `np.expm1` function after prediction to get the real price because
        the PRICE feature is right skewed.
        """
        df = io.read_csv(
            prop_utils.get_dataset_path(self.prop.prop_type, self.dataset_type)
        )
        X = df.drop(columns=["PRICE"])
        y = np.log1p(df["PRICE"])

        # Create pipeline and train the model
        preprocessor = self.preprocessor(
            self.prop._ord_cols, self.prop.schema.CAT_COLS["ohe_cols"]
        )
        pipeline = self.pipeline(preprocessor)
        pipeline.fit(X, y)

        # Store the trained model
        model_path = prop_utils.get_model_path(
            self.prop.prop_type, self.dataset_type, self.model_type
        )
        io.dill_dump(pipeline, model_path)

    def predict(self, df: pd.DataFrame) -> float:
        # Load the stored model
        model_path = prop_utils.get_model_path(
            self.prop.prop_type, self.dataset_type, self.model_type
        )

        try:
            pipeline: Pipeline = io.dill_load(model_path)
        except FileNotFoundError:
            raise ModelNotFoundError(
                f"Price predictor model not found. Please try to train for `{self.prop.prop_type}`."
            )

        pred_price = np.expm1(pipeline.predict(df))
        return pred_price[0]
