import sys
from globalTypes import TokenType

with open("./clean_csv/output/matrix_csv.txt") as f:
    simbolos = next(f).split('_')
    M = [[int(x) for x in line.split()] for line in f]

estado = 0
mapa = {}
lineOfCode_content = ''
errorNo = 0
lineno = 1
setOfErrorMessages = {}
# Creamos un array(llamado mapa) que clasifica/separa los 'digitos' asignandoles un 0
# Al alfabeto y underscore
# e.g mapa = [0,0,0,..., (10)0, 1, 1, 1]
for i in range(len(simbolos)):
    for c in simbolos[i]:# recorremos primero digitos, luego alfabeto
        mapa[c]=i+1

def globales(prog,pos,long):
    global programa
    global progLong
    global posicion
    programa = prog
    posicion = pos
    progLong = long

def getToken(imprime = True):
    global estado, posicion
    tokenAppend = '' 
    global mapa
    global lineOfCode_content, lineno #No. line of code
    global setOfErrorMessages, errorNo#Error number
    messageError = ''
    
    while posicion <= (progLong + 1) :
        c = programa[posicion] # Leemos cada caracter del programa 'ejemplo.txt'     # llega ' ',5
        #debug
        estadoAntiguo = estado
        simboloActual = mapa[c]
        tokenReconocido = False

        estado = M[estado][mapa[c]]# Matriz que representa la funcion de transicion # estado = 0 mapa[c] = 0, estado = 1 mapa[c] = 1
        if estado == 2: # Estado de aceptacion de token
                tokenReconocido = True
                token = TokenType.NUM.name
                tokenString = tokenAppend
        elif estado == 15:
                posicion = posicion + 1
                tokenAppend +=c
                tokenReconocido = True
                token = TokenType.PLUS.name
                tokenString = TokenType.PLUS.value
        elif estado == 16:
                posicion = posicion + 1
                tokenAppend = '-'
                tokenReconocido = True
                token = TokenType.MINUS.name
                tokenString = TokenType.MINUS.value
        elif estado == 17:
                posicion = posicion + 1
                tokenAppend = '*'
                tokenReconocido = True
                token = TokenType.MULT.name
                tokenString = TokenType.MULT.value
        elif estado == 18:
                tokenAppend += c
                posicion += 1
                c = programa[posicion];
                if c == '*': # It's a block comment
                    tokenAppend += c
                    estado = 3 # Real state x
                else:
                    tokenAppend += c #DIV
                    tokenReconocido = True
                    token = TokenType.DIV.name
                    tokenStringTokenType.DIV.value
        elif estado == 19:
            if c == '*':
                tokenAppend += c
                posicion = posicion + 1
                estado = 3 # Real State x
            else:
                tokenAppend += c
                estado = 3 #Real state 19
        elif estado == 20:
            tokenAppend += c
            posicion += 1
            c = programa[posicion]
            if c == '/':
                tokenAppend += c
                posicion+=1
                token = TokenType.COMMENT.name
                tokenString = tokenAppend # go to State 21 and return comment
            elif c == '*':
                tokenAppend += c
                estado = 4 # go to state 20
            else:
                tokenAppend += c
                estado = 3
        elif estado == 22:# DIV
            token = TokenType.DIV.name
            tokenString = TokenType.DIV.value
        elif estado == 23:
            tokenAppend += c
            posicion += 1
            c = programa[posicion];
            # go to state 25
            if c == '=': # '<=' token
                tokenAppend += c
                posicion += 1
                tokenReconocido = True
                token = TokenType.LET.name
                tokenString = TokenType.LET.value
            else: # go to state 24 LT '<'
                tokenReconocido = True
                token = TokenType.LT.name
                tokenString = TokenType.LT.value
        elif estado == 26:
            tokenAppend += c
            posicion += 1
            c = programa[posicion];
            # go to state 28
            if c == '=': # '>=' token
                tokenAppend += c
                posicion += 1 
                tokenReconocido = True
                token = TokenType.GET.name
                tokenString = TokenType.GET.value
            else: # go to state 27
                tokenReconocido = True
                token = TokenType.GT.name
                tokenString = TokenType.GT.name
        elif estado == 29:
            tokenAppend +=c
            c = programa[posicion + 1]
            if c.isalpha():
                estado = 7 # Go to state 29
            else:
                posicion += 1
                tokenReconocido = True
                token = TokenType.ID.name # token ID, state 30
                tokenString = tokenAppend 
        elif estado == 31:
            tokenAppend += c
            posicion += 1
            c = programa[posicion];
            # go to state 33
            if c == '=': # '==' token
                tokenAppend += c
                posicion += 1
                tokenReconocido = True
                token = TokenType.EQ.name
                tokenString = TokenType.EQ.value
            else: # go to state 32 "ASSIGN"
                tokenReconocido = True
                token = TokenType.ASSIGN.name
                tokenString = TokenType.ASSIGN.value
        elif estado == 34:
            tokenAppend += c
            posicion += 1
            c = programa[posicion];
            # go to state 35
            if c == '=': # '!=' token
                tokenAppend += c
                posicion += 1
                tokenReconocido = True
                token = TokenType.NOT_EQ.name
                tokenString = TokenType.NOT_EQ.value
            else: # go to state of error
                token = "Error en !"
                return token, posicion
        elif estado == 36: #Token ';'
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.SEMI.name
            tokenString = TokenType.SEMI.value
        elif estado == 37: # Token ','
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.COMMA.name
            tokenString = TokenType.COMMA.value
        elif estado == 38: # Token '('
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.LPAREN.name
            tokenString = TokenType.LPAREN.value
        elif estado == 39: # Token ')'
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.RPAREN.name
            tokenString = TokenType.RPAREN.value
        elif estado == 40: # Token '['
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.LBRACKET.name
            tokenString = TokenType.LBRACKET.value
        elif estado == 41: # Token ']'
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.RBRACKET.name
            tokenString = TokenType.RBRACKET.value
        elif estado == 42: # Token '{'
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            token = TokenType.LBRACE.name
            tokenString = TokenType.LBRACE.value
        elif estado == 43: # Token '}'
            tokenAppend += c
            posicion += 1
            token = TokenType.RBRACE.name
            tokenString = TokenType.RBRACE.value
            tokenReconocido = True
        elif estado == 44:#EOF '$'
            tokenAppend += c
            posicion += 1
            tokenReconocido = True
            lineno += 1
            token = TokenType.ENDFILE
            tokenString = TokenType.ENDFILE.value
        elif estado == 50:
            lineOfCode_content += c
            posicionError = progLong - posicion;
            while c != '\n':
                posicion += 1
                c = programa[posicion]
                if c == '$':
                    break
                lineOfCode_content += c;
            promptCursor = genBlankSpaces(posicionError)
            messageError = "Línea {}: Error en la formación de un entero: ".format(lineno) + "\n" + lineOfCode_content +  promptCursor
            setOfErrorMessages[errorNo] = messageError
            token = TokenType.ERROR.name
            tokenString = '""'
            tokenReconocido = True
        elif estado != 0:# Si el caracter es distinto del blanco lo concatenamos con el caracter anterior para formar un token
            if c != '\n':
                lineOfCode_content += c
                tokenAppend += c
                
        if(tokenReconocido):
            estado = 0
            if TokenType.ID.name == token:
                token = detectReservedWords(tokenString)

            if imprime:
                print(token," = ", tokenString)

            if token == TokenType.ENDFILE:
                for message in setOfErrorMessages:
                    print(setOfErrorMessages[message])
            lineOfCode_content += tokenString #Pair of lineno and line content

            return token, tokenString
        posicion+=1
        #Append the blank spaces into the lineOfCode_content
        if c == ' ':
            lineOfCode_content += c
        elif c == '\n':
            lineno += 1
            #print("{} {}".format(lineno, lineOfCode_content))
            lineOfCode_content = '' #Clean the line of code to save other more

def detectReservedWords(tokenAppend):
    if tokenAppend == TokenType.ELSE.value:
        return TokenType.ELSE.name
    elif tokenAppend == TokenType.IF.value:
        return TokenType.IF.name
    elif tokenAppend == TokenType.INT.value:
        return TokenType.INT.name
    elif tokenAppend == TokenType.RETURN.value:
        return TokenType.RETURN.name
    elif tokenAppend == TokenType.VOID.value:
        return TokenType.VOID.name
    elif tokenAppend == TokenType.WHILE.value:
        return TokenType.WHILE.name
    else:
        return TokenType.ID.name

def genBlankSpaces(spaces):
    blankSpaces = ''
    for i in range(spaces):
        blankSpaces += ' '
    blankSpaces += "^"

    return blankSpaces