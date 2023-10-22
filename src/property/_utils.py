from pathlib import Path

import pandas as pd

from src.typing import DatasetType, ModelType, PropertyAlias

ORD_COLS_MAPPING = {
    "FURNISH": ["unfurnished", "semifurnished", "furnished"],
    "AGE": [
        "10+ year old property",
        "5-10 year old property",
        "1-5 year old property",
        "0-1 year old property",
        "under construction",
    ],
    "BEDROOM_NUM": [1, 2, 3, 4, 5, 99],
    "BALCONY_NUM": [0, 1, 2, 3, 4, 99],
    "FLOOR_NUM": ["low rise", "mid rise", "high rise"],
    "LUXURY_CATEGORY": [0, 1, 2],
}


def format_99_option(x: int):
    """Format the encode value `99` in **BEDROOM_NUM** and **BALCONY_NUM** feature."""
    if x == 99 or x == "99":
        return "More than Above"
    return x


def query_for_rental_property(
    df: pd.DataFrame,
    extra_query: str | None,
) -> pd.DataFrame:
    """Return the rental properties dataframe from the passed dataframe."""
    df = pd.concat(
        [
            df[df["DESCRIPTION"].str.contains(" rent ") & (df["PRICE"] < 20)],
            df.query(extra_query if extra_query else "PRICE<0"),
        ]
    ).drop_duplicates(ignore_index=True)
    return df


def get_model_details_file_path(
    dataset_type: DatasetType, model_type: ModelType
) -> Path:
    path = Path("models") / dataset_type / f"{model_type}.json"
    path.parent.mkdir(exist_ok=True)
    return path


def get_model_path(
    prop_type: PropertyAlias, dataset_type: DatasetType, model_type: ModelType
) -> Path:
    return Path("models") / dataset_type / model_type / f"{prop_type}.dill"


def get_dataset_path(prop_type: PropertyAlias, dataset_type: DatasetType) -> Path:
    return Path("data") / dataset_type / f"{prop_type}.csv"
