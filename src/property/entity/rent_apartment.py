import streamlit as st

from src.database.schema_reader import SchemaReader
from src.property.form_field import FormField

from .property_type import PropertyType


class RentApartment(PropertyType):
    schema = SchemaReader("rent_apartment")

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
