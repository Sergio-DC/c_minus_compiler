from globalTypes import *
from semantica import *

index = 0
index_aux = 0
strMipsCode = ''
def codeGen(arbol, file_name):
    global index, strMipsCode
    strMipsCode = ".data\n.text\n.globl main\n"
    result = traverseTree(arbol, file_name, stack_TS, index) #El stack_TS viene del analizador semantico
    strMipsCode += "\n#Finish Program\nli $v0 10\nsyscall"
    f = open(file_name, "w")
    f.write(strMipsCode)
    print("FILE WRITTEN")

index = 0
index_aux = 0 
NAME_FUNCTION = ''
def traverseTree(arbol, file_name, stack_TS, index):
    global index_aux, NAME_FUNCTION, strMipsCode
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
            # else: # Another Procedure
            #     genCode_caller(arbol, stack_TS, index)

        if arbol.type == NodeType.RETURN_STMT_2:
            strMipsCode += "#Calculate the expression of RETURN_STMT\n"
            calculadora(arbol.children[0], stack_TS, index)            
        if arbol.type == "compound_stmt":
            tabla_simbolos = stack_TS[index]
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    traverseTree(node, file_name, stack_TS, index)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    traverseTree(arbol.children[child], file_name, stack_TS, index)
            if arbol.type == NodeType.FUN_DECLARATION:
                nombre_funcion = arbol.children[0].leaf
                tipo_retorno = arbol.leaf
                if index < len(stack_TS) - 1 and nombre_funcion != 'main': #Retorno de valor al terminar los pasos de una funcion
                    tabla_simbolos = stack_TS[index] # Segun yo esta tabla hace referencia a la del scope global
                    tupla = getTupla(NodeType.FUN_DECLARATION, nombre_funcion, tabla_simbolos)
                    index_scope = tupla['index_scope']
                    genCode_returnVal(index_scope)
#Recoradtorio: renombrar la funcion por uno mas apropiado al contexto
def genCode_updateVariable(arbol, stack_TS, index):
    global strMipsCode
    tabla_simbolos = stack_TS[index]
    nombre_variable = arbol.children[0].leaf
    tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)
    # Update the variable
    logical_offset = tupla['offset']
    comment = "#Update variable {}".format(nombre_variable)
    genCode_calculatePhysicalOffset(logical_offset, comment)
    # Search the variable 'x' using the physical offset and store the value in the stack
    strMipsCode += "# Search the variable '{}' using the physical offset and load the value from memory to register $a0\n".format(nombre_variable)
    strMipsCode += "subu $t6 $fp $t6\n"
    strMipsCode += "sw $a0 ($t6)\n"# the follwing line is taking advantage of $fp to search the 'X' variable
        

def genCode_mainFunc(arbol, stack_TS, index):
    global strMipsCode
    tabla_simbolos = stack_TS[index]
    #Obtenemos de la TS la tupla de la declaracion de main en el scope global
    tupla = getTupla(NodeType.FUN_DECLARATION, 'main', tabla_simbolos)
    #Obtenemos el index_scope
    index_scope = tupla['index_scope']
    #Buscamos en el stack_TS una tabla de simbolos que cumpla con el criterio de 'index_scopes'
    nueva_tabla_simbolos = stack_TS[index_scope] #Esa tabla contiene las variables locales declaradas dentro de main
    # Obtenemos el numero de variable declaradas en la funcion main
    N = getMatches(NodeType.VAR_DECLARATION_1, nueva_tabla_simbolos)#Representa el numero de variables declaradas localmente en la funcion main
    strMipsCode += "main:\n"
    strMipsCode += "move $fp $sp # Set FP to the bottom\n"# Set %fp to the bottom
    strMipsCode += "addiu $sp $sp -4  # Move stack_pointer to the next empty position\n"# Move stack_pointer to the next empty position
    # Store the matches of local variables in $t7
    comment = "#Reserve space for local variables"
    genCode_calculatePhysicalOffset(N, comment)
    strMipsCode += "sub $sp $sp $t6\n"

def genCode_input(arbol, stack_TS, index):
    global strMipsCode
    if arbol.children[0].type == NodeType.VAR_1:
        strMipsCode += "#Input\n"
        strMipsCode += "li $v0, 5\n"
        strMipsCode += "syscall\n"
        strMipsCode += "move $a0 $v0\n"
