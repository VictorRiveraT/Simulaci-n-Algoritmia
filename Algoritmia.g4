grammar Algoritmia;

// =========================
// Regla Inicial
// =========================
program: (procDecl | NEWLINE)* EOF; // Permitir newlines entre procedimientos

// =========================
// Declaraciones y Bloques
// =========================
procDecl
    : ID ID* PROC_START (statement | NEWLINE)* PROC_END (NEWLINE | EOF)?
    ;

statement:
    // Las sentencias simples DEBEN terminar en un NEWLINE
    ( assignStmt | readStmt | writeStmt | playStmt | listAppendStmt | listCutStmt | procCallStmt ) NEWLINE
    // Las sentencias compuestas (bloques) manejan sus propios finales
    | ifStmt
    | whileStmt
    ;

ifStmt
    : IF expression PROC_START (statement | NEWLINE)* PROC_END
      (ELSE PROC_START (statement | NEWLINE)* PROC_END)?
      (NEWLINE | EOF)?
    ;

whileStmt
    : WHILE expression PROC_START (statement | NEWLINE)* PROC_END
      (NEWLINE | EOF)?
    ;

// =========================
// Sentencias Específicas
// =========================
assignStmt:
    ID ASSIGN expression
    ;
readStmt:
    READ ID
    ;
writeStmt:
    WRITE expression (expression)*
    ;
playStmt:
    PLAY expression
    ;
procCallStmt:
    ID (expression)*
    ;
listAppendStmt:
    ID APPEND expression
    ;
listCutStmt:
    CUT listAccessExpr
    ;

// =========================
// Expresiones
// =========================
expression:
    relExpr
    ;
relExpr:
    addExpr ( (EQ | NEQ | LT | LTE | GT | GTE) addExpr )*
    ;
addExpr:
    multExpr ( (PLUS | MINUS) multExpr )*
    ;
multExpr:
    term ( (MULT | DIV | MOD) term )*
    ;
term:
    '(' expression ')'
    | listLiteral
    | listAccessExpr
    | lengthExpr
    | INT
    | NOTE
    | ID
    | STRING
    ;
listLiteral:
    LBRACE (expression)* RBRACE
    ;
listAccessExpr:
    ID LBRACK expression RBRACK
    ;
lengthExpr:
    LENGTH expression
    ;

// =========================
// LÉXICO (Tokens)
// =========================

// Palabras clave
IF:     'if';
ELSE:   'else';
WHILE:  'while';
// Operadores
ASSIGN: '<-';
READ:   '<?>';
WRITE:  '<w>';
PLAY:   '(:)';
APPEND: '<<';
CUT:    '8<';
LENGTH: '#';
// Bloques
PROC_START: '|:';
PROC_END:   ':|';
// Expresiones
PLUS:   '+';
MINUS:  '-';
MULT:   '*';
DIV:    '/';
MOD:    '%';
EQ:     '=';
NEQ:    '/=';
LT:     '<';
LTE:    '<=';
GT:     '>';
GTE:    '>=';
// Átomos
// Antes: NOTE: [A-G][0-8]?;
// Ahora aceptamos dos puntos opcionales y una letra de duración
NOTE: [A-G] [0-8]? (':' [whqes])?;
ID:     [A-Za-z_][A-Za-z0-9_]*;
INT:    [0-9]+;
STRING: '"' (~["\r\n])*? '"';
// Símbolos
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';

// Ignorar
COMMENT : '###' ( . | '\r' | '\n' )*? '###' -> skip ; // Comentarios
NEWLINE: ( '\r'? '\n' | '\r' )+ ;       // Capturar uno o más saltos de línea
WS:      [ \t]+                 -> skip; // Solo saltar espacios y tabs