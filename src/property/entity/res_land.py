import pandas as pd

from src.data.schema_reader import SchemaReader
from src.property.form_field import FormField

from ..property_type import PropertyType


class ResLand(PropertyType):
    schema = SchemaReader("res_land")
    prop_type = "res_land"
    _PROPERTY_TYPE = "residential land"

    @staticmethod
    def st_form():
        FormField.AREA()

    def extract_this_property(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.query("PROPERTY_TYPE==@self._PROPERTY_TYPE").reset_index(drop=True)

        return df
