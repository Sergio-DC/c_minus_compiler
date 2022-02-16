# coding=utf-8
from globalTypes import *
from Parser import *
from semantica import *
from cgen import *
#import pdb; pdb.set_trace()

f = open('sample.c-', 'r')
sourceCode = f.read()

setSourceCode(sourceCode)

setParserDebugMode(True)
AST = parser()

setShowTable(False)
semantica(AST, False, True)#Revisar modos de impresion antes de enviar

#setCgenDebugMode(False)
#codeGen(AST, "salida.asm")

print("\n\n")
#mostrarTabla(stack_TS, False, True)
