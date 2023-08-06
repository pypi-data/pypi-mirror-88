# pylint: disable=invalid-name,missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code
# Generated from DjangoNLF.g4 by ANTLR 4.8
import sys
from io import StringIO
from typing import TextIO

from antlr4 import ATNDeserializer, DFA, Lexer, LexerATNSimulator, PredictionContextCache


def serializedATN():  # pylint: disable=too-many-statements
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33")
        buf.write("\u01b5\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write('\t\36\4\37\t\37\4 \t \4!\t!\4"\t"\4#\t#\4$\t$\4%\t%')
        buf.write("\4&\t&\4'\t'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\5\2\u0085\n\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\5\3\u0093\n\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\5\3\u00a2\n\3\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\5\5\u00b2\n\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6\u00ca\n\6\3\7\3\7")
        buf.write("\3\7\3\7\3\7\5\7\u00d1\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u00e0\n\7\3\b\3\b\3\b\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\13\3\f\3")
        buf.write("\f\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\20")
        buf.write("\3\20\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\5\24")
        buf.write("\u0108\n\24\3\24\3\24\5\24\u010c\n\24\3\24\3\24\3\25\3")
        buf.write("\25\3\25\3\25\6\25\u0114\n\25\r\25\16\25\u0115\3\26\3")
        buf.write("\26\3\26\7\26\u011b\n\26\f\26\16\26\u011e\13\26\3\26\3")
        buf.write("\26\3\27\3\27\5\27\u0124\n\27\3\30\5\30\u0127\n\30\3\30")
        buf.write("\7\30\u012a\n\30\f\30\16\30\u012d\13\30\3\30\3\30\3\30")
        buf.write("\7\30\u0132\n\30\f\30\16\30\u0135\13\30\3\30\3\30\6\30")
        buf.write("\u0139\n\30\r\30\16\30\u013a\3\30\7\30\u013e\n\30\f\30")
        buf.write("\16\30\u0141\13\30\3\30\5\30\u0144\n\30\3\31\3\31\3\31")
        buf.write("\3\31\6\31\u014a\n\31\r\31\16\31\u014b\3\31\3\31\5\31")
        buf.write("\u0150\n\31\3\31\3\31\7\31\u0154\n\31\f\31\16\31\u0157")
        buf.write("\13\31\3\31\3\31\7\31\u015b\n\31\f\31\16\31\u015e\13\31")
        buf.write("\3\31\3\31\3\32\3\32\3\32\3\32\7\32\u0166\n\32\f\32\16")
        buf.write("\32\u0169\13\32\3\32\3\32\3\33\3\33\3\34\3\34\3\35\3\35")
        buf.write('\3\36\3\36\3\37\3\37\3 \3 \3!\3!\3"\3"\3"\3"\3"\5')
        buf.write("\"\u0180\n\"\3#\3#\3$\3$\3%\3%\3&\3&\3'\3'\3(\3(\3)")
        buf.write("\3)\3*\3*\3+\3+\3,\3,\3-\3-\3.\3.\3/\3/\3\60\3\60\3\61")
        buf.write("\3\61\3\62\3\62\3\63\3\63\3\64\3\64\3\65\3\65\3\66\3\66")
        buf.write("\3\67\3\67\38\38\39\39\3:\3:\3;\3;\3<\3<\2\2=\3\3\5\4")
        buf.write("\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17")
        buf.write("\35\20\37\21!\22#\23%\24'\25)\26+\27-\30/\31\61\32\63")
        buf.write("\33\65\2\67\29\2;\2=\2?\2A\2C\2E\2G\2I\2K\2M\2O\2Q\2S")
        buf.write("\2U\2W\2Y\2[\2]\2_\2a\2c\2e\2g\2i\2k\2m\2o\2q\2s\2u\2")
        buf.write('w\2\3\2!\4\2\13\13""\3\2\61\61\3\2c|\3\2C\\\3\2\62;')
        buf.write("\4\2CCcc\4\2DDdd\4\2EEee\4\2FFff\4\2GGgg\4\2HHhh\4\2I")
        buf.write("Iii\4\2JJjj\4\2KKkk\4\2LLll\4\2MMmm\4\2NNnn\4\2OOoo\4")
        buf.write("\2PPpp\4\2QQqq\4\2RRrr\4\2SSss\4\2TTtt\4\2UUuu\4\2VVv")
        buf.write("v\4\2WWww\4\2XXxx\4\2YYyy\4\2ZZzz\4\2[[{{\4\2\\\\||\2")
        buf.write("\u01b7\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2")
        buf.write("\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2")
        buf.write("\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33")
        buf.write("\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2")
        buf.write("\2\2%\3\2\2\2\2'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2")
        buf.write("\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\3\u0084\3\2")
        buf.write("\2\2\5\u00a1\3\2\2\2\7\u00a3\3\2\2\2\t\u00ac\3\2\2\2\13")
        buf.write("\u00c9\3\2\2\2\r\u00df\3\2\2\2\17\u00e1\3\2\2\2\21\u00e4")
        buf.write("\3\2\2\2\23\u00eb\3\2\2\2\25\u00ed\3\2\2\2\27\u00f0\3")
        buf.write("\2\2\2\31\u00f2\3\2\2\2\33\u00f5\3\2\2\2\35\u00f9\3\2")
        buf.write("\2\2\37\u00fc\3\2\2\2!\u0100\3\2\2\2#\u0102\3\2\2\2%\u0104")
        buf.write("\3\2\2\2'\u010b\3\2\2\2)\u0113\3\2\2\2+\u0117\3\2\2\2")
        buf.write("-\u0123\3\2\2\2/\u0126\3\2\2\2\61\u0149\3\2\2\2\63\u0161")
        buf.write("\3\2\2\2\65\u016c\3\2\2\2\67\u016e\3\2\2\29\u0170\3\2")
        buf.write("\2\2;\u0172\3\2\2\2=\u0174\3\2\2\2?\u0176\3\2\2\2A\u0178")
        buf.write("\3\2\2\2C\u017f\3\2\2\2E\u0181\3\2\2\2G\u0183\3\2\2\2")
        buf.write("I\u0185\3\2\2\2K\u0187\3\2\2\2M\u0189\3\2\2\2O\u018b\3")
        buf.write("\2\2\2Q\u018d\3\2\2\2S\u018f\3\2\2\2U\u0191\3\2\2\2W\u0193")
        buf.write("\3\2\2\2Y\u0195\3\2\2\2[\u0197\3\2\2\2]\u0199\3\2\2\2")
        buf.write("_\u019b\3\2\2\2a\u019d\3\2\2\2c\u019f\3\2\2\2e\u01a1\3")
        buf.write("\2\2\2g\u01a3\3\2\2\2i\u01a5\3\2\2\2k\u01a7\3\2\2\2m\u01a9")
        buf.write("\3\2\2\2o\u01ab\3\2\2\2q\u01ad\3\2\2\2s\u01af\3\2\2\2")
        buf.write("u\u01b1\3\2\2\2w\u01b3\3\2\2\2yz\5U+\2z{\5i\65\2{\u0085")
        buf.write("\3\2\2\2|}\5M'\2}~\5e\63\2~\177\5m\67\2\177\u0080\5E")
        buf.write("#\2\u0080\u0081\5[.\2\u0081\u0082\5i\65\2\u0082\u0085")
        buf.write("\3\2\2\2\u0083\u0085\7?\2\2\u0084y\3\2\2\2\u0084|\3\2")
        buf.write("\2\2\u0084\u0083\3\2\2\2\u0085\4\3\2\2\2\u0086\u0087\5")
        buf.write('U+\2\u0087\u0088\5i\65\2\u0088\u0089\7"\2\2\u0089\u008a')
        buf.write("\5_\60\2\u008a\u008b\5a\61\2\u008b\u008c\5k\66\2\u008c")
        buf.write("\u00a2\3\2\2\2\u008d\u008e\5K&\2\u008e\u0092\5a\61\2\u008f")
        buf.write("\u0090\5M'\2\u0090\u0091\5i\65\2\u0091\u0093\3\2\2\2")
        buf.write("\u0092\u008f\3\2\2\2\u0092\u0093\3\2\2\2\u0093\u0094\3")
        buf.write('\2\2\2\u0094\u0095\7"\2\2\u0095\u0096\5_\60\2\u0096\u0097')
        buf.write('\5a\61\2\u0097\u0098\5k\66\2\u0098\u0099\7"\2\2\u0099')
        buf.write("\u009a\5M'\2\u009a\u009b\5e\63\2\u009b\u009c\5m\67\2")
        buf.write("\u009c\u009d\5E#\2\u009d\u009e\5[.\2\u009e\u00a2\3\2\2")
        buf.write("\2\u009f\u00a0\7#\2\2\u00a0\u00a2\7?\2\2\u00a1\u0086\3")
        buf.write("\2\2\2\u00a1\u008d\3\2\2\2\u00a1\u009f\3\2\2\2\u00a2\6")
        buf.write("\3\2\2\2\u00a3\u00a4\5I%\2\u00a4\u00a5\5a\61\2\u00a5\u00a6")
        buf.write("\5_\60\2\u00a6\u00a7\5k\66\2\u00a7\u00a8\5E#\2\u00a8\u00a9")
        buf.write("\5U+\2\u00a9\u00aa\5_\60\2\u00aa\u00ab\5i\65\2\u00ab\b")
        buf.write("\3\2\2\2\u00ac\u00ad\5K&\2\u00ad\u00b1\5a\61\2\u00ae\u00af")
        buf.write("\5M'\2\u00af\u00b0\5i\65\2\u00b0\u00b2\3\2\2\2\u00b1")
        buf.write("\u00ae\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2\u00b3\3\2\2\2")
        buf.write('\u00b3\u00b4\7"\2\2\u00b4\u00b5\5_\60\2\u00b5\u00b6\5')
        buf.write('a\61\2\u00b6\u00b7\5k\66\2\u00b7\u00b8\7"\2\2\u00b8\u00b9')
        buf.write("\5I%\2\u00b9\u00ba\5a\61\2\u00ba\u00bb\5_\60\2\u00bb\u00bc")
        buf.write("\5k\66\2\u00bc\u00bd\5E#\2\u00bd\u00be\5U+\2\u00be\u00bf")
        buf.write("\5_\60\2\u00bf\n\3\2\2\2\u00c0\u00c1\5]/\2\u00c1\u00c2")
        buf.write("\5E#\2\u00c2\u00c3\5k\66\2\u00c3\u00c4\5I%\2\u00c4\u00c5")
        buf.write("\5S*\2\u00c5\u00c6\5M'\2\u00c6\u00c7\5i\65\2\u00c7\u00ca")
        buf.write("\3\2\2\2\u00c8\u00ca\7\u0080\2\2\u00c9\u00c0\3\2\2\2\u00c9")
        buf.write("\u00c8\3\2\2\2\u00ca\f\3\2\2\2\u00cb\u00cc\5K&\2\u00cc")
        buf.write("\u00d0\5a\61\2\u00cd\u00ce\5M'\2\u00ce\u00cf\5i\65\2")
        buf.write("\u00cf\u00d1\3\2\2\2\u00d0\u00cd\3\2\2\2\u00d0\u00d1\3")
        buf.write('\2\2\2\u00d1\u00d2\3\2\2\2\u00d2\u00d3\7"\2\2\u00d3\u00d4')
        buf.write("\5_\60\2\u00d4\u00d5\5a\61\2\u00d5\u00d6\5k\66\2\u00d6")
        buf.write('\u00d7\7"\2\2\u00d7\u00d8\5]/\2\u00d8\u00d9\5E#\2\u00d9')
        buf.write("\u00da\5k\66\2\u00da\u00db\5I%\2\u00db\u00dc\5S*\2\u00dc")
        buf.write("\u00e0\3\2\2\2\u00dd\u00de\7#\2\2\u00de\u00e0\7\u0080")
        buf.write("\2\2\u00df\u00cb\3\2\2\2\u00df\u00dd\3\2\2\2\u00e0\16")
        buf.write("\3\2\2\2\u00e1\u00e2\5U+\2\u00e2\u00e3\5_\60\2\u00e3\20")
        buf.write("\3\2\2\2\u00e4\u00e5\5_\60\2\u00e5\u00e6\5a\61\2\u00e6")
        buf.write('\u00e7\5k\66\2\u00e7\u00e8\7"\2\2\u00e8\u00e9\5U+\2\u00e9')
        buf.write("\u00ea\5_\60\2\u00ea\22\3\2\2\2\u00eb\u00ec\7@\2\2\u00ec")
        buf.write("\24\3\2\2\2\u00ed\u00ee\7@\2\2\u00ee\u00ef\7?\2\2\u00ef")
        buf.write("\26\3\2\2\2\u00f0\u00f1\7>\2\2\u00f1\30\3\2\2\2\u00f2")
        buf.write("\u00f3\7>\2\2\u00f3\u00f4\7?\2\2\u00f4\32\3\2\2\2\u00f5")
        buf.write("\u00f6\5E#\2\u00f6\u00f7\5_\60\2\u00f7\u00f8\5K&\2\u00f8")
        buf.write("\34\3\2\2\2\u00f9\u00fa\5a\61\2\u00fa\u00fb\5g\64\2\u00fb")
        buf.write("\36\3\2\2\2\u00fc\u00fd\5_\60\2\u00fd\u00fe\5a\61\2\u00fe")
        buf.write("\u00ff\5k\66\2\u00ff \3\2\2\2\u0100\u0101\7*\2\2\u0101")
        buf.write('"\3\2\2\2\u0102\u0103\7+\2\2\u0103$\3\2\2\2\u0104\u0105')
        buf.write("\t\2\2\2\u0105&\3\2\2\2\u0106\u0108\7\17\2\2\u0107\u0106")
        buf.write("\3\2\2\2\u0107\u0108\3\2\2\2\u0108\u0109\3\2\2\2\u0109")
        buf.write("\u010c\7\f\2\2\u010a\u010c\7\17\2\2\u010b\u0107\3\2\2")
        buf.write("\2\u010b\u010a\3\2\2\2\u010c\u010d\3\2\2\2\u010d\u010e")
        buf.write("\b\24\2\2\u010e(\3\2\2\2\u010f\u0114\59\35\2\u0110\u0114")
        buf.write('\5;\36\2\u0111\u0114\5=\37\2\u0112\u0114\5C"\2\u0113')
        buf.write("\u010f\3\2\2\2\u0113\u0110\3\2\2\2\u0113\u0111\3\2\2\2")
        buf.write("\u0113\u0112\3\2\2\2\u0114\u0115\3\2\2\2\u0115\u0113\3")
        buf.write("\2\2\2\u0115\u0116\3\2\2\2\u0116*\3\2\2\2\u0117\u011c")
        buf.write("\5\67\34\2\u0118\u011b\5)\25\2\u0119\u011b\5%\23\2\u011a")
        buf.write("\u0118\3\2\2\2\u011a\u0119\3\2\2\2\u011b\u011e\3\2\2\2")
        buf.write("\u011c\u011a\3\2\2\2\u011c\u011d\3\2\2\2\u011d\u011f\3")
        buf.write("\2\2\2\u011e\u011c\3\2\2\2\u011f\u0120\5\67\34\2\u0120")
        buf.write(",\3\2\2\2\u0121\u0124\5)\25\2\u0122\u0124\5+\26\2\u0123")
        buf.write("\u0121\3\2\2\2\u0123\u0122\3\2\2\2\u0124.\3\2\2\2\u0125")
        buf.write("\u0127\5!\21\2\u0126\u0125\3\2\2\2\u0126\u0127\3\2\2\2")
        buf.write("\u0127\u012b\3\2\2\2\u0128\u012a\5%\23\2\u0129\u0128\3")
        buf.write("\2\2\2\u012a\u012d\3\2\2\2\u012b\u0129\3\2\2\2\u012b\u012c")
        buf.write("\3\2\2\2\u012c\u012e\3\2\2\2\u012d\u012b\3\2\2\2\u012e")
        buf.write("\u0138\5-\27\2\u012f\u0133\5\65\33\2\u0130\u0132\5%\23")
        buf.write("\2\u0131\u0130\3\2\2\2\u0132\u0135\3\2\2\2\u0133\u0131")
        buf.write("\3\2\2\2\u0133\u0134\3\2\2\2\u0134\u0136\3\2\2\2\u0135")
        buf.write("\u0133\3\2\2\2\u0136\u0137\5-\27\2\u0137\u0139\3\2\2\2")
        buf.write("\u0138\u012f\3\2\2\2\u0139\u013a\3\2\2\2\u013a\u0138\3")
        buf.write("\2\2\2\u013a\u013b\3\2\2\2\u013b\u013f\3\2\2\2\u013c\u013e")
        buf.write("\5%\23\2\u013d\u013c\3\2\2\2\u013e\u0141\3\2\2\2\u013f")
        buf.write("\u013d\3\2\2\2\u013f\u0140\3\2\2\2\u0140\u0143\3\2\2\2")
        buf.write("\u0141\u013f\3\2\2\2\u0142\u0144\5#\22\2\u0143\u0142\3")
        buf.write("\2\2\2\u0143\u0144\3\2\2\2\u0144\60\3\2\2\2\u0145\u014a")
        buf.write("\59\35\2\u0146\u014a\5;\36\2\u0147\u014a\5=\37\2\u0148")
        buf.write("\u014a\5? \2\u0149\u0145\3\2\2\2\u0149\u0146\3\2\2\2\u0149")
        buf.write("\u0147\3\2\2\2\u0149\u0148\3\2\2\2\u014a\u014b\3\2\2\2")
        buf.write("\u014b\u0149\3\2\2\2\u014b\u014c\3\2\2\2\u014c\u014d\3")
        buf.write("\2\2\2\u014d\u014f\5!\21\2\u014e\u0150\5-\27\2\u014f\u014e")
        buf.write("\3\2\2\2\u014f\u0150\3\2\2\2\u0150\u015c\3\2\2\2\u0151")
        buf.write("\u0155\5\65\33\2\u0152\u0154\5%\23\2\u0153\u0152\3\2\2")
        buf.write("\2\u0154\u0157\3\2\2\2\u0155\u0153\3\2\2\2\u0155\u0156")
        buf.write("\3\2\2\2\u0156\u0158\3\2\2\2\u0157\u0155\3\2\2\2\u0158")
        buf.write("\u0159\5-\27\2\u0159\u015b\3\2\2\2\u015a\u0151\3\2\2\2")
        buf.write("\u015b\u015e\3\2\2\2\u015c\u015a\3\2\2\2\u015c\u015d\3")
        buf.write("\2\2\2\u015d\u015f\3\2\2\2\u015e\u015c\3\2\2\2\u015f\u0160")
        buf.write("\5#\22\2\u0160\62\3\2\2\2\u0161\u0167\5A!\2\u0162\u0163")
        buf.write("\7^\2\2\u0163\u0166\7\61\2\2\u0164\u0166\n\3\2\2\u0165")
        buf.write("\u0162\3\2\2\2\u0165\u0164\3\2\2\2\u0166\u0169\3\2\2\2")
        buf.write("\u0167\u0165\3\2\2\2\u0167\u0168\3\2\2\2\u0168\u016a\3")
        buf.write("\2\2\2\u0169\u0167\3\2\2\2\u016a\u016b\5A!\2\u016b\64")
        buf.write("\3\2\2\2\u016c\u016d\7.\2\2\u016d\66\3\2\2\2\u016e\u016f")
        buf.write("\7$\2\2\u016f8\3\2\2\2\u0170\u0171\t\4\2\2\u0171:\3\2")
        buf.write("\2\2\u0172\u0173\t\5\2\2\u0173<\3\2\2\2\u0174\u0175\t")
        buf.write("\6\2\2\u0175>\3\2\2\2\u0176\u0177\7a\2\2\u0177@\3\2\2")
        buf.write("\2\u0178\u0179\7\61\2\2\u0179B\3\2\2\2\u017a\u0180\7\60")
        buf.write("\2\2\u017b\u0180\5? \2\u017c\u0180\7/\2\2\u017d\u0180")
        buf.write("\5A!\2\u017e\u0180\7<\2\2\u017f\u017a\3\2\2\2\u017f\u017b")
        buf.write("\3\2\2\2\u017f\u017c\3\2\2\2\u017f\u017d\3\2\2\2\u017f")
        buf.write("\u017e\3\2\2\2\u0180D\3\2\2\2\u0181\u0182\t\7\2\2\u0182")
        buf.write("F\3\2\2\2\u0183\u0184\t\b\2\2\u0184H\3\2\2\2\u0185\u0186")
        buf.write("\t\t\2\2\u0186J\3\2\2\2\u0187\u0188\t\n\2\2\u0188L\3\2")
        buf.write("\2\2\u0189\u018a\t\13\2\2\u018aN\3\2\2\2\u018b\u018c\t")
        buf.write("\f\2\2\u018cP\3\2\2\2\u018d\u018e\t\r\2\2\u018eR\3\2\2")
        buf.write("\2\u018f\u0190\t\16\2\2\u0190T\3\2\2\2\u0191\u0192\t\17")
        buf.write("\2\2\u0192V\3\2\2\2\u0193\u0194\t\20\2\2\u0194X\3\2\2")
        buf.write("\2\u0195\u0196\t\21\2\2\u0196Z\3\2\2\2\u0197\u0198\t\22")
        buf.write("\2\2\u0198\\\3\2\2\2\u0199\u019a\t\23\2\2\u019a^\3\2\2")
        buf.write("\2\u019b\u019c\t\24\2\2\u019c`\3\2\2\2\u019d\u019e\t\25")
        buf.write("\2\2\u019eb\3\2\2\2\u019f\u01a0\t\26\2\2\u01a0d\3\2\2")
        buf.write("\2\u01a1\u01a2\t\27\2\2\u01a2f\3\2\2\2\u01a3\u01a4\t\30")
        buf.write("\2\2\u01a4h\3\2\2\2\u01a5\u01a6\t\31\2\2\u01a6j\3\2\2")
        buf.write("\2\u01a7\u01a8\t\32\2\2\u01a8l\3\2\2\2\u01a9\u01aa\t\33")
        buf.write("\2\2\u01aan\3\2\2\2\u01ab\u01ac\t\34\2\2\u01acp\3\2\2")
        buf.write("\2\u01ad\u01ae\t\35\2\2\u01aer\3\2\2\2\u01af\u01b0\t\36")
        buf.write("\2\2\u01b0t\3\2\2\2\u01b1\u01b2\t\37\2\2\u01b2v\3\2\2")
        buf.write("\2\u01b3\u01b4\t \2\2\u01b4x\3\2\2\2\37\2\u0084\u0092")
        buf.write("\u00a1\u00b1\u00c9\u00d0\u00df\u0107\u010b\u0113\u0115")
        buf.write("\u011a\u011c\u0123\u0126\u012b\u0133\u013a\u013f\u0143")
        buf.write("\u0149\u014b\u014f\u0155\u015c\u0165\u0167\u017f\3\b\2")
        buf.write("\2")
        return buf.getvalue()


class DjangoNLFLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    EQUALS = 1
    NEQUALS = 2
    CONTAINS = 3
    NCONTAINS = 4
    REGEX = 5
    NREGEX = 6
    IN = 7
    NIN = 8
    GT = 9
    GTE = 10
    LT = 11
    LTE = 12
    AND = 13
    OR = 14
    NOT = 15
    OPEN_PAREN = 16
    CLOSE_PAREN = 17
    WHITESPACE = 18
    NEWLINE = 19
    TEXT = 20
    QUOTED_TEXT = 21
    ARGUMENT = 22
    LISTING = 23
    FUNCTION = 24
    REGULAR_EXPR = 25

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>", "'>'", "'>='", "'<'", "'<='", "'('", "')'"]

    symbolicNames = [
        "<INVALID>",
        "EQUALS",
        "NEQUALS",
        "CONTAINS",
        "NCONTAINS",
        "REGEX",
        "NREGEX",
        "IN",
        "NIN",
        "GT",
        "GTE",
        "LT",
        "LTE",
        "AND",
        "OR",
        "NOT",
        "OPEN_PAREN",
        "CLOSE_PAREN",
        "WHITESPACE",
        "NEWLINE",
        "TEXT",
        "QUOTED_TEXT",
        "ARGUMENT",
        "LISTING",
        "FUNCTION",
        "REGULAR_EXPR",
    ]

    ruleNames = [
        "EQUALS",
        "NEQUALS",
        "CONTAINS",
        "NCONTAINS",
        "REGEX",
        "NREGEX",
        "IN",
        "NIN",
        "GT",
        "GTE",
        "LT",
        "LTE",
        "AND",
        "OR",
        "NOT",
        "OPEN_PAREN",
        "CLOSE_PAREN",
        "WHITESPACE",
        "NEWLINE",
        "TEXT",
        "QUOTED_TEXT",
        "ARGUMENT",
        "LISTING",
        "FUNCTION",
        "REGULAR_EXPR",
        "COMA",
        "QUOTE",
        "LOWERCASE",
        "UPPERCASE",
        "NUMBER",
        "UNDERSCORE",
        "SLASH",
        "SYMBOL",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    grammarFileName = "DjangoNLF.g4"

    def __init__(self, input_=None, output: TextIO = sys.stdout):
        super().__init__(input_, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(
            self, self.atn, self.decisionsToDFA, PredictionContextCache()
        )
        self._actions = None
        self._predicates = None
