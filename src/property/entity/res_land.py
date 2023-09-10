import streamlit as st

from src.database.reader import SchemaReader
from src.property.selectbox import SelectBox

from .property_type import PropertyType


class ResLand(PropertyType):
    schema = SchemaReader("res_land")

    @staticmethod
    def st_form():
        l, r = st.columns(2)
        SelectBox.CITY(pos=l)
        SelectBox.LOCALITY_NAME(pos=r)

        SelectBox.AREA()
