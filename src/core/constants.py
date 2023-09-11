""" Contains the project constants. """
from pathlib import Path

from src.property.entity import (
    IndFloor,
    IndHouse,
    PropertyType,
    RentApartment,
    RentIndFloor,
    ResApartment,
    ResLand,
)
from src.typing import PropertyAlias

ALL_PROPERTY: dict[PropertyAlias, PropertyType] = {
    "res_apartment": ResApartment(),
    "rent_apartment": RentApartment(),
    "ind_floor": IndFloor(),
    "rent_ind_floor": RentIndFloor(),
    "ind_house": IndHouse(),
    "res_land": ResLand(),
}

# --- --- Database Constants --- --- #
DATA_SCHEMA_PATH = Path("src/database/schema.json")

