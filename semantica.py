#La estructura de la TS(Tabla de Simbolos) esta construida la siguiente forma:
# Un lista de diccionarios que tienen las siguietes claves:
# Nombre del Formato: TUPLA_TS
# {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : ''}
#

from globalTypes import *

stack_TS = [] # Stack de tabla de simbolos
tabla_global_1 = []

def tabla(tree, imprime = True):
    tabla_global = []
    declaracion_global = None

    for declaracion_global in tree.children:# Acceder al array de variables y funciones globales
        if declaracion_global.type == NodeType.VAR_DECLARATION_1: # Variables globales
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            #tabla_temp = insertar_actualizar_registros(declaracion_global, tabla_temp, 'global', fila, 'declaracion-var')
            insertarRegistro(fila, declaracion_global, 'global', NodeType.VAR_DECLARATION_1, tabla_global)
        if declaracion_global.type == NodeType.VAR_DECLARATION_2:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            #tabla_temp = insertar_actualizar_registros(declaracion_global, tabla_temp, 'global', fila, NodeType.VAR_DECLARATION_2)
        if declaracion_global.type == NodeType.FUN_DECLARATION: # Funciones Globales
            tupla_fun_decl = {'nombre': '', 'tipo_dato': '', 'valor': '', 'type' : '', 'scope': '', 'params':[],'lineno' : ''}
            # Se guardan los datos de la funcion
            tupla_fun_decl = insertarRegistro(tupla_fun_decl, declaracion_global, 'global', NodeType.FUN_DECLARATION, tabla_global)
            tabla_local = []
            #recorrido del los params de la funcion
            nombre_funcion = declaracion_global.children[0].leaf # Se guarda el nombre de la funcion, para buscar sus parametros en la siguiente funcion
            tabla_local = recorrido_params(declaracion_global.children[0], nombre_funcion, tabla_local)#Los params de la funcion son guardados en la TS
            print("Tabla Local: ", tabla_local)
            ## Se agregan solamente los tipos de datos que tiene los parametros de una función al campo 'params' de la tupla de la misma funcion
            for registro in tabla_local:
                print("Que hay aqui: {}  {}".format(registro['type'], registro['tipo_dato']))            
                if registro['type'] == NodeType.PARAM_1: 
                    tupla_fun_decl['params'].append(registro['tipo_dato'])                          
            # recorrido del cuerpo de la funcion
            tabla_local = recorrido_compound(declaracion_global.children[1], nombre_funcion, tabla_local)
            
    stack_TS.append(tabla_global)     

def recorrido_params(arbol, scope, nueva_tabla):
    if arbol.type == NodeType.PARAMS_1:#En este punto estamos sobre una declaracion de funcion e.g void suma(int x, int y)
        for node in arbol.children: # Iteramos sobre un array de params e.g abstraccion->[int x, int y] realidad -> [int--*x, int--*y]
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
            #En este punto le damos formato al nodo analizado(PARAM), el formato será: TUPLA_TS
            registro = formatearNodo(node, NodeType.PARAM_1, scope)
            val_name = registro['nombre']
            #registro = getTupla(NodeType.PARAM_1, val_name, nueva_tabla)
            #if registro != None and type != NodeType.PARAM_1: # Actualizamos simbolo
            #    actualizarRegistro(node, registro, nueva_tabla)
            #else: # Se agrega un nuevo registro a la tabla

            #if registro['tipo_dato'] != 'void':
            insertarRegistro(fila, node, scope, NodeType.PARAM_1,nueva_tabla)
    return nueva_tabla
                 

