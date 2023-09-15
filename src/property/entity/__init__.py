from ..property_type import PropertyType  # isort:skip
from src.typing import PropertyAlias

from .ind_floor import IndFloor
from .ind_house import IndHouse
from .rent_apartment import RentApartment
from .rent_ind_floor import RentIndFloor
from .res_apartment import ResApartment
from .res_land import ResLand

ALL_PROPERTY: dict[PropertyAlias, PropertyType] = {
    "res_apartment": ResApartment(),
    "rent_apartment": RentApartment(),
    "ind_floor": IndFloor(),
    "rent_ind_floor": RentIndFloor(),
    "ind_house": IndHouse(),
    "res_land": ResLand(),
}
