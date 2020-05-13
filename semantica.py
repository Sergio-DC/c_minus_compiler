#La estructura de la TS(Tabla de Simbolos) esta construida la siguiente forma:
# Un lista de diccionarios que tienen las siguietes claves:
# Nombre del Formato: TUPLA_TS
# {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : ''}
#

from globalTypes import *

#stack_TS = [] # Stack de tabla de simbolos
tabla_global_1 = []

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atributos del simbolo
def getTupla(type, val_name, tabla_simbolos):
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['type'] == type and tabla_simbolos[i]['nombre'] == val_name:
            registro = tabla_simbolos[i]
            return registro
    return None

def preOrder(arbol, resultado, tabla_simbolos):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            return arbol.leaf
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado, tabla_simbolos)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado, tabla_simbolos)
        resultado = operacion(arbol.leaf, hijoLeft, hijoDer, tabla_simbolos)
    return resultado

# Recibe un ast de expresiones aritmeticas y devuelve el resultado del calculo
#La TS la ocupamos cuando la expresion esta compuesta por literales, en este caso recurrimos a la TS para localizar el valors
def calculoAritmeticoArbol(arbol, tabla_simbolos):
    resultado = 0;    
    resultado = preOrder(arbol, resultado , tabla_simbolos)
    return resultado


def operacion(op, valIzq, valDer, tabla_simbolos):
    resultado = None
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

#Se inserta Funcion a la tabla de Simbolos
def insertarRegistro(fila, node, scope, type,  tabla_temp):
    registro = formatearNodo(node, type, scope)
    fila['nombre'] = registro['nombre']
    fila['tipo_dato'] = registro['tipo_dato']
    fila['valor'] = registro['valor']
    fila['type'] = type
    fila['scope'] = scope
    fila['dimension'] = registro['dimension']
    fila['lineno'] = registro['lineno']
    tabla_temp.append(fila)

    return fila

scope = 'global'
YaPase = False
def crearTabla(arbol, table, stack_TS):
    global scope, YaPase
    # print("Ora: ", arbol.type)
    if arbol.type == NodeType.VAR_DECLARATION_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        tupla_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable fue declarada
        if tupla_1 == None and tupla_2 == None:
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_1,  table)
        else:
            msgError("Variable Repetida")
    elif arbol.type == NodeType.VAR_DECLARATION_2: # Declaracion de variable de tipo array []
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        tamano = arbol.children[1].leaf
        tupla_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable fue declarada
        if tupla_1 == None and tupla_2 == None:            
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_2, table)
        else:
            msgError("Variable Repetida")
    elif arbol.type == NodeType.FUN_DECLARATION:
        tupla_fun_decl = {'nombre': '', 'tipo_dato': '', 'valor': '', 'type' : '', 'scope': '', 'params':[],'lineno' : ''}
        tupla_fun_decl = insertarRegistro(tupla_fun_decl, arbol, scope, NodeType.FUN_DECLARATION, table)
        scope = tupla_fun_decl['nombre']
        if not YaPase:
            stack_TS.append(table)
        YaPase = True
        # table = []
    elif arbol.type == NodeType.EXPRESSION_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        valor = arbol.children[1].leaf
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table) #Buscar en TS si la variable fue declarada
        if tupla != None:                
            tupla['valor'] = valor #Actualizamos la variable
        else:
            msgError("Variable no declarada") #Arrojamos Error
    elif arbol.type == NodeType.RETURN_STMT_2:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        #Buscar en TS si la variable fue declarada
        tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)
        if tupla == None:
            msgError("Variable no declarada") #Arrojamos Error
    elif arbol.type == NodeType.PARAMS_1:
        try:
            lista_params = arbol.children[0]
            #print("lista_params: ", lista_params)
        except IndexError:
            print("Syntax Error: Is missing void")
            exit()
    elif arbol.type == NodeType.PARAM_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        tipo_dato = arbol.leaf
        nombre_variable = arbol.children[0].leaf
        print("Nom Var: ", nombre_variable)
        if tipo_dato == 'void':
            msgError("Tipo de dato Invalido")# No pueden exitir params con tipo de dato void, se arroja Error
            exit()
        else:
            registro = insertarRegistro(fila, arbol, scope, NodeType.PARAM_1,table)# Se agregan los parametros a la tabla local
            #Agregar tipos de datos a la declaracion de la funcion
            table_bottom = stack_TS[0] #Obtener referencia de la tabla del fondo (Contexto Global)
            tupla = getTupla(NodeType.FUN_DECLARATION, scope, stack_TS[0])#Obtenemos a refencia a la funcion que contiene los PARAMS
            tupla['params'].append(arbol.leaf)#Actualizamos el campo de PARAM de la declaracion de funcion

    if arbol != None:
        if arbol.type == "compound_stmt":
           
            table = []
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    crearTabla(node, table, stack_TS)
            stack_TS.append(table)
            scope = 'global'
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    crearTabla(arbol.children[child], table, stack_TS)
    return stack_TS

index = 0
def typeCheck(tree, stack, index_):
    global index 
    index = index_
    imprimeAST(tree, checkNode, stack, index)

def imprimeAST(arbol, checkNode, stack, index):
    if arbol != None:
        if arbol.type == "compound_stmt":
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    imprimeAST(node, checkNode, stack, index)
            index = index - 1
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    imprimeAST(arbol.children[child], checkNode, stack, index)
            checkNode(arbol, stack, index)

