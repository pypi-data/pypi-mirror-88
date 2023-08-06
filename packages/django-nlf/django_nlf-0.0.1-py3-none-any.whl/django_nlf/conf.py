"""
Configuration module
"""
import warnings

try:
    from django.conf import settings as dj_settings
    from django.core.signals import setting_changed
except ImportError:
    dj_settings = object()
    setting_changed = None


DEFAULTS = {
    "QUERY_PARAM": "q",
    "PATH_SEPARATOR": ".",
    "EMPTY_VALUE": "EMPTY",
    "FALSE_VALUES": ("0", "f"),
}


DEPRECATED_SETTINGS = []


def deprecate(msg, level_modifier=0):
    warnings.warn(msg, DeprecationWarning, stacklevel=3 + level_modifier)


def is_callable(value):
    # check for callables, except types
    return callable(value) and not isinstance(value, type)


class Settings:
    def __getattr__(self, name):
        if name not in DEFAULTS:
            msg = "'%s' object has no attribute '%s'"
            raise AttributeError(msg % (self.__class__.__name__, name))

        value = self.get_setting(name)

        if is_callable(value):
            value = value()

        # Cache the result
        setattr(self, name, value)
        return value

    def get_setting(self, setting):
        django_setting = f"NLF_{setting}"

        if setting in DEPRECATED_SETTINGS and hasattr(dj_settings, django_setting):
            deprecate(f"The '{django_setting}' setting has been deprecated.")

        return getattr(dj_settings, django_setting, DEFAULTS[setting])

    def change_setting(self, setting, value, enter, **kwargs):
        if not setting.startswith("NLF_"):
            return
        setting = setting[4:]  # strip 'NLF_'

        # ensure a valid app setting is being overridden
        if setting not in DEFAULTS:
            return

        # if exiting, delete value to repopulate
        if enter:
            setattr(self, setting, value)
        else:
            delattr(self, setting)


nlf_settings = Settings()

if setting_changed is not None:
    setting_changed.connect(nlf_settings.change_setting)
