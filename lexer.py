import os
import sys
from globalTypes import TokenType

posicion = 0 #posicion del puntero en el documento
#mainFile = os.getcwd() + "/matrix_csv.txt"
with open("./clean_csv/output/matrix_csv.txt") as f:
    simbolos = next(f).split('_')
    M = [[int(x) for x in line.split()] for line in f]
f = open('./input.txt', 'r')
programa = f.read() 		# lee todo el programa a tokenizar

programa += '$'                  # agregamos $ para representar EOF
progLong = len(programa) 	# progLong del programa
estado = 0
token = ''

mapa = {}
# Creamos un array(llamado mapa) que clasifica/separa los 'digitos' asignandoles un 0
# Al alfabeto y underscore
# e.g mapa = [0,0,0,..., (10)0, 1, 1, 1]
for i in range(len(simbolos)):
    for c in simbolos[i]:# recooremos primero digitos, luego alfabeto
        mapa[c]=i+1

def getToken():
    global programa
    global posicion
    global estado
    global token
    global mapa
    global progLong

   
    token = ''

    while posicion < progLong :
        c = programa[posicion] # Leemos cada caracter del programa 'ejemplo.txt'     # llega ' ',5
        #debug
        estadoAntiguo = estado
        simboloActual = mapa[c]

        estado = M[estado][mapa[c]]# Matriz que representa la funcion de transicion # estado = 0 mapa[c] = 0, estado = 1 mapa[c] = 1
        if estado == 2: # Estado de aceptacion de token
                estado = 0
                return TokenType.NUM.name, token
        elif estado == 15:
                posicion = posicion + 1
                estado = 0
                token +=c
                return TokenType.PLUS.name, TokenType.PLUS.value
        elif estado == 16:
                posicion = posicion + 1
                estado = 0
                token = '-'
                return TokenType.MINUS.name, TokenType.MINUS.value
        elif estado == 17:
                posicion = posicion + 1
                estado = 0
                token = '*'
                return TokenType.MULT.name, TokenType.MULT.value
        elif estado == 18:
                token += c
                posicion += 1
                c = programa[posicion];
                if c == '*': # It's a block comment
                    token += c
                    estado = 3 # Real state x
                else:
                    token += c #DIV
                    estado = 0
                    return TokenType.DIV.name, TokenType.DIV.value
        elif estado == 19:
            if c == '*':
                token += c
                posicion = posicion + 1
                estado = 3 # Real State x
            else:
                token += c
                estado = 3 #Real state 19
        elif estado == 20:
            token += c
            posicion += 1
            c = programa[posicion]
            if c == '/':
                token += c
                posicion+=1
                estado = 0
                return TokenType.COMMENT.name, token # go to State 21 and return comment
            elif c == '*':
                token += c
                estado = 4 # go to state 20
            else:
                token += c
                estado = 3
        elif estado == 22:# DIV
            estado = 0
            token = '/';
            return TokenType.DIV.name, TokenType.DIV.value
        elif estado == 23:
            token += c
            posicion += 1
            c = programa[posicion];
            # go to state 25
            if c == '=': # '<=' token
                token += c
                posicion += 1
                estado = 0 
                return TokenType.LET.name, TokenType.LET.value
            else: # go to state 24 LT '<'
                estado = 0
                return TokenType.LT.name, TokenType.LT.value
        elif estado == 26:
            token += c
            posicion += 1
            c = programa[posicion];
            # go to state 28
            if c == '=': # '>=' token
                token += c
                posicion += 1
                estado = 0 
                return TokenType.GET.name, TokenType.GET.value
            else: # go to state 27
                estado = 0
                return TokenType.GT.name, TokenType.GT.name
        elif estado == 29:
            token +=c
            c = programa[posicion + 1]
            if c.isalpha():
                estado = 7 # Go to state 29
            else:
                estado = 0
                posicion += 1
                return TokenType.ID.name, token # token ID, state 30
        elif estado == 31:
            token += c
            posicion += 1
            c = programa[posicion];
            # go to state 33
            if c == '=': # '==' token
                token += c
                posicion += 1
                estado = 0 
                return TokenType.EQ.name, TokenType.EQ.value
            else: # go to state 32 "ASSIGN"
                estado = 0
                return TokenType.ASSIGN.name, TokenType.ASSIGN.value
        elif estado == 34:
            token += c
            posicion += 1
            c = programa[posicion];
            # go to state 35
            if c == '=': # '!=' token
                token += c
                posicion += 1
                estado = 0 
                return TokenType.NOT_EQ.name, TokenType.NOT_EQ.value
            else: # go to state of error
                estado = 0
                token = "Error en !"
                return token, posicion
        elif estado == 36: #Token ';'
            token += c
            posicion += 1
            estado = 0
            return TokenType.SEMI.name, TokenType.SEMI.value
        elif estado == 37: # Token ','
            token += c
            posicion += 1
            estado = 0
            return TokenType.COMMA.name, TokenType.COMMA.value
        elif estado == 38: # Token '('
            token += c
            posicion += 1
            estado = 0
            return TokenType.LPAREN.name, TokenType.LPAREN.value
        elif estado == 39: # Token ')'
            token += c
            posicion += 1
            estado = 0
            return TokenType.RPAREN.name, TokenType.RPAREN.value
        elif estado == 40: # Token '['
            token += c
            posicion += 1
            estado = 0
            return TokenType.LBRACKET.name, TokenType.LBRACKET.value
        elif estado == 41: # Token ']'
            token += c
            posicion += 1
            estado = 0
            return TokenType.RBRACKET.name, TokenType.RBRACKET.value
        elif estado == 42: # Token '{'
            token += c
            posicion += 1
            estado = 0
            return TokenType.LBRACE.name, TokenType.LBRACE.value
        elif estado == 43: # Token '}'
            token += c
            posicion += 1
            estado = 0
            return TokenType.RBRACE.name, TokenType.RBRACE.value
        elif estado == 44:#EOF '$'
            token += c
            posicion += 1
            return TokenType.ENDFILE, TokenType.ENDFILE.value
        elif estado == 50:
            print("Error en: ", posicion)
            sys.exit()
        elif estado != 0:# Si el caracter es distinto del blanco lo concatenamos con el caracter anterior para formar un token
            if c != '\n':
                token += c
            elif c == '$':
                return token, posicion
        posicion+=1

# class States(Enum):
#     s18 = 2
#     s19 = 4



progLong = progLong 
token, tokenString =getToken()
while token != TokenType.ENDFILE:
    print("{}   {}".format(token,str(tokenString)))
    token, tokenString =getToken()    