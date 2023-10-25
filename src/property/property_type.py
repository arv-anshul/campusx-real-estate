from abc import ABC, abstractmethod

import pandas as pd

from src.data.schema_reader import SchemaReader
from src.property import _utils
from src.property._utils import get_dataset_path
from src.typing import DatasetType, PropertyAlias


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
        fp = get_dataset_path(self.prop_type, dataset_type)

        if fp.exists() and extend:
            old_df = pd.read_csv(fp)
            df = pd.concat([old_df, df], axis="index").drop_duplicates(["PROP_ID"])

        df["PROP_ID"] = "https://99acres.com/" + df["PROP_ID"].str.upper()
        df.to_csv(fp, index=False)
