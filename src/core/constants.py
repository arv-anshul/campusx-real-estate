""" Contains the project constants. """
from pathlib import Path

# --- --- Database Constants --- --- #
DATA_SCHEMA_PATH = Path("src/database/schema.json")

# --- --- Form Options Constants --- --- #
CITY_CSV = Path("data/form_options/CITY.csv")
LOCALITY_NAME_CSV = Path("data/form_options/LOCALITY_NAME.csv")

# --- --- DataCleaner --- --- #
LAKH = 1_00_000
TEN_LAC = 10_00_000
CRORE = 1_00_00_000

FACETS_PATH = Path("data/facets")
