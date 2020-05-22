from globalTypes import *
from calculadora import *

def codeGen(arbol, file_name):
    result = traverseTree(arbol, file_name)

    
def traverseTree(arbol, file_name):
    if arbol != None:
        calculoAritmetico(arbol)

        if arbol.type == "compound_stmt":
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    traverseTree(node, file_name)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    traverseTree(arbol.children[child], file_name)

def calculoAritmetico(arbol):
    if arbol.type == NodeType.EXPRESSION_1:
        res = calculadora(arbol.children[1]) # Recibe una expresion aritmentica en AST sin literales, calcula el resultado
        print("li $a0 {}".format(int(res)))
        print("$sw $a0 0($sp)")
        print("addiu $sp $sp -4")



