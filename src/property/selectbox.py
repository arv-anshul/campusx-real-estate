from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from . import utils
from .options import options


class SelectBox:
    @staticmethod
    def CITY(
        label: str = "Select City",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.CITY,
            disabled=True,
            key="CITY",
        )

    @staticmethod
    def LOCALITY_NAME(
        label: str = "Select Locality",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.LOCALITY_NAME,
            key="LOCALITY_NAME",
        )

    @staticmethod
    def AREA(
        label: str = "Area (in sq.ft.)",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "number_input")(
            label,
            min_value=1,
            format="%d",
            key="AREA",
        )

    @staticmethod
    def FACING(
        label: str = "Facing of the Property",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.FACING,
            key="FACING",
        )

    @staticmethod
    def AGE(
        label: str = "Age of Property",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.AGE,
            key="AGE",
        )

    @staticmethod
    def FURNISH(
        label: str = "Furnishing Status",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.FURNISH,
            key="FURNISH",
        )

    @staticmethod
    def BEDROOM_NUM(
        label: str = "Select number of Bedroom",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.BEDROOM_NUM,
            key="BEDROOM_NUM",
            format_func=utils.format_99_option,
        )

    @staticmethod
    def BALCONY_NUM(
        label: str = "Select number of Balcony",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.BALCONY_NUM,
            key="BALCONY_NUM",
            format_func=utils.format_99_option,
        )

    @staticmethod
    def FLOOR_NUM(
        label: str = "Select Floor type",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=options.FLOOR_NUM,
            key="FLOOR_NUM",
        )
