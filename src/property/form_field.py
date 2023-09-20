from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from . import _utils
from .form_options import form_options


class FormField:
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
            options=form_options.FACING,
            format_func=lambda x: x.title(),
            key="FACING",
        )

    @staticmethod
    def AGE(
        label: str = "Age of Property",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.AGE,
            format_func=lambda x: x.title(),
            key="AGE",
        )

    @staticmethod
    def FURNISH(
        label: str = "Furnishing Status",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.FURNISH,
            format_func=lambda x: x.title(),
            key="FURNISH",
        )

    @staticmethod
    def BEDROOM_NUM(
        label: str = "Select number of Bedroom",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.BEDROOM_NUM,
            key="BEDROOM_NUM",
            format_func=_utils.format_99_option,
        )

    @staticmethod
    def BALCONY_NUM(
        label: str = "Select number of Balcony",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.BALCONY_NUM,
            key="BALCONY_NUM",
            format_func=_utils.format_99_option,
        )

    @staticmethod
    def FLOOR_NUM(
        label: str = "Select Floor type",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.FLOOR_NUM,
            format_func=lambda x: x.title(),
            key="FLOOR_NUM",
        )

    @staticmethod
    def LUXURY_CATEGORY(
        label: str = "Select Luxury Category",
        pos: Optional[DeltaGenerator] = None,
    ):
        getattr(st if pos is None else pos, "selectbox")(
            label,
            options=form_options.LUXURY_CATEGORY.keys(),
            format_func=lambda x: form_options.LUXURY_CATEGORY[x],
            key="LUXURY_CATEGORY",
        )
