import typing

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

from django_nlf.types import Expression, CompositeExpression

from .error_listener import DjangoNLFErrorListener
from .generated import DjangoNLFLexer, DjangoNLFParser
from .listener import DjangoNLFListener


class DjangoNLFLanguage:
    lexer_class = DjangoNLFLexer
    parser_class = DjangoNLFParser
    listener_class = DjangoNLFListener
    error_listener_class = DjangoNLFErrorListener

    def parse(self, filter_expr: str) -> typing.Union[Expression, CompositeExpression]:
        if not filter_expr:
            return []

        _input = InputStream(filter_expr)
        lexer = self.get_lexer(_input)
        stream = CommonTokenStream(lexer)
        parser = self.get_parser(stream)

        error_listener = self.get_error_listener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        tree = parser.parse()

        listener = self.get_listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.output[0]

    def get_error_listener(self) -> DjangoNLFErrorListener:
        return self.error_listener_class()

    def get_listener(self) -> DjangoNLFListener:
        return self.listener_class()

    def get_lexer(self, input_stream: InputStream) -> DjangoNLFLexer:
        return self.lexer_class(input_stream)

    def get_parser(self, token_stream: CommonTokenStream) -> DjangoNLFParser:
        return self.parser_class(token_stream)
