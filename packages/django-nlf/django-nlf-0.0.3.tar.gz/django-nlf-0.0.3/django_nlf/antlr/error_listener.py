from antlr4.error.ErrorListener import ErrorListener

from .exceptions import LanguageSyntaxError


class DjangoNLFErrorListener(ErrorListener):
    def syntaxError(
        self, recognizer, offendingSymbol, line, column, msg, e
    ):  # pylint: disable=too-many-arguments
        symbol = offendingSymbol.text
        raise LanguageSyntaxError(f'"{symbol}" at line {line}:{column} {msg}')

    def reportAmbiguity(
        self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
    ):  # pylint: disable=too-many-arguments
        pass

    def reportAttemptingFullContext(
        self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
    ):  # pylint: disable=too-many-arguments
        pass

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):  # pylint: disable=too-many-arguments
        pass
