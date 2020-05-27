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
            if arbol.type == NodeType.NUMBER:
                print("li $a0 {}".format(arbol.leaf))
                return None
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
        registro = getTupla(NodeType.VAR_DECLARATION_1, valIzq, tabla_simbolos)
        registro = getTupla(NodeType.PARAM_1, valIzq, tabla_simbolos) #Si la variable declarada no se encuentra en VAR_DECLARATION_1 se busca en PARAM_1
        logical_offset = registro['offset']
        print("#Val Left")
        print("li $t7 {} # <- Logical offset".format(logical_offset))
        print("li $t6 4 # Num 4 is the byte_alignment")
        print("mult $t7 $t6 # Calculate physical offset")  # Calculate physical offset"
        print("mflo $t6 # <- It has the physical offset") # <- It has the physical offset

        print("# Load the param value from stack to $t0")
        print("addu $t6 $fp $t6")
        print("lw $t0 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valIzq))
    if not isinstance(valDer, int):
        registro = getTupla(NodeType.VAR_DECLARATION_1, valDer, tabla_simbolos)
        registro = getTupla(NodeType.PARAM_1, valDer, tabla_simbolos) #Si la variable declarada no se encuentra en VAR_DECLARATION_1 se busca en PARAM_1
        logical_offset = registro['offset']
        print("# Val Right")
        print("li $t7 {} # <- Logical offset".format(logical_offset))
        print("li $t6 4 # Num 4 is the byte_alignment")
        print("mult $t7 $t6 # Calculate physical offset")  # Calculate physical offset"
        print("mflo $t6 # <- It has the physical offset") # <- It has the physical offset

        print("# Load the param value from stack to $t0")
        print("addu $t6 $fp $t6")
        print("lw $t1 ($t6) #This line takes advantage of $fp as pivot to search for '{}' param".format(valDer))

    if op == '+':
        if valDer == 0:
            # Val Right
            # # Search in ST the offset of valDer
            # li $t7 ñ ## Num ñ represent the logical_offset of 'x' variable
            # # Calculate physical offset
            # mult $t7 4  # Num 4 is the byte_alignment
            # mflo $t6 # <- It has the physical offset
            # # Load the param value from stack to $t1
            # lw $t1 $t6($fp) #This line takes advantage of $fp as pivot to search for 'x' param
            # add $a0 $a0 $t1
            print("li $a0 {}".format(valIzq))
            print("lw $t1 4($sp)")         
            print("add $a0 $a0 $t1")
            print("sw $a0 4($sp)")
        elif valIzq == 0:
            # Val Left
            # # Search in ST the offset of valIzq
            # li $t7 2 ## Num 2 represent the logical_offset of 'y' variable
            # # Calculate physical offset
            # mult $t7 4  # Num 4 is the byte_alignment
            # mflo $t6 # <- It has the physical offset
            # # Load the param value from stack to $t0
            # lw $t0 $t6($fp) #This line takes advantage of $fp as pivot to search for 'y' param 
            # # Calculate the Sum
            # add $a0 $a0 $t0
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")         
            print("add $a0 $a0 $t1")
            print("sw $a0 4($sp)")
        else:
            print("#Calculate the sum")
            print("add $a0 $t0 $t1")
            
    if op == '-':
        if valDer == 0:
            print("li $a0 {}".format(valIzq))
            print("lw $t1 4($sp)")         
            print("sub $a0 $t1 $a0")
            print("sw $a0 4($sp)")
        elif valIzq == 0:
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")         
            print("sub $a0 $t1 $a0")
            print("sw $a0 4($sp)")
        else:
            print("li $a0 {}".format(valIzq))
            print("sw $a0 0($sp)")
            print("addiu $sp $sp -4")
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")
            print("sub $a0 $t1 $a0")
            print("sw $a0 4($sp)")
    if op == '*':
        if valDer == 0:
            print("li $a0 {}".format(valIzq))
            print("lw $t1 4($sp)")         
            print("mult $a0 $t1")
            print("mflo $a0")
            print("sw $a0 4($sp)")
        elif valIzq == 0:
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")         
            print("mult $a0 $t1")
            print("mflo $a0")
            print("sw $a0 4($sp)")
        else:
            print("li $a0 {}".format(valIzq)) 
            print("sw $a0 0($sp)")
            print("addiu $sp $sp -4")
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")
            print("mult $a0 $t1")
            print("mflo $a0")
            print("sw $a0 4($sp)")
    if op == '/':
        if valDer == 0:
            print("li $a0 {}".format(valIzq))
            print("lw $t1 4($sp)")         
            print("div $t1 $a0")
            print("mflo $a0")
            print("sw $a0 4($sp)")
        elif valIzq == 0:
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")         
            print("div $t1 $a0")
            print("mflo $a0")
            print("sw $a0 4($sp)")
        else:
            print("li $a0 {}".format(valIzq)) 
            print("sw $a0 0($sp)")
            print("addiu $sp $sp -4")
            print("li $a0 {}".format(valDer))
            print("lw $t1 4($sp)")
            print("div $t1 $a0")
            print("mflo $a0")
            print("sw $a0 4($sp)")

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

    