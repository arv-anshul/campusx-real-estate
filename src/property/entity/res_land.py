import streamlit as st

from src.database.reader import SchemaReader
from src.property.form_field import FormField

from .property_type import PropertyType


class ResLand(PropertyType):
    schema = SchemaReader("res_land")

    @staticmethod
    def st_form():
        l, r = st.columns(2)
        FormField.CITY(pos=l)
        FormField.LOCALITY_NAME(pos=r)

        FormField.AREA()
