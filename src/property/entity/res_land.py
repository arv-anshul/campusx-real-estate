from src.database.schema_reader import SchemaReader
from src.property.form_field import FormField

from .property_type import PropertyType


class ResLand(PropertyType):
    schema = SchemaReader("res_land")

    @staticmethod
    def st_form():
        FormField.AREA()