def recorrido_compound(arbol, scope, nueva_tabla):
    for i in range(len(arbol.children)):
        for node in arbol.children[i]:
            if node.type == NodeType.VAR_DECLARATION_1:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '','lineno' : ''}
                registro_local = formatearNodo(node, NodeType.VAR_DECLARATION_1, scope)
                val_name = registro_local['nombre']
                registro_global = getTupla(NodeType.VAR_DECLARATION_1, val_name, nueva_tabla)
                if registro_local != None and registro_local['scope'] != scope  : # Se manda un error: indicando que la variable ya ha sido declarada
                    print("Error: La variable ya ha sido declarada")
                else: # Se agrega un nuevo registro a la tabla
                    insertarRegistro(fila, node, scope, NodeType.VAR_DECLARATION_1,nueva_tabla)
                #insertar_actualizar_registros(node, nueva_tabla, scope, fila, NodeType.VAR_DECLARATION_1)
            elif node.type == NodeType.VAR_DECLARATION_2:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension': '', 'lineno' : ''}
                #insertar_actualizar_registros(node, nueva_tabla, scope, fila, '', NodeType.VAR_DECLARATION_2)
            elif node.type == NodeType.EXPRESSION_1:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
                var_asignacion = formatearNodo(node, NodeType.EXPRESSION_1, scope) #asignacion
                val_name = var_asignacion['nombre']
                var_declaracion = getTupla(NodeType.VAR_DECLARATION_1, val_name, nueva_tabla)#Declaracion
                if var_declaracion == None: # No se declarado una variables
                    print("Error: No se ha declarado la variable :(")
                else: # La variable si ha sido declarada
                    if not isinstance(var_asignacion['valor'], int): #Significa que la asignacion no es numero sino una expresion
                        resultado = calculoAritmeticoArbol(node.children[1], nueva_tabla)#Calculo del string de la derecha de la variable
                        var_declaracion['valor'] = resultado # Se asigna el calculo a la variable
                    else: # En este caso la asignacion es un simple numero(sin expresiones aritmeticas)
                        var_declaracion['valor'] = var_asignacion['valor']          
            elif node.type == NodeType.RETURN_STMT_2:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
                insertarRegistro(fila, node, scope, NodeType.RETURN_STMT_2,nueva_tabla)
    stack_TS.append(nueva_tabla)
    return nueva_tabla

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atributos del simbolo
def getTupla(type, val_name, tabla_simbolos):
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['type'] == type and tabla_simbolos[i]['nombre'] == val_name:
            registro = tabla_simbolos[i]
            return registro
    return None

def actualizar_TS(val_type, val_name, tabla_simbolos, valores):
    """
    Parameters:

    rol : (str) este puede ser 'variable'|'funcion'|'arreglo'

    nombre : (str) este lo da el programador a 'variable'|'funcion'|'arreglo'

    tabla_simbolos : (list) TS que sera actualizada

    valores : (list) con los que sera actualizada la TS
    """
    registro = getTupla(type, val_name, tabla_simbolos)
    for valor in valores: # Se actualiza el campo de 'params' de la funcion
        registro['params'].append(valor)

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

def insertar_actualizar_registros(node, tabla_temp, scope, fila, val_type):## Aqui esta el problema de no deteccion de variables repetidas
    registro = formatearNodo(node, val_type)
    val_name = registro['nombre']
    registro = getTupla(val_type, val_name, tabla_temp)
    if registro != None and type != NodeType.PARAM: # Actualizamos simbolo
        actualizarRegistro(node, registro, val_type)
    else: # Se agrega un nuevo registro a la tabla
        insertarRegistro(fila, node, scope, val_type,tabla_temp)                   
    return tabla_temp

def actualizarRegistro(node, registro, type):
    if type == NodeType.PARAM:
        if len(node.children) == 2:#Si la variable se usa para asignacion, obtenemos el valor guardado en la variable
            if registro['valor'] != '':
                valor_aux = registro['valor'] # Valor anterior de Y

            resultado = calculoAritmeticoArbol(node.children[1])#Calculo del string de la derecha de la variable
            registro['valor'] = resultado
    #elif type == NodeType.VAR_DECLARATION_1:

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

def typeCheck(tree):
    imprimeAST(tree, checkNode)

