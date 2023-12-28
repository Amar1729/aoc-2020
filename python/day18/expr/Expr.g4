grammar Expr;

prog: expr EOF;

expr:
	addExpr (TIMES addExpr)*
	;

addExpr:
	atom (PLUS atom)*
	;

atom
    : NUMBER    # int
	| '(' expr ')'  # parens
	;

PLUS
    : '+'
    ;

TIMES
    : '*'
    ;

NUMBER: ('0' .. '9')+ ;
WS: [ \r\n\t]+ -> skip;
