import abc
import typing

from django_nlf.antlr import DjangoNLFLanguage
from django_nlf.functions import FunctionRegistry
from django_nlf.types import (
    CompositeExpression,
    CustomFunction,
    Expression,
    FunctionRole,
    Operation,
)


class NLFilterBase(abc.ABC):
    language_class = DjangoNLFLanguage
    function_factory = FunctionRegistry

    def get_conditions(self, expression: str):
        filter_tree = self.get_language().parse(expression)
        return self.build_conditions(filter_tree)

    def resolve_expression(self, expression: Expression):
        if isinstance(expression.field, CustomFunction):
            field_name = self.normalize_field_function(
                self.resolve_function(expression.field, FunctionRole.FIELD)
            )
        else:
            field_name = self.normalize_field_name(expression.field)

        if isinstance(expression.value, CustomFunction):
            value = self.normalize_value_function(
                self.resolve_function(expression.value, FunctionRole.VALUE, field_name=field_name)
            )
        else:
            value = self.normalize_value(field_name, expression.value)

        condition = self.get_condition(field_name, expression.lookup, value)

        return condition if not expression.exclude else ~condition

    def build_conditions(
        self, filter_tree: typing.Union[Expression, CompositeExpression, CustomFunction]
    ):
        if isinstance(filter_tree, Expression):
            return self.resolve_expression(filter_tree)

        if isinstance(filter_tree, CustomFunction):
            return self.normalize_expression_function(
                self.resolve_function(filter_tree, FunctionRole.EXPRESSION)
            )

        left = self.build_conditions(filter_tree.left)
        right = self.build_conditions(filter_tree.right)

        if filter_tree.operation == Operation.OR:
            return left | right
        return left & right

    def resolve_function(self, func: CustomFunction, role: FunctionRole, field_name: str = None):
        context = self.get_function_context()
        func.kwargs.update(context)

        fn = self.function_factory.get_function(func.name, role, context.get("model"))
        return fn(*func.args, **func.kwargs, field_name=field_name)

    def get_language(self):
        return self.language_class()

    @abc.abstractmethod
    def get_function_context(self):
        raise NotImplementedError(".get_function_context() must be overriden")

    @abc.abstractmethod
    def filter(self, queryset, value):
        raise NotImplementedError(".filter() must be overriden")

    @abc.abstractmethod
    def normalize_value(self, field_name, value):
        raise NotImplementedError(".normalize_value() must be overriden")

    @abc.abstractmethod
    def normalize_field_function(self, value):
        raise NotImplementedError(".normalize_field_function() must be overriden")

    @abc.abstractmethod
    def normalize_value_function(self, value):
        raise NotImplementedError(".normalize_value_function() must be overriden")

    @abc.abstractmethod
    def normalize_expression_function(self, value):
        raise NotImplementedError(".normalize_expression_function() must be overriden")

    @abc.abstractmethod
    def normalize_field_name(self, field_name):
        raise NotImplementedError(".normalize_field_name() must be overriden")

    @abc.abstractmethod
    def get_condition(self, field, lookup, value):
        raise NotImplementedError(".get_condition() must be overriden")
