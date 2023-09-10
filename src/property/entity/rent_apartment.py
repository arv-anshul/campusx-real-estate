import streamlit as st

from src.database.reader import SchemaReader
from src.property.selectbox import SelectBox

from .property_type import PropertyType


class RentApartment(PropertyType):
    schema = SchemaReader("rent_apartment")

    @staticmethod
    def st_form():
        l, r = st.columns(2)
        SelectBox.CITY(pos=l)
        SelectBox.LOCALITY_NAME(pos=r)

        SelectBox.AREA()
        SelectBox.FACING()

        l, r = st.columns(2)
        SelectBox.AGE(pos=l)
        SelectBox.FURNISH(pos=r)

        l, m, r = st.columns(3)
        SelectBox.BEDROOM_NUM(pos=l)
        SelectBox.BALCONY_NUM(pos=m)
        SelectBox.FLOOR_NUM(pos=r)