def checkNode(t, stack_TS, index):
    print("Type: {}  Index: {}  Val: {}".format(t.type, index, t.leaf))
    if t.type == NodeType.VAR_DECLARATION_1:# declaracion de variable
            tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
            if (t.leaf != 'int'): # la declaracion de una varible debe ser INT
                typeError(t,"Error: El tipo debe ser INT")
            elif nombreRepetido(t.children[0].leaf, tabla_simbolos) == True: #El nombre de la variable no debe repetirse
                typeError(t,"Error: variable {} is already defined".format(t.children[0].leaf))
                #exit()
    elif t.type == NodeType.FUN_DECLARATION:
            #Buscamos en la TS un RETURN, si este tiene valor INT y el retorno es VOID arrojamos ERROR
            #Buscamos en la TS un RETURN, si no hay y el retorno es INT arrojamos ERROR
            tabla_simbolos = stack_TS[0]#TS local
            #Obtener params a nivel local
            # param_list_names = []
            # # print("Pase")
            # for registro in tabla_simbolos:
            #     if registro['type'] == NodeType.PARAM_1:
            #         print("Pase :)")
            #         param_list_names.append(registro['nombre'])
            #         if registro['tipo_dato'] == 'void' and registro['nombre'] != '' : # Error para foo(void x)
            #             print("Error:Un param es igual a void x")
            # if len(param_list_names) != len(set(param_list_names)): # Devuelve true si hay nombres repetidos
            #     print("error: variable y is already defined in method suma")

            # return_stmt = None
            # for registro in tabla_simbolos:
            #     if registro['type'] == 'return':# Buscamos un statement de tipo RETURN
            #         return_stmt = registro
            #         break

            # if return_stmt != None:
            #     if return_stmt['tipo_dato'] != t.leaf:#Se compara el retorno con el retorno de firma
            #         print("Error: incompatible types: unexpected return value")
            # elif return_stmt == None and t.leaf == 'int':
            #     print("error: missing return statement")
    elif t.type == NodeType.RETURN_STMT_2:
        #print("Stack: ", stack_TS)
        tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
        
        
        return_variable = t.children[0].leaf
        tupla_return = getTupla(NodeType.VAR_DECLARATION_1, return_variable, tabla_simbolos)
        print("tupla_retrun: ", tabla_simbolos)
        #tupla_func = getTupla(NodeType.FUN_DECLARATION, tupla_return['scope'], )
        
        #if tupla['tipo_dato'] == 
        print("que hay: ", return_variable)
        #if return_value 

        # if tabla_simbolos[0]['tipo_dato'] != t.leaf:#Se compara lo que devueleve la fucnion con el retorno de firma
        #     print("Error: incompatible types: unexpected return value")
        # elif return_stmt == None and t.leaf == 'int':
        #     print("error: missing return statement")

def nombreRepetido(val_name, tabla_simbolos):
    registros = []
    for item in tabla_simbolos:
        if item['nombre'] == val_name and item['scope'] != 'global':
            registros.append(item)
    return True if len(registros) > 1 else False

def typeError(t, message):
    print("Type error at line", t.lineno, ":",message)
    Error = True
#Podriamos mejorar esta funcion para que recupere metadatos de un Nodo o de un Registro (Ts)
def formatearNodo(node, type, scope):
    if type == NodeType.FUN_DECLARATION:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_type = type == NodeType.FUN_DECLARATION
        val_valor = ''
        val_scope = 'global'
        val_dimension = "1"
        val_lineno = node.lineno
    elif type == NodeType.VAR_DECLARATION_1:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_valor = ''
        val_type = NodeType.VAR_DECLARATION_1
        val_scope = scope
        val_dimension = "1"
        val_lineno = node.lineno
    elif type == NodeType.VAR_DECLARATION_2:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_valor = ''
        val_type = 'fun_declaration'
        val_scope = ''
        val_dimension = node.children[1].leaf
        val_lineno = node.lineno
    elif type == NodeType.EXPRESSION_1:
        val_nombre = node.children[0].leaf
        val_tipo_dato = '' #Tipo lo omitimos por que lo desconocemos
        val_valor = node.children[1].leaf
        val_type = NodeType.EXPRESSION_1
        val_scope = ''
        val_dimension = "1"
        val_lineno = node.lineno
    elif type == NodeType.PARAM_1:
        try:
            val_nombre = node.children[0].leaf # Si el param tiene esta forma foo(int x)
        except IndexError:
            val_nombre = node.leaf # Si el param tiene esta forma foo(void)
        val_tipo_dato = node.leaf
        val_valor = ''
        val_type = NodeType.PARAM_1
        val_scope = ''
        val_dimension = "1"
        val_lineno = node.lineno
    elif type == NodeType.RETURN_STMT_2:
        
        if isinstance(node.children[0].leaf, int): # Si return esta acompañado de un numero, poner el numero en el campo de 'valor'
            val_valor = node.children[0].leaf
            val_nombre = ''
        else:
            val_nombre = node.children[0].leaf
            val_valor = ''
        
        if isinstance(val_nombre, int) or isinstance(val_valor, int): #Si el valor devuelto por la funcion es de tipo INT se actualiza TS
            val_tipo_dato = 'int'   
        else:
            val_tipo_dato = 'undefined'
        val_type = ''
        val_scope = ''
        val_dimension = "1"
        val_lineno = 5

    return {'nombre':val_nombre, 'tipo_dato':val_tipo_dato, 'valor':val_valor, 'type': val_type , 'scope': val_scope, 'dimension': val_dimension, 'lineno' : val_lineno}

def mostrarTabla():
    # print(stack_TS)
    # for tabla_simbolos in stack_TS:
    #     for item in tabla_simbolos:
    #         print("Tabla: {}".format(item['scope']), item)
    print('\n\n'.join('{}: {}'.format(*k) for k in enumerate(stack_TS)))

def msgError(mensaje):
    print("Error: ", mensaje)