from semantica import *

# Recibe un AST de expresiones aritmeticas y genera codigo ensamblador
def calculadora(arbol, stack_TS, index):
    resultado = 0;
    if arbol.type == NodeType.NUMBER:
        print("li $a0 {}".format(arbol.leaf))
    else:
        resultado = preOrder(arbol, resultado, stack_TS, index)
    return resultado

def preOrder(arbol, resultado, stack_TS, index):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            if arbol.type == NodeType.NUMBER:
                #print("li $a0 {}".format(arbol.leaf))
                return arbol.leaf
            elif arbol.type == NodeType.CALL:
                caller(arbol, stack_TS, index)
                nombre_funcion = arbol.leaf
            else:
                nombre_funcion = arbol.leaf
            return nombre_funcion
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado, stack_TS, index)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado, stack_TS, index)
        operacion(arbol.leaf, hijoLeft, hijoDer, stack_TS, index)
    return resultado

def operacion(op, valIzq, valDer, stack_TS, index):
    tabla_simbolos = stack_TS[index]

    if not isinstance(valIzq, int):
        while(True):
            registro = getTupla(NodeType.VAR_DECLARATION_1, valIzq, tabla_simbolos)
            if registro != None:
                break
            registro = getTupla(NodeType.PARAM_1, valIzq, tabla_simbolos) #Si la variable declarada no se encuentra en VAR_DECLARATION_1 se busca en PARAM_1
            if registro != None:
                break
            if registro == None:
                print("No se encontro lo que buscabas en la TS")
                break
        logical_offset = registro['offset']
        print("#Val Left")
        print("li $t7 {} # <- Logical offset".format(logical_offset))
        print("li $t6 4 # Num 4 is the byte_alignment")
        print("mult $t7 $t6 # Calculate physical offset")  # Calculate physical offset"
        print("mflo $t6 # <- It has the physical offset") # <- It has the physical offset

        # index_scope = getIndexScope(registro) #The index_scope will be used as an index of stack_TS
        # stack_TS[index_scope] 

        if registro['type'] == NodeType.VAR_DECLARATION_1:
            print("subu $t6 $fp $t6")
            print("# Load the param value from stack to $t0")
            print("lw $t0 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valIzq))
        elif registro['type'] == NodeType.PARAM_1:
            print("addu $t6 $fp $t6")
            print("# Load the param value from stack to $t0")
            print("lw $t0 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valIzq))
    else:
        print("li $t0 {}".format(valIzq))
    if not isinstance(valDer, int):
        while(True):
            registro = getTupla(NodeType.VAR_DECLARATION_1, valDer, tabla_simbolos)
            if registro != None:
                break
            registro = getTupla(NodeType.PARAM_1, valDer, tabla_simbolos) #Si la variable declarada no se encuentra en VAR_DECLARATION_1 se busca en PARAM_1
            if registro != None:
                break
            if registro == None:
                print("No se encontro lo que buscabas en la TS")
                break
        logical_offset = registro['offset']
        print("# Val Right")
        print("li $t7 {} # <- Logical offset".format(logical_offset))
        print("li $t6 4 # Num 4 is the byte_alignment")
        print("mult $t7 $t6 # Calculate physical offset")  # Calculate physical offset"
        print("mflo $t6 # <- It has the physical offset") # <- It has the physical offset

        if registro['type'] == NodeType.VAR_DECLARATION_1:
            print("subu $t6 $fp $t6")
            print("# Load the param value from stack to $t0")
            print("lw $t1 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valIzq))
        elif registro['type'] == NodeType.PARAM_1:
            print("addu $t6 $fp $t6")
            print("# Load the param value from stack to $t1")
            print("lw $t1 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valDer))
    else:
        print("li $t1 {}".format(valDer))

    if op == '+':
        if valDer == 0:
            print("#Calculate accrued sum")
            print("add $a0 $a0 $t0")
        elif valIzq == 0:
            print("#Calculate accrued sum")
            print("add $a0 $a0 $t1")
        else:
            print("#Calculate the sum")
            print("add $a0 $t0 $t1")
            
    if op == '-':
        if valDer == 0:
            print("#Calculate accrued SUB")        
            print("sub $a0 $t0 $a0")
        elif valIzq == 0:   
            print("#Calculate accrued SUB")           
            print("sub $a0 $t1 $a0")
        else:
            print("#Calculate the SUB")
            print("sub $a0 $t0 $t1")
    if op == '*':
        if valDer == 0: 
            print("#Calculate accrued MULT")             
            print("mult $a0 $t0")
            print("mflo $a0")
        elif valIzq == 0:    
            print("#Calculate accrued MULT")     
            print("mult $a0 $t1")
            print("mflo $a0")
        else:
            print("#Calculate MULT")
            print("mult $t0 $t1")
            print("mflo $a0")
    if op == '/':
        if valDer == 0:
            print("#Calculate accrued DIV")             
            print("div $t0 $a0")
            print("mflo $a0")
        elif valIzq == 0:  
            print("#Calculate accrued DIV")     
            print("div $t1 $a0")
            print("mflo $a0")
        else:
            print("#Calculate the DIV")
            print("div $t0 $t1")
            print("mflo $a0")

def caller(arbol, stack_TS, index):
    tabla_simbolos = stack_TS[index]
    print("#Caller part")
    print("#Creating a new Activation Record")
    print("sw $fp 0($sp)")#Store the Old FramePointer, at this point a new Activation Record is created
    print("addiu $sp $sp -4")
    # Save the params in a reverse manner
    list_args = []
    for arg in arbol.children: #append the args in a list
        list_args.append(arg.leaf)
    #Reverse the list
    for arg in arbol.children[::-1]:
        nombre_variable = arg.leaf
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)#Logical offset
        logical_offset = tupla['offset']
        print("li $t7 {} # Number {} represent the logical offset of variable '{}', that number is obtained by ST".format(logical_offset, logical_offset, nombre_variable))
        print("li $t6 4") #Num 4 is the byte-alignment
        print("mult $t7 $t6") # Calculate the physical offset
        print("mflo $t6") # <- it has the physical offset
        print("subu $t6 $fp $t6")
        print("lw $a0 ($t6) # # the following line is taking advantage of $fp to search the 'Y' variable") # the following line is taking advantage of $fp to search the 'Y' variable
        print("sw $a0 0($sp) # #Store param in the param section of the new Activation Record") #Store param in the param section of the new Activation Record
        print("addiu $sp $sp -4")

    #Jump to the function
    nombre_funcion = arbol.leaf
    print("jal ", nombre_funcion)


#This function returns a number that is the scope where a symbol is located
# The number could be used close to stack_TS as an index
def getIndexScope(registro):
    scope_variable = registro['scope']
    tabla_ambito_global = stack_TS[0]
    tupla = getTupla(NodeType.FUN_DECLARATION, scope_variable, tabla_ambito_global)
    index_scope = tupla['index_scope']

    return index_scope

    