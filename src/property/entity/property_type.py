from abc import ABC, abstractmethod


class PropertyType(ABC):
    """Abstract class for to for different property type in real estate."""

    @abstractmethod
    def st_form(cls) -> None:
        ...
