# Generated from DjangoNLF.g4 by ANTLR 4.8
from antlr4 import ParseTreeListener

from django_nlf.types import CompositeExpression, CustomFunction, Expression, Lookup, Operation
from .generated import DjangoNLFLexer, DjangoNLFParser


class Operator:
    def __init__(self, value: int, depth: int = 0):
        self.value = depth * 2 + value

    def is_and(self) -> bool:
        return self.value % 2 == 0

    def has_precedence(self, other: "Operator") -> bool:
        return self.is_and() and self.value == other.value - 1

    def to_operation(self) -> Operation:
        return Operation.AND if self.is_and() else Operation.OR

    def __repr__(self) -> str:
        operation = "AND" if self.is_and() else "OR"
        return f"<Operator.{operation}: {self.value}>"


def handle_precedence(operator, left, right):
    if isinstance(left, list) and operator.has_precedence(left[0]):
        previous_expression = left.pop()
        left.append([operator, previous_expression, right])
        return left

    return [operator, left, right]


def handle_operator(part):
    return part.to_operation() if isinstance(part, Operator) else part


def normalize_operators(output):
    normalized = [
        normalize_operators(el) if isinstance(el, list) else handle_operator(el) for el in output
    ]

    if len(normalized) == 3:
        return CompositeExpression(*normalized)

    return normalized


def sanitize_value(value, **kwargs):
    if value.type == DjangoNLFLexer.TEXT:
        return value.text

    if value.type == DjangoNLFLexer.QUOTED_TEXT or value.type == DjangoNLFLexer.REGULAR_EXPR:
        return value.text[1:-1]

    if value.type == DjangoNLFLexer.LISTING:
        return [val.strip('"') for val in value.text[1:-1].split(", ")]

    if value.type == DjangoNLFLexer.FUNCTION:
        open_paren_pos = value.text.index("(")
        function_name = value.text[:open_paren_pos]
        params_str = value.text[open_paren_pos + 1 : -1]
        args = [arg.strip(' "') for arg in params_str.split(",")] if params_str else []
        return CustomFunction(function_name, args, kwargs)

    # TODO: Proper error msg
    raise ValueError("Invalid value")


def negate(output):
    if isinstance(output, Operator):
        if output.is_and():
            output.value += 1
        else:
            output.value -= 1

        return output

    if isinstance(output, Expression):
        output.exclude = not output.exclude
        return output

    return [negate(part) for part in output]


