from globalTypes import *
from calculadora import *
from semantica import *

index = 0
index_aux = 0
def codeGen(arbol, file_name):
    global index
    result = traverseTree(arbol, file_name, stack_TS, index) #El stack_TS viene del analizador semantico

index = 0
index_aux = 0  
def traverseTree(arbol, file_name, stack_TS, index):
    global index_aux
    if arbol != None:
        calculoAritmetico(arbol, stack_TS, index)

        if arbol.type == "compound_stmt":
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    traverseTree(node, file_name, stack_TS, index)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    traverseTree(arbol.children[child], file_name, stack_TS, index)

def calculoAritmetico(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]
    #Se ignora declaracion de constantes e.g x = 18(Para no colocarla en el codigo ensamblador), ya que se pasara a la calculadora en tiempo de compilacion
    if arbol.type == NodeType.EXPRESSION_1 and not isinstance(arbol.children[1].leaf, int):
        res = calculadora(arbol.children[1], stack_TS, index) # Recibe una expresion aritmentica en AST sin literales, calcula el resultado
        name_var = arbol.children[0].leaf
        updateTupla(NodeType.VAR_DECLARATION_1, name_var, 'valor', res, tabla_simbolos)
        print("li $a0 {}".format(int(res)))
        print("$sw $a0 0($sp)")
        print("addiu $sp $sp -4")



