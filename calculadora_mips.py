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
        tupla = getVariable(valIzq, tabla_simbolos)
        logical_offset = tupla['offset']
        print("#Val Left")
        genCode_calculatePhysicalOffset(logical_offset)
        if tupla['type'] == NodeType.VAR_DECLARATION_1:
            genCode_loadVariableValueTo("$t0") #Gen code to load a value from stack to a register
        elif tupla['type'] == NodeType.PARAM_1:
            genCode_loadParamValueTo("$t0")#Gen code to load a value from stack to a register
    else:
        print("li $t0 {}".format(valIzq))

    if not isinstance(valDer, int):
        tupla = getVariable(valDer, tabla_simbolos)
        logical_offset = tupla['offset']
        print("# Val Right")
        genCode_calculatePhysicalOffset(logical_offset)
        if tupla['type'] == NodeType.VAR_DECLARATION_1:
            genCode_loadVariableValueTo("$t1")
        elif tupla['type'] == NodeType.PARAM_1:
            genCode_loadParamValueTo("$t1")
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
            print("div $a0 $t0")
            print("mflo $a0")
        elif valIzq == 0:  
            print("#Calculate accrued DIV")     
            print("div $a0 $t1")
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
        genCode_calculatePhysicalOffset(logical_offset)
        genCode_loadVariableValueTo("$a0")
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

# The following function generates mips-code that loads a value from the stack to the register passed as param in the function
# Note: the section of memory that the assembler code generated is trying to enter is property of local variables
def genCode_loadVariableValueTo(mips_register):
    print("# Load the value of the variable declarated from stack to {}".format(mips_register))
    print("subu $t6 $fp $t6")
    print("lw {} ($t6)".format(mips_register))

# The following function generates mips-code that loads a value from the stack to the register passed as param in the function
# Note: the section of memory that the assembler code generated is trying to enter is property of params    
def genCode_loadParamValueTo(mips_register):
    print("# Load the param value from stack to {}".format(mips_register))
    print("addu $t6 $fp $t6")   
    print("lw {} ($t6)".format(mips_register))
# This function returns a variable in a tuple format, no matters if the variable searched is a a param
# Because the function look over all the possible types of variables
def getVariable(valor, tabla_simbolos):
    while(True):
        registro = getTupla(NodeType.VAR_DECLARATION_1, valor, tabla_simbolos)
        if registro != None:
            return registro
        registro = getTupla(NodeType.PARAM_1, valor, tabla_simbolos) #Si la variable declarada no se encuentra en VAR_DECLARATION_1 se busca en PARAM_1
        if registro != None:
            return registro
        if registro == None:
            return None