#  pylint: disable=invalid-name
class DjangoNLFListener(ParseTreeListener):
    def __init__(self):
        super().__init__()
        self.output = []

        self.boolean_expr = None
        self.lookup = None
        self.operator = None
        self.exclude = False

        self.stage = []
        self.depth = 0

    def get_current_expression(self, ctx: DjangoNLFParser.ExpressionContext):
        if self.boolean_expr is not None:
            return self.boolean_expr

        if ctx.NOT() is not None:
            self.exclude = not self.exclude

        if (
            ctx.field is None
            and ctx.value is not None
            and ctx.value.type == DjangoNLFLexer.FUNCTION
        ):
            return sanitize_value(ctx.value, exclude=self.exclude)

        return Expression(
            lookup=self.lookup,
            field=sanitize_value(ctx.field),
            value=sanitize_value(ctx.value),
            exclude=self.exclude,
        )

    # # Enter a parse tree produced by DjangoNLFParser#operator.
    # def enterOperator(self, ctx: DjangoNLFParser.OperatorContext):
    #     pass

    # Exit a parse tree produced by DjangoNLFParser#operator.
    def exitOperator(self, ctx: DjangoNLFParser.OperatorContext):
        if ctx.AND() is not None:
            self.operator = Operator(0, self.depth)
        elif ctx.OR() is not None:
            self.operator = Operator(1, self.depth)

    # # Enter a parse tree produced by DjangoNLFParser#boolean_expr.
    # def enterBoolean_expr(self, ctx:DjangoNLFParser.Boolean_exprContext):
    #     pass

    # Exit a parse tree produced by DjangoNLFParser#boolean_expr.
    def exitBoolean_expr(self, ctx: DjangoNLFParser.Boolean_exprContext):
        value = ctx.EQUALS() is not None
        self.boolean_expr = Expression(
            lookup=Lookup.EQUALS,
            field=ctx.field.text,
            value=value,
            exclude=False,
        )

    # # Enter a parse tree produced by DjangoNLFParser#lookup.
    # def enterLookup(self, ctx: DjangoNLFParser.LookupContext):
    #     pass

    # Exit a parse tree produced by DjangoNLFParser#lookup.
    def exitLookup(self, ctx: DjangoNLFParser.LookupContext):
        if ctx.EQUALS() is not None:
            self.lookup = Lookup.EQUALS
        elif ctx.NEQUALS() is not None:
            self.lookup = Lookup.EQUALS
            self.exclude = True
        elif ctx.CONTAINS() is not None:
            self.lookup = Lookup.CONTAINS
        elif ctx.NCONTAINS() is not None:
            self.lookup = Lookup.CONTAINS
            self.exclude = True
        elif ctx.REGEX() is not None:
            self.lookup = Lookup.REGEX
        elif ctx.NREGEX() is not None:
            self.lookup = Lookup.REGEX
            self.exclude = True
        elif ctx.IN() is not None:
            self.lookup = Lookup.IN
        elif ctx.NIN() is not None:
            self.lookup = Lookup.IN
            self.exclude = True
        elif ctx.GT() is not None:
            self.lookup = Lookup.GT
        elif ctx.GTE() is not None:
            self.lookup = Lookup.GTE
        elif ctx.LT() is not None:
            self.lookup = Lookup.LT
        elif ctx.LTE() is not None:
            self.lookup = Lookup.LTE

    # # Enter a parse tree produced by DjangoNLFParser#expression.
    # def enterExpression(self, ctx: DjangoNLFParser.ExpressionContext):
    #     pass

    # Exit a parse tree produced by DjangoNLFParser#expression.
    def exitExpression(self, ctx: DjangoNLFParser.ExpressionContext):
        current_expression = self.get_current_expression(ctx)
        self.boolean_expr = None
        self.lookup = None
        self.exclude = False

        if self.operator is None:
            self.output.append(current_expression)
        else:
            previous_expression = self.output.pop()
            step = handle_precedence(self.operator, previous_expression, current_expression)
            self.output.append(step)
            self.operator = None

    # # Enter a parse tree produced by DjangoNLFParser#composite_expr.
    # def enterComposite_expr(self, ctx: DjangoNLFParser.Composite_exprContext):
    #     pass

    # # Exit a parse tree produced by DjangoNLFParser#composite_expr.
    # def exitComposite_expr(self, ctx: DjangoNLFParser.Composite_exprContext):
    #     pass

    # Enter a parse tree produced by DjangoNLFParser#nested_comp_expr.
    def enterNested_comp_expr(
        self, ctx: DjangoNLFParser.Nested_comp_exprContext
    ):  # pylint: disable=unused-argument
        self.stage.append((self.operator, self.output))
        self.depth += 1
        # let the listener parse the nested expression as if it were a new one
        self.output = []
        self.operator = None

    # Exit a parse tree produced by DjangoNLFParser#nested_comp_expr.
    def exitNested_comp_expr(
        self, ctx: DjangoNLFParser.Nested_comp_exprContext
    ):  # pylint: disable=unused-argument
        operator, left = self.stage.pop()
        if ctx.NOT() is not None:
            right = negate(self.output)
        else:
            right = self.output

        if operator:
            step = handle_precedence(operator, left[0], right[0])

            self.output = [step]

        self.depth -= 1

    # # Enter a parse tree produced by DjangoNLFParser#filter_exp.
    # def enterFilter_expr(self, ctx: DjangoNLFParser.Filter_exprContext):
    #     pass

    # Exit a parse tree produced by DjangoNLFParser#filter_exp.
    def exitFilter_expr(
        self, ctx: DjangoNLFParser.Filter_exprContext
    ):  # pylint: disable=unused-argument
        self.output = normalize_operators(self.output)

    # # Enter a parse tree produced by DjangoNLFParser#parse.
    # def enterParse(self, ctx: DjangoNLFParser.ParseContext):
    #     pass
    #
    # # Exit a parse tree produced by DjangoNLFParser#parse.
    # def exitParse(self, ctx: DjangoNLFParser.ParseContext):
    #     pass


del DjangoNLFParser
