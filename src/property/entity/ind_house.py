import pandas as pd
import streamlit as st

from src.data.schema_reader import SchemaReader
from src.property import _utils
from src.property.form_field import FormField

from ..property_type import PropertyType


class IndHouse(PropertyType):
    schema = SchemaReader("ind_house")
    prop_type = "ind_house"
    _PROPERTY_TYPE = "independent house/villa"

    @staticmethod
    def st_form():
        FormField.AREA()
        FormField.FACING()

        l, r = st.columns(2)
        FormField.AGE(pos=l)
        FormField.FURNISH(pos=r)

    def extract_this_property(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.query("PROPERTY_TYPE==@self._PROPERTY_TYPE").reset_index(drop=True)
        df = df.drop(
            index=df[
                df["PROP_ID"].isin(
                    _utils.query_for_rental_property(df, "PRICE<6_00_000")["PROP_ID"]
                )
            ].index
        ).reset_index(drop=True)

        return df
