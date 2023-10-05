from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from src.database.schema_reader import SchemaReader
from src.property import _utils
from src.typing import DatasetType, ModelType, PropertyAlias


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    schema: SchemaReader
    prop_type: PropertyAlias
    _PROPERTY_TYPE: str

    @property
    def _ord_cols(self) -> dict[str, list[str | int]]:
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
        fp = self.get_dataset_path(dataset_type)

        if fp.exists() and extend:
            old_df = pd.read_csv(fp)
            df = pd.concat([old_df, df], axis="index").drop_duplicates(["PROP_ID"])

        df.to_csv(fp, index=False)

    def get_model_path(self, dataset_type: DatasetType, model_type: ModelType) -> Path:
        return Path("models/") / dataset_type / model_type / f"{self.prop_type}.dill"

    def get_dataset_path(self, dataset_type: DatasetType) -> Path:
        return Path("data") / dataset_type / f"{self.prop_type}.csv"
