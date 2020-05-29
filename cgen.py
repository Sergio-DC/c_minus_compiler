from globalTypes import *
#from calculadora import *
from calculadora_mips import *
from semantica import *

index = 0
index_aux = 0
def codeGen(arbol, file_name):
    global index
    print(".data")
    print(".text")
    print(".globl main")
    result = traverseTree(arbol, file_name, stack_TS, index) #El stack_TS viene del analizador semantico
    print("\n#Finish Program")
    print("li $v0 10")
    print("syscall")

index = 0
index_aux = 0 
NAME_FUNCTION = ''
def traverseTree(arbol, file_name, stack_TS, index):
    global index_aux, NAME_FUNCTION
    if arbol != None:
        if arbol.type == NodeType.FUN_DECLARATION:
            nombre_funcion = arbol.children[0].leaf
            if nombre_funcion == 'main':
                genCode_mainFunc(arbol, stack_TS, index)
            else: # CALLE PART
                genCode_calle(nombre_funcion)
        if arbol.type == NodeType.EXPRESSION_1 :
            NAME_FUNCTION = arbol.children[1].leaf
            variable = arbol.children[0].leaf
            if arbol.children[1].type == NodeType.CALL and NAME_FUNCTION == 'input': #Funcion Input
                genCode_input(arbol, stack_TS, index)
                genCode_updateVariable(arbol, stack_TS, index)
            else:
                NAME_FUNCTION = calculadora(arbol.children[1], stack_TS, index) # Recibe una expresion aritmentica en AST y genera codigo para el calculo
                genCode_updateVariable(arbol, stack_TS, index)
        elif arbol.type == NodeType.CALL and not NAME_FUNCTION == arbol.leaf:
            if arbol.leaf == "output":
                genCode_output(arbol, stack_TS, index)

        if arbol.type == NodeType.RETURN_STMT_2:
            print("#Calculate the expression of RETURN_STMT")
            calculadora(arbol.children[0], stack_TS, index)            
        if arbol.type == "compound_stmt":
            tabla_simbolos = stack_TS[index]
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    traverseTree(node, file_name, stack_TS, index)

            if index < len(stack_TS) - 1: #Retorno de valor al terminar los pasos de una funcion
                genCode_returnVal(arbol, stack_TS, index)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    traverseTree(arbol.children[child], file_name, stack_TS, index)

#Recoradtorio: renombrar la funcion por uno mas apropiado al contexto
def genCode_updateVariable(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]
    nombre_variable = arbol.children[0].leaf
    tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)
    # Update the variable
    logical_offset = tupla['offset']
    print("#Update variable {}".format(nombre_variable))
    genCode_calculatePhysicalOffset(logical_offset)
    # Search the variable 'x' using the physical offset and store the value in the stack
    print("# Search the variable '{}' using the physical offset and load the value from memory to register $a0".format(nombre_variable))
    print("subu $t6 $fp $t6")
    print("sw $a0 ($t6)")# the follwing line is taking advantage of $fp to search the 'X' variable
        

def genCode_mainFunc(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]
    #Obtenemos de la TS la tupla de la declaracion de main en el scope global
    tupla = getTupla(NodeType.FUN_DECLARATION, 'main', tabla_simbolos)
    #Obtenemos el index_scope
    index_scope = tupla['index_scope']
    #Buscamos en el stack_TS una tabla de simbolos que cumpla con el criterio de 'index_scopes'
    nueva_tabla_simbolos = stack_TS[index_scope] #Esa tabla contiene las variables locales declaradas dentro de main
    # Obtenemos el numero de variable declaradas en la funcion main
    N = getMatches(NodeType.VAR_DECLARATION_1, nueva_tabla_simbolos)#Representa el numero de variables declaradas localmente en la funcion main
    print("main:")
    print("move $fp $sp # Set FP to the bottom")# Set %fp to the bottom
    print("addiu $sp $sp -4  # Move stack_pointer to the next empty position")# Move stack_pointer to the next empty position
    # Store the matches of local variables in $t7
    genCode_calculatePhysicalOffset(N)
    print("sub $sp $sp $t6")

def genCode_input(arbol, stack_TS, index):
    if arbol.children[0].type == NodeType.VAR_1:
        print("#Input")
        print("li $v0, 5")
        print("syscall")
        print("move $a0 $v0")
def genCode_output(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]
    print("\n#Print the value")
    # Search the variable in ST that is gonna printed 
    #Get the logical offset of the variable
    nombre_variable = arbol.children[0].leaf
    tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)
    logical_offset = tupla['offset']
    genCode_calculatePhysicalOffset(logical_offset)
    print("subu $t6 $fp $t6")
    print("lw $a0 ($t6)")
    print("li $v0 1")
    print("syscall")
    #Print a new Line
    print("addi $a0, $0, 0xA #ascii code for LF, if you have any trouble try 0xD for CR.")
    print("addi $v0, $0, 0xB #syscall 11 prints the lower 8 bits of $a0 as an ascii character.")
    print("syscall")

def genCode_calle(nombre_funcion):
    print("\n #Calle Part")
    print("{}:".format(nombre_funcion))# The label
    print("move $fp $sp #move the pointer of the $fp to point to $sp")
    print("sw $ra 0($sp) #save the return address in the activation record")
    print("addiu $sp $sp -4")

def genCode_returnVal(arbol, stack_TS, index):
    print("\n\n# Return the value")
    tabla_simbolos = stack_TS[index]
    # Load return address to register $ra
    print("lw $ra 4($sp)")
    # The stack-pointer will do a deep pop to restore to the pevious activation-frame top 
    #Get from the ST the count of parameters
    num_of_params = getMatches(NodeType.PARAM_1, tabla_simbolos)
    print("li $t0 {}  # {} represents the number of total params obtained from ST".format(num_of_params, num_of_params))
    print("#deep offset = z")
    print("li $t6 4")
    print("mult $t0 $t6  #  4 * N") #  4 * N
    print("mflo $t0") 
    print("addi $t0 $t0 8  # z = 4*n + 8") # z = 4*n + 8
    print("addu $sp $sp $t0")
    print("lw $fp 0($sp) #Restore the $fp to the old Frame pointer") # Restore the $fp to the old Frame pointer 
    print("jr $ra #Return control to caller function")





