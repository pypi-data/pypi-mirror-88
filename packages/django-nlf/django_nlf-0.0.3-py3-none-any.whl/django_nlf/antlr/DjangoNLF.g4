grammar DjangoNLF;

/*
 * Parser rules
 */
operator            : WHITESPACE* (AND | OR) WHITESPACE* ;
boolean_expr        : WHITESPACE* (EQUALS | NEQUALS) WHITESPACE+ field=TEXT ;
lookup              : WHITESPACE* (EQUALS | NEQUALS | CONTAINS | NCONTAINS | REGEX | NREGEX | IN | NIN | GT | GTE | LT | LTE) WHITESPACE* ;
expression          : (NOT WHITESPACE*)? value=FUNCTION
                    | boolean_expr
                    | ((NOT WHITESPACE*)? field=(TEXT | FUNCTION) lookup value=(TEXT | QUOTED_TEXT | LISTING | FUNCTION | REGULAR_EXPR)) ;
composite_expr      : (expression | nested_comp_expr) (operator (expression | nested_comp_expr))* ;
nested_comp_expr    : (NOT WHITESPACE*)? OPEN_PAREN composite_expr CLOSE_PAREN ;
filter_expr         : (composite_expr | nested_comp_expr) (operator (composite_expr | nested_comp_expr))* ;
parse               : filter_expr? WHITESPACE* EOF ;

/*
 * Lexer rules
 */

// Field lookups
EQUALS              : I S | E Q U A L S | '=' ;
NEQUALS             : I S ' ' N O T | D O (E S)? ' ' N O T ' ' E Q U A L | '!=' ;
CONTAINS            : C O N T A I N S ;
NCONTAINS           : D O (E S)? ' ' N O T ' ' C O N T A I N ;
REGEX               : M A T C H E S | '~' ;
NREGEX              : D O (E S)? ' ' N O T ' ' M A T C H | '!~' ;
IN                  : I N ;
NIN                 : N O T ' ' I N ;
GT                  : '>' ;
GTE                 : '>=' ;
LT                  : '<' ;
LTE                 : '<=' ;

// Operators
AND                 : A N D ;
OR                  : O R ;
NOT                 : N O T ;

OPEN_PAREN          : '(' ;
CLOSE_PAREN         : ')' ;
WHITESPACE          : (' ' | '\t') ;
NEWLINE             : ('\r'? '\n' | '\r') -> skip;
TEXT                : (LOWERCASE | UPPERCASE | NUMBER | SYMBOL)+ ;
QUOTED_TEXT         : QUOTE (TEXT | WHITESPACE)* QUOTE ;
ARGUMENT            : TEXT | QUOTED_TEXT ;
LISTING             : OPEN_PAREN? WHITESPACE* (ARGUMENT) (COMA WHITESPACE* (ARGUMENT))+ WHITESPACE* CLOSE_PAREN? ;
FUNCTION            : (LOWERCASE | UPPERCASE | NUMBER | UNDERSCORE)+ OPEN_PAREN (ARGUMENT)? (COMA WHITESPACE* (ARGUMENT))* CLOSE_PAREN ;
REGULAR_EXPR        : SLASH ('\\/' | ~[/])* SLASH ;

fragment COMA       : ',' ;
fragment QUOTE      : '"' ;
fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;
fragment NUMBER     : [0-9] ;
fragment UNDERSCORE : '_' ;
fragment SLASH      : '/' ;
fragment SYMBOL     : '.' | UNDERSCORE | '-' | SLASH | ':' ;
fragment A          : [aA] ;
fragment B          : [bB] ;
fragment C          : [cC] ;
fragment D          : [dD] ;
fragment E          : [eE] ;
fragment F          : [fF] ;
fragment G          : [gG] ;
fragment H          : [hH] ;
fragment I          : [iI] ;
fragment J          : [jJ] ;
fragment K          : [kK] ;
fragment L          : [lL] ;
fragment M          : [mM] ;
fragment N          : [nN] ;
fragment O          : [oO] ;
fragment P          : [pP] ;
fragment Q          : [qQ] ;
fragment R          : [rR] ;
fragment S          : [sS] ;
fragment T          : [tT] ;
fragment U          : [uU] ;
fragment V          : [vV] ;
fragment W          : [wW] ;
fragment X          : [xX] ;
fragment Y          : [yY] ;
fragment Z          : [zZ] ;
