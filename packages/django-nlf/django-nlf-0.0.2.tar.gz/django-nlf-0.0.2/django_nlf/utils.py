"""
Utility functions
"""
from .conf import nlf_settings


def coerce_bool(value):
    """Coerces any value to a boolean. String values are checked for the first letter
    and matched against the `FALSE_VALUES` setting.
    """
    if isinstance(value, str):
        return value[0].lower() not in nlf_settings.FALSE_VALUES
    return value
