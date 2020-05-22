from semantica import *

# Recibe un ast de expresiones aritmeticas y devuelve el resultado del calculo
#La TS la ocupamos cuando la expresion esta compuesta por literales, en este caso recurrimos a la TS para localizar el valor
def calculadora(arbol, stack_TS, index):
    resultado = 0;    
    resultado = preOrder(arbol, resultado, stack_TS, index)
    return resultado

def preOrder(arbol, resultado, stack_TS, index):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            return arbol.leaf
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado, stack_TS, index)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado, stack_TS, index)
        resultado = operacion(arbol.leaf, hijoLeft, hijoDer, stack_TS, index)
    return resultado

def operacion(op, valIzq, valDer, stack_TS, index):
    resultado = None
    tabla_simbolos = stack_TS[index]
    if not isinstance(valIzq, int):
        registro = getTupla(NodeType.VAR_DECLARATION_1, valIzq, tabla_simbolos)
        valIzq = registro['valor']#Reasignamos un valor de tipo INT
    if not isinstance(valDer, int):
        registro = getTupla(NodeType.VAR_DECLARATION_1, valDer, tabla_simbolos)
        valDer = registro['valor']#Reasignamos un valor de tipo INT
    
    if op == '+':
        resultado = int(valIzq) + int(valDer)
    if op == '-':
        resultado = int(valIzq) - int(valDer)
    if op == '*':
        resultado = int(valIzq) * int(valDer)
    if op == '/':
        resultado = int(valIzq) / int(valDer)

    return resultado