def imprimeAST_1(arbol, scope):
    global tabla_global_1
    if arbol != None:
        if arbol.type == NodeType.VAR_DECLARATION_1:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_1,  tabla_global_1)
        elif arbol.type == NodeType.FUN_DECLARATION:
            tupla_fun_decl = {'nombre': '', 'tipo_dato': '', 'valor': '', 'type' : '', 'scope': '', 'params':[],'lineno' : ''}
            tupla_fun_decl = insertarRegistro(tupla_fun_decl, arbol, scope, NodeType.FUN_DECLARATION, tabla_global_1)
            scope = scope + 1
        elif arbol.type == NodeType.EXPRESSION_1:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            nombre_variable = arbol.children[0].leaf
            valor = arbol.children[1].leaf
            #Buscar en TS si la variable fue declarada
            tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_global_1)
            if tupla != None:                
                tupla['valor'] = valor #Actualizamos la variable
            else:
                msgError("Variable no declarada") #Arrojamos Error
        elif arbol.type == NodeType.RETURN_STMT_2:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            nombre_variable = arbol.children[0].leaf
            #Buscar en TS si la variable fue declarada
            tupla = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, tabla_global_1)
            if tupla == None:
                msgError("Variable no declarada") #Arrojamos Error

        if arbol.type == "compound_stmt":
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                        imprimeAST_1(node, scope)
        elif arbol.children:
            for child in range(len(arbol.children),):
                if arbol.children[child] != []:
                        imprimeAST_1(arbol.children[child], scope)

def getArray():
    global tabla_global_1
    return tabla_global_1


def imprimeAST(arbol, checkNode):
    if arbol != None:
        if arbol.type == "compound_stmt":
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                        imprimeAST(node, checkNode)
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                        imprimeAST(arbol.children[child], checkNode)
            checkNode(arbol)

def checkNode(t):
    print("Type: ", t.type)
    if t.type == NodeType.VAR_DECLARATION_1:# declaracion de variable
            tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
            #print("Tipo: {}  id: {}".format(t.leaf, t.children[0].leaf))
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
            param_list_names = []
            # print("Pase")
            for registro in tabla_simbolos:
                print("registro[type]: ", registro['type'])
                if registro['type'] == NodeType.PARAM_1:
                    print("Pase :)")
                    param_list_names.append(registro['nombre'])
                    if registro['tipo_dato'] == 'void' and registro['nombre'] != '' : # Error para foo(void x)
                        print("Error:Un param es igual a void x")
            if len(param_list_names) != len(set(param_list_names)): # Devuelve true si hay nombres repetidos
                print("error: variable y is already defined in method suma")

            return_stmt = None
            for registro in tabla_simbolos:
                if registro['type'] == 'return':# Buscamos un statement de tipo RETURN
                    return_stmt = registro
                    break

            if return_stmt != None:
                if return_stmt['tipo_dato'] != t.leaf:#Se compara el retorno con el retorno de firma
                    print("Error: incompatible types: unexpected return value")
            elif return_stmt == None and t.leaf == 'int':
                print("error: missing return statement")
    elif t.type == NodeType.RETURN_STMT_2:
        print("Stack: ", stack_TS)
        tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
        
        if tabla_simbolos[0]['tipo_dato'] != t.leaf:#Se compara el lo que devueleve la fucnion con el retorno de firma
            print("Error: incompatible types: unexpected return value")
        elif return_stmt == None and t.leaf == 'int':
            print("error: missing return statement")

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

def eliminarRegistro(tabla_simbolos, val_nombre, val_type):
    #Obtener el indice del primer registro encontrado, el primer registro encontrado debe coincidir con los criterios
    registro = getTupla(val_type, val_nombre, tabla_simbolos)
    #print("registro eliminado: ", registro)
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['nombre'] == val_nombre and tabla_simbolos[i]['type'] == val_type:
            del tabla_simbolos[i]
            break


def obtenerValorReciente(tabla_simbolos, val_nombre, val_type):
    registro = getTupla(val_type, val_nombre, tabla_simbolos)

#def obtenerUltimaLineaCodigo:

def mostrarTabla():
    # print(stack_TS)
    # for tabla_simbolos in stack_TS:
    #     for item in tabla_simbolos:
    #         print("Tabla: {}".format(item['scope']), item)
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(stack_TS)))

def msgError(mensaje):
    print("Error: ", mensaje)