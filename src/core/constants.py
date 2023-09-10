""" Contains the project constants. """
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
