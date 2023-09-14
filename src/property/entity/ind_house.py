import streamlit as st

from src.database.schema_reader import SchemaReader
from src.property.form_field import FormField

from .property_type import PropertyType


class IndHouse(PropertyType):
    schema = SchemaReader("ind_house")

    @staticmethod
    def st_form():
        FormField.AREA()
        FormField.FACING()

        l, r = st.columns(2)
        FormField.AGE(pos=l)
        FormField.FURNISH(pos=r)
