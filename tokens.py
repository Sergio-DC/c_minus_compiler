import os
import sys
#from globalTypes import TokenType
# from enum import Enum

p = 0 #posicion del puntero en el documento
#mainFile = os.getcwd() + "/matrix_csv.txt"
with open("./clean_csv/output/matrix_csv.txt") as f:
    simbolos = next(f).split('_')
    M = [[int(x) for x in line.split()] for line in f]
f = open('./input.txt', 'r')
archivo = f.read() 		# lee todo el archivo a tokenizar

#archivo += '$'                  # agregamos $ para representar EOF
longitud = len(archivo) 	# longitud del archivo
estado = 0
token = ''

mapa = {}
# Creamos un array(llamado mapa) que clasifica/separa los 'digitos' asignandoles un 0
# Al alfabeto y underscore
# e.g mapa = [0,0,0,..., (10)0, 1, 1, 1]
for i in range(len(simbolos)):
    for c in simbolos[i]:# recooremos primero digitos, luego alfabeto
        mapa[c]=i+1

def getToken(archivo):
    global p
    global estado
    global token
    global mapa

   
    token = ''

    while p < longitud :
        c = archivo[p] # Leemos cada caracter del archivo 'ejemplo.txt'     # llega ' ',5
        #debug
        estadoAntiguo = estado
        simboloActual = mapa[c]

        estado = M[estado][mapa[c]]# Matriz que representa la funcion de transicion # estado = 0 mapa[c] = 0, estado = 1 mapa[c] = 1
        if estado == 2: # Estado de aceptacion de token
                estado = 0
                return token, p
        elif estado == 15:
                p = p + 1
                estado = 0
                token = '+'
                return token, p
        elif estado == 16:
                p = p + 1
                estado = 0
                token = '-'
                return token, p
        elif estado == 17:
                p = p + 1
                estado = 0
                token = '*'
                return token, p
        elif estado == 18:
                token += c
                p += 1
                c = archivo[p];
                if c == '*': # It's a block comment
                    token += c
                    estado = 3 # Real state x
                else:
                    token = '/' #DIV
                    estado = 0
                    return token, p
        elif estado == 19:
            if c == '*':
                token += c
                p = p + 1
                estado = 3 # Real State x
            else:
                token += c
                estado = 3 #Real state 19
        elif estado == 20:
            token += c
            p += 1
            c = archivo[p]
            if c == '/':
                token += c
                p+=1
                estado = 0
                return token, p # go to State 21 and return comment
            elif c == '*':
                token += c
                estado = 4 # go to state 20
            else:
                token += c
                estado = 3
        elif estado == 22:# DIV
            estado = 0
            token = '/';
            return token, p
        elif estado == 50:
            print("Error en: ", p)
            sys.exit()
        elif estado != 0:# Si el caracter es distinto del blanco lo concatenamos con el caracter anterior para formar un token
            if c != '\n':
                token += c
        p+=1

# class States(Enum):
#     s18 = 2
#     s19 = 4



longitud = longitud 
while p < longitud:
    token, p =getToken(archivo)
    print(token)
    print("posicion ", p+1)