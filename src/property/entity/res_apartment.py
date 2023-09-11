import streamlit as st

from src.database.reader import SchemaReader
from src.property.form_field import FormField

from . import PropertyType


class ResApartment(PropertyType):
    schema = SchemaReader("res_apartment")

    @staticmethod
    def st_form():
        l, r = st.columns(2)
        FormField.CITY(pos=l)
        FormField.LOCALITY_NAME(pos=r)

        FormField.AREA()
        FormField.FACING()

        l, r = st.columns(2)
        FormField.AGE(pos=l)
        FormField.FURNISH(pos=r)

        l, m, r = st.columns(3)
        FormField.BEDROOM_NUM(pos=l)
        FormField.BALCONY_NUM(pos=m)
        FormField.FLOOR_NUM(pos=r)
