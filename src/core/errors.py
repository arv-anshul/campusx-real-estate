# --- --- Dataset Validation --- --- #
class DataValidationError(Exception):
    """Raise while validating user's uploads data."""


class ModelNotFoundError(Exception):
    """Raise while the model is not found or trained."""
