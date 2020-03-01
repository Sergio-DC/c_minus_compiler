from enum import Enum

class TokenType(Enum):
    ID = 200
    NUM = 201
    COMMENT = 203
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    ASSIGN = '='
    EQ = '=='
    NOT_EQ = '!='
    LT = '<'
    GT = '>'
    LET = '<='
    GET = '>='
    LPAREN = '('
    RPAREN = ')'
    LBRACKET = '['
    RBRACKET = ']'
    LBRACE = '{'
    RBRACE = '}'
    PLUS = '+'
    MINUS = '-'
    MULT = '*'
    DIV = '/'
    SEMI = ';'
    COMMA = ','
    ENDFILE = '$'
