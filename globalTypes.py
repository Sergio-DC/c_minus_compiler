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
    PARAM_1 = 3 # Representa la estructura de un parametro aislado e.g int x
    PARAMS_1 = 4 # Representa la lista de parametros, ver doc de C- para más info
    PARAMS_2 = 5 # Representa un parametro vacio
    EXPRESSION_1 = 6
    EXPRESSION_2 = 7
    RETURN_STMT_2 = 8
    VAR_1  = 9
    CALL = 10
    ADDITIVE_EXPRESSION_1 = 11
    PARAM_2 = 12
    TYPE_SPECIFIER = 13
    IO = 14
    NUMBER = 15
    TERM_1 = 16

def genCode_calculatePhysicalOffset(logical_offset):
    print("li $t7 {} # <- Logical offset".format(logical_offset))
    print("li $t6 4 # Num 4 is the byte_alignment")
    print("mult $t7 $t6 # Calculate physical offset")  # Calculate physical offset"
    print("mflo $t6 # <- It has the physical offset") # <- It has the physical offset