import json
from typing import Self

from src.core.constants import DATA_SCHEMA_PATH
from src.typing import CAT_COLS_Key, PropertyAlias


class SchemaReader:
    _instance: dict[PropertyAlias, Self] = {}

    def __new__(cls, prop_type: PropertyAlias):
        if prop_type not in cls._instance:
            cls._instance[prop_type] = super(SchemaReader, cls).__new__(cls)
            cls._instance[prop_type]._load_schema(prop_type)
        return cls._instance[prop_type]

    def _load_schema(self, prop_type: PropertyAlias):
        with open(DATA_SCHEMA_PATH) as f:
            schema_dict = json.load(f)[prop_type]

        self.TARGET: str = schema_dict["target"]
        self.ALL_COLS: list[str] = schema_dict["all_cols"]
        self.NUM_COLS: list[str] = schema_dict["num_cols"]
        self.CAT_COLS: dict[CAT_COLS_Key, list[str]] = schema_dict["cat_cols"]
