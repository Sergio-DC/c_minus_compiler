from globalTypes import *
#from calculadora import *
from calculadora_mips import *
from semantica import *

index = 0
index_aux = 0
def codeGen(arbol, file_name):
    global index

    print(".text")
    print(".globl main")
    result = traverseTree(arbol, file_name, stack_TS, index) #El stack_TS viene del analizador semantico
    print("\n#Finish Program")
    print("li $v0 10")
    print("syscall")

index = 0
index_aux = 0 
nombre_funcion = ''
def traverseTree(arbol, file_name, stack_TS, index):
    global index_aux
    if arbol != None:
        main(arbol, stack_TS, index)
        calculoAritmetico(arbol, stack_TS, index)
        # caller(arbol, stack_TS, index)
        # calle(arbol, stack_TS, index)
        input(arbol, stack_TS, index)

        if arbol.type == NodeType.ADDITIVE_EXPRESSION_1:
            print("\n")
            calculadora(arbol, stack_TS, index)

        if arbol.type == "compound_stmt":
            tabla_simbolos = stack_TS[index]
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    traverseTree(node, file_name, stack_TS, index)
            if index < len(stack_TS) - 1:
                print("\n\n# Return the value")
                nueva_tabla_simbolos = stack_TS[index]
                # Load return address to register $ra
                print("lw $ra 4($sp)")
                # The stack-pointer will do a deep pop to restore to the pevious activation-frame top 
                #Get from the ST the count of parameters
                num_of_params = getMatches(NodeType.PARAM_1, nueva_tabla_simbolos)
                print("li $t0 {}  # {} represents the number of total params obtained from ST".format(num_of_params, num_of_params))
                print("#deep offset = z")
                print("li $t6 4")
                print("mult $t0 $t6  #  4 * N") #  4 * N
                print("mflo $t0") 
                print("addi $t0 $t0 8  # z = 4*n + 8") # z = 4*n + 8
                print("addu $sp $sp $t0")
                print("lw $fp 0($sp) #Restore the $fp to the old Frame pointer") # Restore the $fp to the old Frame pointer 
                print("jr $ra")

            # print("jr $ra  #Return control to caller function")
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    traverseTree(arbol.children[child], file_name, stack_TS, index)
#Recoradtorio: renombrar la funcion por uno mas apropiado al contexto
def calculoAritmetico(arbol, stack_TS, index):
    global nombre_funcion
    tabla_simbolos = stack_TS[index]
    #Se ignora declaracion de constantes e.g x = 18(Para no colocarla en el codigo ensamblador), ya que se pasara a la calculadora en tiempo de compilacion
    if arbol.type == NodeType.EXPRESSION_1 :
        nombre_funcion = calculadora(arbol.children[1], stack_TS, index) # Recibe una expresion aritmentica en AST y genera codigo para el calculo
        nombre_variable = arbol.children[0].leaf
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)

        # Update the variable
        logical_offset = tupla['offset']
        print("#Update variable {}".format(nombre_variable))
        print("li $t7 {} # Number {} represent the logical offset of variable '{}', that number is obtained by ST".format(logical_offset, logical_offset, nombre_variable))
        print("li $t6 4") # 4 is the byte_alignment
        print("mult $t7 $t6")#Calculate physical offset
        print("mflo $t6  # <- it has the physical offset") # $t6 has the physical offset
        # Search the variable 'x' using the physical offset and store the value in the stack
        print("# Search the variable '{}' using the physical offset and load the value from memory to register $a0".format(nombre_variable))
        print("subu $t6 $fp $t6")
        print("sw $a0 ($t6)")# the follwing line is taking advantage of $fp to search the 'X' variable
    elif arbol.type == NodeType.CALL and not nombre_funcion == arbol.leaf:
        #¿Se podra ver lo que hay en un nivel superior? La respuesta es si, pero no es posible acceder directamente a esa referencia
        if arbol.leaf == "output":
            print("\n#Print the value")
            # Search the variable in ST that is gonna printed 
            #Get the logical offset of the variable
            nombre_variable = arbol.children[0].leaf
            tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)
            logical_offset = tupla['offset']
            print("li $t7 {}  # {} represent the logical offset of variable {}".format(logical_offset, logical_offset, nombre_variable)) 
            print("li $t6 4") # 4 byte-alignment
            print("mult $t7 $t6") #calculate physical offset
            print("mflo $t6")
            print("subu $t6 $fp $t6")
            print("lw $a0 ($t6)")
            print("li $v0 1")
            print("syscall")

# Recordatorio: Renombrar funcion
def main(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]

    if arbol.type == NodeType.FUN_DECLARATION:
        nombre_funcion = arbol.children[0].leaf
        if nombre_funcion == 'main':
            #Obtenemos de la TS la tupla de la declaracion de main en el scope global
            tupla = getTupla(NodeType.FUN_DECLARATION, 'main', tabla_simbolos)
            #Obtenemos el index_scope
            index_scope = tupla['index_scope']
            #Buscamos en el stack_TS una tabla de simbolos que cumpla con el criterio de 'index_scopes'
            nueva_tabla_simbolos = stack_TS[index_scope] #Esa tabla contiene las variables locales declaradas dentro de main
            # Obtenemos el numero de variable declaradas en la funcion main
            N = getMatches(NodeType.VAR_DECLARATION_1, nueva_tabla_simbolos)#Representa el numero de variables declaradas localmente en la funcion main
            #print("Numero de variables declaradas: ", N)

            print("main:")
            print("move $fp $sp # Set FP to the bottom")# Set %fp to the bottom
            print("addiu $sp $sp -4  # Move stack_pointer to the next empty position")# Move stack_pointer to the next empty position
            # Store the matches of local variables in $t7
            print("li $t7 {}  # Store the matches of local variables in $t7".format(N))
            # Reserve Space for the local variables
            print("li $t6 4")
            print("mult $t7 $t6  # N * 4") # N * 4
            print("mflo $t6") # physical offset that is going to use to reserve space in stack for local variables
            print("sub $sp $sp $t6")
        else: # There is a function different to main, CALLE PART
            print("\n #Calle Part")
            print("{}:".format(nombre_funcion))#The label
            print("move $fp $sp #move the pointer of the $fp to point to $sp")
            print("sw $ra 0($sp) #save the return address in the activation record")
            print("addiu $sp $sp -4")




def input(arbol, stack_TS, index):
    if arbol.type == NodeType.EXPRESSION_1:
        nombre_funcion = arbol.children[1].leaf
        if arbol.children[1].type == NodeType.CALL and nombre_funcion == 'input': #Funcion Input
            if arbol.children[0].type == NodeType.VAR_1:
                print("li $v0, 5")
                print("syscall")
                print("move $a0 $v0")
                #getTupla(NodeType.VAR_DECLARATION_1, )
                print("sw $a0 0($sp)")




