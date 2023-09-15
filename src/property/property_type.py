from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from src.database.schema_reader import SchemaReader
from src.typing import PropertyAlias


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    schema: SchemaReader
    prop_type: PropertyAlias
    _PROPERTY_TYPE: str

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
