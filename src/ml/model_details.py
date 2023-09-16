import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, NaiveDatetime

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


def get_model_details_file_path(dataset_type: DatasetType, model_type: ModelType) -> Path:
    path = Path("models") / dataset_type / f"{model_type}.json"
    path.parent.mkdir(exist_ok=True)
    return path


def load_details(model_details_path: Path) -> ModelDetailsJSON:
    try:
        with open(model_details_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return ModelDetailsJSON()

    return ModelDetailsJSON(**data)


def dump_details(data: ModelDetailsJSON, model_details_path: Path) -> None:
    with open(model_details_path, "w") as f:
        json.dump(data.model_dump(), f, indent=2, default=_json_default)


def append_details(
    model_details_path: Path,
    prop_type: PropertyAlias,
    details: ModelDetailsItem,
) -> None:
    data = load_details(model_details_path)
    getattr(data, prop_type).append(details)
    dump_details(data, model_details_path)
