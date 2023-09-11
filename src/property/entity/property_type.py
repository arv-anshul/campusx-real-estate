from abc import ABC, abstractmethod

from src.database.schema_reader import SchemaReader


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    st_form_key: str
    schema: SchemaReader

    @abstractmethod
    def st_form(cls) -> None:
        ...