def genCode_output(arbol, stack_TS, index):
    global strMipsCode
    tabla_simbolos = stack_TS[index]
    strMipsCode += "\n#Print the value\n"
    # Search the variable in ST that is gonna printed 
    #Get the logical offset of the variable
    if arbol.children[0].type == NodeType.VAR_1:
        nombre_variable = arbol.children[0].leaf
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)
        logical_offset = tupla['offset']
        genCode_calculatePhysicalOffset(logical_offset, "#Dummy")
        strMipsCode += "subu $t6 $fp $t6\n"
        strMipsCode += "lw $a0 ($t6)\n"
    elif arbol.children[0].type == NodeType.CALL:
        strMipsCode += "#CALL ME\n"
        genCode_caller(arbol.children[0], stack_TS, index)
    strMipsCode += "li $v0 1\n"
    strMipsCode += "syscall\n"
    #Print a new Line
    strMipsCode += "addi $a0, $0, 0xA #ascii code for LF, if you have any trouble try 0xD for CR.\n"
    strMipsCode += "addi $v0, $0, 0xB #syscall 11 prints the lower 8 bits of $a0 as an ascii character.\n"
    strMipsCode += "syscall\n"

def genCode_calle(nombre_funcion):
    global strMipsCode
    strMipsCode += "\n #Calle Part\n"
    strMipsCode += "{}:\n".format(nombre_funcion)# The label
    strMipsCode += "move $fp $sp #move the pointer of the $fp to point to $sp\n"
    strMipsCode += "sw $ra 0($sp) #save the return address in the activation record\n"
    strMipsCode += "addiu $sp $sp -4\n"

def genCode_returnVal(index_scope):
    global strMipsCode
    strMipsCode += "\n# Return the value\n"
    tabla_simbolos = stack_TS[index_scope]
    # Load return address to register $ra
    strMipsCode += "lw $ra 4($sp) #Load return address to register $ra\n"
    # The stack-pointer will do a deep pop to restore to the pevious activation-frame top 
    #Get from the ST the count of parameters
    num_of_params = getMatches(NodeType.PARAM_1, tabla_simbolos)

    strMipsCode += "li $t0 {}  # {} represents the number of total params obtained from ST\n".format(num_of_params, num_of_params)
    strMipsCode += "#deep offset = z\n"
    strMipsCode += "li $t6 4\n"
    strMipsCode += "mult $t0 $t6  #  4 * N\n" #  4 * N
    strMipsCode += "mflo $t0\n" 
    strMipsCode += "addi $t0 $t0 8  # z = 4*n + 8\n" # z = 4*n + 8
    strMipsCode += "addu $sp $sp $t0\n"
    strMipsCode += "lw $fp 0($sp) #Restore the $fp to the old Frame pointer\n" # Restore the $fp to the old Frame pointer 
    strMipsCode += "jr $ra #Return control to caller function\n"



def genCode_caller(arbol, stack_TS, index):
    global strMipsCode
    tabla_simbolos = stack_TS[index]
    strMipsCode += "#Caller part CGEN\n"
    strMipsCode += "#Creating a new Activation Record\n"
    strMipsCode += "sw $fp 0($sp)\n"#Store the Old FramePointer, at this point a new Activation Record is created
    strMipsCode += "addiu $sp $sp -4\n"
    # Save the params in a reverse manner
    list_args = []
    for arg in arbol.children: #append the args in a list
        list_args.append(arg.leaf)
    #Reverse the list
    for arg in arbol.children[::-1]:
        if arg.type == NodeType.CALL: # If the param passed to a functio is a caller break
            break
        else:
            nombre_variable = arg.leaf
            tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)#Logical offset
            logical_offset = tupla['offset']
            genCode_calculatePhysicalOffset(logical_offset)
            genCode_loadVariableValueTo("$a0")
            strMipsCode += "sw $a0 0($sp) # #Store param in the param section of the new Activation Record\n" #Store param in the param section of the new Activation Record
            strMipsCode += "addiu $sp $sp -4\n"

    #Jump to the function
    nombre_funcion = arbol.leaf
    strMipsCode += "jal {}\n".format(nombre_funcion)

def genCode_calculatePhysicalOffset(logical_offset, comment):
    global strMipsCode
    strMipsCode += comment + "\n"
    strMipsCode += "li $t7 {} # <- Logical offset\n".format(logical_offset)
    strMipsCode += "li $t6 4 # Num 4 is the byte_alignment\n"
    strMipsCode += "mult $t7 $t6 # Calculate physical offset\n"
    strMipsCode += "mflo $t6 # <- It has the physical offset\n"

