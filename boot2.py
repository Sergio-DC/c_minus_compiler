from globalTypes import *
from Parser import *
from semantica import *
from cgen import *

f = open('sample.c-', 'r')
programa = f.read()
progLong = len(programa)
programa = programa + '$'
posicion = 0

globales(programa, posicion, progLong)

AST = parser(True)

semantica(AST, False, True)#Revisar modos de impresion antes de enviar
codeGen(AST, "salida.txt")

print("\n\n")
#mostrarTabla(stack_TS, False, True)
