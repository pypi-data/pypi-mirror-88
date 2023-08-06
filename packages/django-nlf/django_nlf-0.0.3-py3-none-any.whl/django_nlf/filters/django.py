from typing import Any, Union

from django.db import models
from django.db.models.constants import LOOKUP_SEP

from django_nlf.conf import nlf_settings
from django_nlf.types import Lookup
from django_nlf.utils import coerce_bool

from .base import NLFilterBase


class DjangoNLFilter(NLFilterBase):
    lookups: dict = {
        Lookup.EQUALS: "iexact",
        Lookup.CONTAINS: "icontains",
        Lookup.REGEX: "iregex",
        Lookup.IN: "in",
        Lookup.GT: "gt",
        Lookup.GTE: "gte",
        Lookup.LT: "lt",
        Lookup.LTE: "lte",
    }
    path_sep: str = nlf_settings.PATH_SEPARATOR
    empty_val: str = nlf_settings.EMPTY_VALUE
    # field_shortcuts = {}

    def __init__(self, request=None, view=None):
        super().__init__()
        self.request = request
        self.view = view

        self.distinct = False
        self.model = None
        self.opts = None

        self.annotations = {}

    def follow_field_path(self, opts, path):
        """Resolves the field path on the model to get a Field instance. If any many to many
        relationships are found, the distinct flag is set to `True`.

        :param type opts: .
        :param type path: .
        :return: .
        :rtype: type
        """
        field = opts.get_field(path[0])

        if hasattr(field, "get_path_info"):
            # This field is a relation, update opts to follow the relation
            path_info = field.get_path_info()

            if any(path.m2m for path in path_info):
                self.distinct = True

            opts = path_info[-1].to_opts
            return self.follow_field_path(opts, path[1:])

        return field

    def normalize_field_function(self, value: dict) -> str:
        """Normalizes the output of field functions. Only one annotation is accepted, and its key
        is used as field name.

        :param dict value: A dictionary describing the annotation.
        :return: The key of the dictionary.
        :rtype: str
        :raises ValueError: Multiple annotations are returned.

        """
        annotation, *other = value.items()
        if other:
            raise ValueError("Multiple annotations returned!")
        self.annotations.update(**value)
        field_name, _ = annotation
        return field_name

    def normalize_value_function(self, value: Any) -> Any:
        """Normalizes the output of value functions. Currently a noop.

        :param Any value: .
        :return: .
        :rtype: Any
        """
        return value

    def normalize_expression_function(self, value):
        """Normalizes the output of expression functions. Annotations are collections and
        the filtering condition is returned.

        :param type value: .
        :return: .
        :rtype: type
        """
        annotations, condition = value
        self.annotations.update(**annotations)

        return condition

    def normalize_field_name(self, field_name: str) -> str:
        """Normalizes field name. By default it replaces PATH_SEPARATOR characters with Django's LOOKUP_SEP.

        :param str field_name: The name of the field.
        :return: Normalized field name.
        :rtype: str
        """
        # field_name = self.field_shortcuts.get(field_name, field_name)
        return field_name.replace(self.path_sep, LOOKUP_SEP)

    def normalize_value(
        self,
        field_name: Union[str, models.F, models.Aggregate, models.Subquery, models.Window],
        value: Any,
    ) -> Any:
        """Normalizes the value by checking if it is acceptable for the given field.
        If the field has choices, checks if the value is any of them
        and coerces boolean and datetime values if needed.

        :param Union[str, models.F, models.Aggregate, models.Subquery, models.Window] field_name: The field name.
        :param Any value: The filter value for the field.
        :return: Normalized value.
        :rtype: Any
        :raises ValueError: If the value is not matching any of the choices for a field.
        """
        if (
            field_name in self.annotations
            or value == self.empty_val
            or isinstance(value, (models.F, models.Aggregate, models.Subquery, models.Window))
        ):
            return value

        parts = field_name.split(LOOKUP_SEP)
        field = self.follow_field_path(self.opts, parts)

        if field.choices:
            for val, display in field.choices:
                if value.lower() == display.lower():
                    return val

            choices = ", ".join([display for _, display in field.choices])
            raise ValueError(f"Invalid {field_name}! Must be one of {choices}")

        if isinstance(field, (models.DateField, models.DateTimeField)):
            return self.coerce_datetime(value)

        if isinstance(field, (models.BooleanField, models.NullBooleanField)):
            return self.coerce_bool(value)

        return value

    def get_condition(self, field: str, lookup: Lookup, value: Any):
        """Constructs a :class:`Q object <>` based on parameters.

        :param str field: The field name.
        :param Lookup lookup: The lookup to be used.
        :param Any value: The filtering value.
        :return: The matching Q object, the filtering condition.
        :rtype: :class:`Q <>`
        """
        if isinstance(value, bool):
            lookup_str = None
        elif value == self.empty_val:
            lookup_str = "isnull"
            value = True
        else:
            lookup_str = self.lookups.get(lookup)

        orm_lookup = LOOKUP_SEP.join([field, lookup_str]) if lookup_str else field

        return models.Q(**{orm_lookup: value})

    def get_function_context(self):
        """Return the context for custom function calls.

        :return: context.
        :rtype: dict
        """
        return {
            "model": self.model,
            "request": self.request,
            "view": self.view,
        }

    def filter(self, queryset: models.QuerySet, value: str) -> models.QuerySet:
        """Filters the given query set according to the given filter expression.

        :param models.QuerySet queryset: Any queryset to be filtered.
        :param str value: The filter expression.
        :return: The filtered queryset.
        :rtype: models.QuerySet
        """
        self.model = queryset.model
        self.opts = queryset.model._meta  # pylint: disable=protected-access

        conditions = self.get_conditions(value)
        if self.annotations:
            queryset = queryset.annotate(**self.annotations)
        queryset = queryset.filter(conditions)

        if self.distinct:
            queryset = queryset.distinct()

        return queryset

    def coerce_bool(self, value: Any) -> bool:  # pylint: disable=no-self-use
        """Boolean coercion based on :func:`coerce_bool <django_nlf:django_nlf.utils.coerce_bool>`.
        Override this to customize.

        :param Any value: The value to coerce.
        :return: The coerced value.
        :rtype: bool
        """
        return coerce_bool(value)

    def coerce_datetime(self, value: Any) -> Any:  # pylint: disable=no-self-use
        """Datetime coercion, which is currently a noop. Override this to customize.

        :param Any value: The value to coerce.
        :return: The coerced value.
        :rtype: Any
        """
        return value
