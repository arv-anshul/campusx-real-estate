import pandas as pd
import streamlit as st

from src.database.schema_reader import SchemaReader
from src.property import _utils
from src.property.form_field import FormField

from ..property_type import PropertyType


class IndFloor(PropertyType):
    schema = SchemaReader("ind_floor")
    prop_type = "ind_floor"
    _PROPERTY_TYPE = "independent/builder floor"
    _ord_cols = {
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
    _ohe_cols = ["FACING", "LOCALITY_NAME"]

    @staticmethod
    def st_form():
        FormField.AREA()
        FormField.FACING()

        l, r = st.columns(2)
        FormField.AGE(pos=l)
        FormField.FURNISH(pos=r)

        l, m, r = st.columns(3)
        FormField.BEDROOM_NUM(pos=l)
        FormField.BALCONY_NUM(pos=m)
        FormField.FLOOR_NUM(pos=r)

        FormField.LUXURY_CATEGORY()

    def extract_this_property(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.query("PROPERTY_TYPE==@self._PROPERTY_TYPE").reset_index(drop=True)
        df = df.drop(
            index=df[
                df["PROP_ID"].isin(
                    _utils.query_for_rental_property(df, "PRICE<8_00_000")["PROP_ID"]
                )
            ].index
        ).reset_index(drop=True)

        df["PROP_ID"] = self.prop_type
        return df
