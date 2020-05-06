from enum import Enum

class TokenType(Enum):
    #Reserved Words
     ELSE = "ELSE"
     IF = "IF"
     INT = "INT"
     RETURN = "RETURN"
     VOID = "VOID"
     WHILE = "WHILE"
     # Symbols
     PLUS = "PLUS"
     MINUS = "MINUS"
     TIMES = "TIMES"
     DIVIDE = "DIVIDE"
     LESS = "LESS"
     LESSEQUAL = "LESSEQUAL"
     GREATER = "GREATER"
     GREATEREQUAL = "GREATEREQUAL"
     ASSIGN = "ASSIGN"
     DEQUAL = "DEQUAL"
     DISTINT = "DISTINT"
     SEMICOLON = "SEMICOLON"
     COMMA = "COMMA"
     LPAREN = "LPAREN"
     RPAREN = "RPAREN"
     LBRACKET = "LBRACKET"
     RBRACKET = "RBRACKET"
     LBLOCK = "LBLOCK"
     RBLOCK = "RLOCK"
     COMMENTS = "COMMENTS"
     # Others	
     ID = "ID"
     NUMBER = "NUMBER"
     SPACES = "SPACES"
     ENDFILE = "$"
     ERROR = "ERROR"

class NodeType(Enum):
    VAR_DECLARATION_1 = 0
    VAR_DECLARATION_2 = 1
    FUN_DECLARATION = 2
    PARAMS = 3
    EXPRESSION_1 = 4
    RETURN_STMT_2 = 5

