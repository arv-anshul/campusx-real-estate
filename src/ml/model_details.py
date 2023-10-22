import json
from datetime import datetime

import numpy as np
from pydantic import BaseModel, Field, NaiveDatetime
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from streamlit.elements.lib.mutable_status_container import StatusContainer

from src.core import io
from src.core.errors import ModelNotFoundError
from src.property import _utils
from src.property import _utils as prop_utils
from src.typing import DatasetType, ModelType, PropertyAlias
from src.utils._json_encoding import _json_default


class ModelDetailsItem(BaseModel):
    class_name: str
    r2_score_mean: float
    r2_score_std: float
    mae: float
    created_at: NaiveDatetime = Field(default_factory=datetime.now)


class ModelDetailsJSON(BaseModel):
    res_apartment: list[ModelDetailsItem] = Field(default_factory=list)
    rent_apartment: list[ModelDetailsItem] = Field(default_factory=list)
    ind_floor: list[ModelDetailsItem] = Field(default_factory=list)
    rent_ind_floor: list[ModelDetailsItem] = Field(default_factory=list)
    ind_house: list[ModelDetailsItem] = Field(default_factory=list)
    res_land: list[ModelDetailsItem] = Field(default_factory=list)


class GetModelDetails:
    def __init__(
        self,
        *,
        property_type: PropertyAlias,
        dataset_type: DatasetType,
        model_type: ModelType,
    ) -> None:
        self.property_type: PropertyAlias = property_type
        self.dataset_type: DatasetType = dataset_type
        self.model_type: ModelType = model_type
        self.model_details_path = _utils.get_model_details_file_path(
            self.dataset_type, self.model_type
        )

    def load_details(self) -> ModelDetailsJSON:
        try:
            data = json.loads(self.model_details_path.read_text())
        except FileNotFoundError:
            return ModelDetailsJSON()

        return ModelDetailsJSON(**data)

    def dump_details(self, data: ModelDetailsJSON) -> None:
        with open(self.model_details_path, "w") as f:
            json.dump(data.model_dump(), f, indent=2, default=_json_default)

    def append_details(self, details: ModelDetailsItem) -> None:
        data = self.load_details()
        getattr(data, self.property_type).append(details)
        self.dump_details(data)

    def store_model_details(self, st_status: StatusContainer) -> None:
        df = io.read_csv(
            prop_utils.get_dataset_path(self.property_type, self.dataset_type)
        )
        X = df.drop(columns=["PRICE"])
        y = np.log1p(df["PRICE"])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        try:
            pipeline: Pipeline = io.dill_load(
                prop_utils.get_model_path(
                    self.property_type, self.dataset_type, self.model_type
                )
            )
        except FileNotFoundError:
            raise ModelNotFoundError(
                f"Model for {self.property_type} is not trained yet."
            )

        st_status.write("Calculating Cross Validation Score (R2 Score)...")
        scores = cross_val_score(
            estimator=pipeline, X=X_train, y=y_train, cv=5, scoring="r2"
        )

        try:
            st_status.write("Predicting `X_test` for more scoring metrics...")
            y_pred = np.expm1(pipeline.predict(X_test))
        except ValueError as e:  # When any/some predicted value become inf or NaN
            st_status.error(str(e), icon="🛑")
            st_status.update(
                label="Error while predicting `X_test`.", expanded=False, state="error"
            )
            y_pred = y_test

        st_status.write("Creating model scores details...")
        details = ModelDetailsItem(
            class_name=pipeline.named_steps["reg_model"].__class__.__name__,
            r2_score_mean=round(scores.mean(), 3),
            r2_score_std=round(scores.std(), 3),
            mae=round(float(mean_absolute_error(np.expm1(y_test), y_pred)), 3),
        )

        st_status.write("Storing model details...")
        self.append_details(details)
        st_status.write("Storing model details complete.")