# Recibe un AST de expresiones aritmeticas y genera codigo ensamblador
def calculadora(arbol, stack_TS, index):
    global strMipsCode
    resultado = 0;
    if arbol.type == NodeType.NUMBER:
        strMipsCode += "li $a0 {}\n".format(arbol.leaf)
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
    global strMipsCode
    tabla_simbolos = stack_TS[index]

    if not isinstance(valIzq, int):
        tupla = getVariable(valIzq, tabla_simbolos)
        logical_offset = tupla['offset']
        comment = "#Val Left"
        genCode_calculatePhysicalOffset(logical_offset, comment)
        if tupla['type'] == NodeType.VAR_DECLARATION_1:
            genCode_loadVariableValueTo("$t0") #Gen code to load a value from stack to a register
        elif tupla['type'] == NodeType.PARAM_1:
            genCode_loadParamValueTo("$t0")#Gen code to load a value from stack to a register
    else:
        strMipsCode += "li $t0 {}\n".format(valIzq)

    if not isinstance(valDer, int):
        tupla = getVariable(valDer, tabla_simbolos)
        logical_offset = tupla['offset']
        comment = "# Val Right\n"
        genCode_calculatePhysicalOffset(logical_offset, comment)
        if tupla['type'] == NodeType.VAR_DECLARATION_1:
            genCode_loadVariableValueTo("$t1")
        elif tupla['type'] == NodeType.PARAM_1:
            genCode_loadParamValueTo("$t1")
    else:
        strMipsCode += "li $t1 {}\n".format(valDer)

    if op == '+':
        if valDer == 0:
            strMipsCode += "#Calculate accrued sum\n"
            strMipsCode += "add $a0 $a0 $t0\n"
        elif valIzq == 0:
            strMipsCode += "#Calculate accrued sum\n"
            strMipsCode += "add $a0 $a0 $t1\n"
        else:
            strMipsCode += "#Calculate the sum\n"
            strMipsCode += "add $a0 $t0 $t1\n"
            
    if op == '-':
        if valDer == 0:
            strMipsCode += "#Calculate accrued SUB\n"    
            strMipsCode += "sub $a0 $t0 $a0\n"
        elif valIzq == 0:   
            strMipsCode += "#Calculate accrued SUB\n"          
            strMipsCode += "sub $a0 $t1 $a0\n"
        else:
            strMipsCode += "#Calculate the SUB\n"
            strMipsCode += "sub $a0 $t0 $t1\n"
    if op == '*':
        if valDer == 0: 
            strMipsCode += "#Calculate accrued MULT\n"         
            strMipsCode += "mult $a0 $t0\n"
            strMipsCode += "mflo $a0\n"
        elif valIzq == 0:    
            strMipsCode += "#Calculate accrued MULT\n"  
            strMipsCode += "mult $a0 $t1\n"
            strMipsCode += "mflo $a0\n"
        else:
            strMipsCode += "#Calculate MULT\n"
            strMipsCode += "mult $t0 $t1\n"
            strMipsCode += "mflo $a0\n"
    if op == '/':
        if valDer == 0:
            strMipsCode += "#Calculate accrued DIV\n"            
            strMipsCode += "div $a0 $t0\n"
            strMipsCode += "mflo $a0\n"
        elif valIzq == 0:  
            strMipsCode += "#Calculate accrued DIV\n"    
            strMipsCode += "div $a0 $t1\n"
            strMipsCode += "mflo $a0\n"
        else:
            strMipsCode += "#Calculate the DIV\n"
            strMipsCode += "div $t0 $t1\n"
            strMipsCode += "mflo $a0\n"

def caller(arbol, stack_TS, index):
    global strMipsCode
    tabla_simbolos = stack_TS[index]
    strMipsCode += "#Caller part\n"
    strMipsCode += "#Creating a new Activation Record\n"
    strMipsCode += "sw $fp 0($sp)\n"#Store the Old FramePointer, at this point a new Activation Record is created
    strMipsCode += "addiu $sp $sp -4\n"
    # Save the params in a reverse manner
    list_args = []
    for arg in arbol.children: #append the args in a list
        list_args.append(arg.leaf)
    #Reverse the list
    strMipsCode += "# Save the params in a reverse manner\n"
    for arg in arbol.children[::-1]:
        nombre_variable = arg.leaf
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_simbolos)#Logical offset
        logical_offset = tupla['offset']
        genCode_calculatePhysicalOffset(logical_offset, "########")
        genCode_loadVariableValueTo("$a0")
        strMipsCode += "sw $a0 0($sp) # #Store param in the param section of the new Activation Record\n" #Store param in the param section of the new Activation Record
        strMipsCode += "addiu $sp $sp -4\n"

    #Jump to the function
    nombre_funcion = arbol.leaf
    strMipsCode += "jal {}\n".format(nombre_funcion)


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
    global strMipsCode
    strMipsCode += "# Load the value of the variable declarated from stack to {}\n".format(mips_register)
    strMipsCode += "subu $t6 $fp $t6\n"
    strMipsCode += "lw {} ($t6)\n".format(mips_register)

# The following function generates mips-code that loads a value from the stack to the register passed as param in the function
# Note: the section of memory that the assembler code generated is trying to enter is property of params    
def genCode_loadParamValueTo(mips_register):
    global strMipsCode
    strMipsCode += "# Load the param value from stack to {}\n".format(mips_register)
    strMipsCode += "addu $t6 $fp $t6\n"  
    strMipsCode += "lw {} ($t6)\n".format(mips_register)
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
