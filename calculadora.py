def calculadora(arbol):
    resultado = 0;    
    resultado = preOrder(arbol, resultado)
    return resultado

def preOrder(arbol, resultado):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            return arbol.leaf
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado)
        resultado = operacion(arbol.leaf, hijoLeft, hijoDer)
    return resultado

def operacion(op, valIzq, valDer):
    resultado = None
    # if not isinstance(valIzq, int):
    #     registro = getTupla(NodeType.VAR_DECLARATION_1, valIzq, tabla_simbolos)
    #     valIzq = registro['valor']#Reasignamos un valor de tipo INT
    # if not isinstance(valDer, int):
    #     registro = getTupla(NodeType.VAR_DECLARATION_1, valDer, tabla_simbolos)
    #     valDer = registro['valor']#Reasignamos un valor de tipo INT
    
    if op == '+':
        resultado = int(valIzq) + int(valDer)
    if op == '-':
        resultado = int(valIzq) - int(valDer)
    if op == '*':
        resultado = int(valIzq) * int(valDer)
    if op == '/':
        resultado = int(valIzq) / int(valDer)

    return resultado
