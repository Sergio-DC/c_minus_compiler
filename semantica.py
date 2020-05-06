#La estructura de la TS(Tabla de Simbolos) esta construida la siguiente forma:
# Un lista de diccionarios que tienen las siguietes claves:
#{'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : ''}
#

from globalTypes import *

stack_TS = [] # Stack de tabla de simbolos

def tabla(tree, imprime = True):
    tabla_temp = []
    declaracion_global = None

    for declaracion_global in tree.children:#Acceder al array de variables y funciones globales
        if declaracion_global.type == NodeType.VAR_DECLARATION_1: # Variables globales
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            #tabla_temp = insertar_actualizar_registros(declaracion_global, tabla_temp, 'global', fila, 'declaracion-var')
            insertarRegistro(fila, declaracion_global, 'global', NodeType.VAR_DECLARATION_1, tabla_temp)
        if declaracion_global.type == NodeType.VAR_DECLARATION_2:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
            tabla_temp = insertar_actualizar_registros(declaracion_global, tabla_temp, 'global', fila, NodeType.VAR_DECLARATION_2)
        if declaracion_global.type == NodeType.FUN_DECLARATION: # Funciones Globales
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params':[],'lineno' : ''}
            # Devuelve el scope que usaran las variable interiores del cuerpo
            fila = insertarRegistro(fila, declaracion_global, 'global', NodeType.FUN_DECLARATION, tabla_temp)
            nueva_tabla = []
            #recorrido del los params de la funcion
            nombre_funcion = declaracion_global.children[0].leaf
            nueva_tabla = recorrido_params(declaracion_global.children[0], nombre_funcion, nueva_tabla, insertar_actualizar_registros)
            valores = []
            for registro in nueva_tabla:              
                valores.append(registro['tipo_dato'])
            if nueva_tabla:
                actualizar_TS('funcion', fila['nombre'], tabla_temp, valores)      
            # recorrido del cuerpo de la funcion
            nueva_tabla = recorrido_compound(declaracion_global.children[1], nombre_funcion, nueva_tabla)
            
    stack_TS.append(tabla_temp)     

def recorrido_params(arbol, scope, nueva_tabla, insertar_actualizar_registros):
    if arbol.type == NodeType.PARAMS:
        for node in arbol.children:
            fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
            if insertar_actualizar_registros != None:
                insertar_actualizar_registros(node, nueva_tabla, scope, fila, NodeType.PARAMS)
    if nueva_tabla != None:
        return nueva_tabla
    else:
        return None
                 

def recorrido_compound(arbol, scope, nueva_tabla):
    #nueva_tabla = []
    for i in range(len(arbol.children)):
        for node in arbol.children[i]:
            if node.type == NodeType.VAR_DECLARATION_1:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '','lineno' : ''}
                insertar_actualizar_registros(node, nueva_tabla, scope, fila, NodeType.VAR_DECLARATION_1)
            elif node.type == NodeType.VAR_DECLARATION_2:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension': '', 'lineno' : ''}
                insertar_actualizar_registros(node, nueva_tabla, scope, fila, '', NodeType.VAR_DECLARATION_2)
            elif node.type == NodeType.EXPRESSION_1:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
                var_asignacion = obtenerMetadatos_de_registro(node, NodeType.EXPRESSION_1) #asignacion
                val_name = var_asignacion['nombre']
                var_declaracion = obtener_registro(NodeType.VAR_DECLARATION_1, val_name, nueva_tabla)#Declaracion
                if var_declaracion == None: # No se declarado una variables
                    print("Error: No se ha declarado la variable :(")
                else: # La variable si ha sido declarada
                    if not isinstance(var_asignacion['valor'], int): #Significa que la asignacion no es numero sino una expresion
                        resultado = calculoAritmeticoArbol(node.children[1])#Calculo del string de la derecha de la variable
                        var_declaracion['valor'] = resultado
                    else:
                        var_declaracion['valor'] = var_asignacion['valor']
                    
            elif node.type == NodeType.RETURN_STMT_2:
                fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
                insertarRegistro(fila, node, scope, NodeType.RETURN_STMT_2,nueva_tabla)
    stack_TS.append(nueva_tabla)

    return nueva_tabla

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atributos del simbolo
def obtener_registro(type, val_name, tabla_simbolos):
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['type'] == type and tabla_simbolos[i]['nombre'] == val_name:
            registro = tabla_simbolos[i]
            return registro
    return None

def actualizar_TS(type, val_name, tabla_simbolos, valores):
    """
    Parameters:

    rol : (str) este puede ser 'variable'|'funcion'|'arreglo'

    nombre : (str) este lo da el programador a 'variable'|'funcion'|'arreglo'

    tabla_simbolos : (list) TS que sera actualizada

    valores : (list) con los que sera actualizada la TS
    """
    registro = obtener_registro(type, val_name, tabla_simbolos)
    for valor in valores: # Se actualiza el campo de 'params' de la funcion
        registro['params'].append(valor)

def preOrder(arbol, resultado):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            return arbol.leaf
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado)
        resultado = operacion(arbol.leaf, hijoLeft, hijoDer)
    return resultado

# Recibe un ast de expresiones aritmeticas y devuelve el resultado del calculo
def calculoAritmeticoArbol(arbol):
    resultado = 0;    
    resultado = preOrder(arbol, resultado)
    return resultado


def operacion(op, valIzq, valDer):
    resultado = None
    # if not isinstance(valIzq, int):
    #     registro = obtener_registro(NodeType.EXPRESSION_1, valIzq)
    #     valIzq = registro['valor']#Reasignamos un valor de tipo INT
    # if not isinstance(valDer, int):
    #     registro = obtener_registro(NodeType.EXPRESSION_1. valDer)
    #     valDer = registro['valor']#Reasignamos un valor de tipo INT
    
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
    registro = obtenerMetadatos_de_registro(node, val_type)
    val_name = registro['nombre']
    registro = obtener_registro(val_type, val_name, tabla_temp)
    if registro != None and type != NodeType.PARAMS: # Actualizamos simbolo
        actualizarRegistro(node, registro, val_type)
    else: # Se agrega un nuevo registro a la tabla
        insertarRegistro(fila, node, scope, val_type,tabla_temp)                   
    return tabla_temp

def actualizarRegistro(node, registro, type):
    if type == NodeType.PARAMS:
        if len(node.children) == 2:#Si la variable se usa para asignacion, obtenemos el valor guardado en la variable
            if registro['valor'] != '':
                valor_aux = registro['valor'] # Valor anterior de Y

            resultado = calculoAritmeticoArbol(node.children[1])#Calculo del string de la derecha de la variable
            registro['valor'] = resultado
    #elif type == NodeType.VAR_DECLARATION_1:

#Se inserta Funcion a la tabla de Simbolos
def insertarRegistro(fila, node, scope, type,  tabla_temp):
    registro = obtenerMetadatos_de_registro(node, type)
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

def imprimeAST(arbol, checkNode):
    if arbol != None:
        if arbol.type == "compound_stmt":
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                        #print("arbol.type: ", node.type)
                        imprimeAST(node, checkNode)
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                        imprimeAST(arbol.children[child], checkNode)
            checkNode(arbol)
            #print(arbol.leaf)

def checkNode(t):
    #print("Type: ", t.type)

    if t.type == NodeType.VAR_DECLARATION_1:# declaracion de variable
            tabla_simbolos = stack_TS[1] #TS Global
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
            for registro in tabla_simbolos:
                if registro['type'] == 'params':
                    param_list_names.append(registro['nombre'])
                    if 'void' == registro['tipo_dato'] and registro['nombre'] != 'void': # Error para foo(void x)
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
    elif t.type == NodeType.EXPRESSION_1:
        #Buscamos en el scope actual la declaracion de la variable
        tabla_simbolos = stack_TS[0]
        for registro in tabla_simbolos:
            registro_aux = obtenerMetadatos_de_registro(t, NodeType.VAR_DECLARATION_1)
            if registro['nombre'] == registro_aux['nombre'] and registro['type'] == NodeType.VAR_DECLARATION_1:
                #Quitamos de la tabla de simbolos los registros repetidos y nos quedamos con uno
                eliminarRegistro(tabla_simbolos, registro['nombre'], NodeType.EXPRESSION_1)
            else:
                print("La variable no ha sido declarada")

def nombreRepetido(val_name, tabla_simbolos):
    registros = []
    for item in tabla_simbolos:
        if item['nombre'] == val_name:
            registros.append(item)
    return True if len(registros) > 1 else False

def typeError(t, message):
    print("Type error at line", t.lineno, ":",message)
    Error = True
#Podriamos mejorar esta funcion para que recupere metadatos de un Nodo o de un Registro (Ts)
def obtenerMetadatos_de_registro(node, type):
    if type == NodeType.VAR_DECLARATION_1 or type == NodeType.FUN_DECLARATION:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_valor = ''
        val_type = NodeType.VAR_DECLARATION_1
        val_scope = ''
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
    elif type == NodeType.PARAMS:
        try:
            val_nombre = node.children[0].leaf # Si el param tiene esta forma foo(int x)
        except IndexError:
            val_nombre = node.leaf # Si el param tiene esta forma foo(void)
        val_tipo_dato = node.leaf
        val_valor = ''
        val_type = NodeType.PARAMS
        val_scope = ''
        val_dimension = "1"
        val_lineno = node.lineno
    else: # return
        val_nombre = node.children[0].leaf
        if isinstance(val_nombre, int):
            val_tipo_dato = 'int'
        else:
            val_tipo_dato = 'undefined'
        val_valor = ''
        val_type = ''
        val_scope = ''
        val_dimension = "1"
        val_lineno = node.lineno

    return {'nombre':val_nombre, 'tipo_dato':val_tipo_dato, 'valor':val_valor, 'type': val_type , 'scope': val_scope, 'dimension': val_dimension, 'lineno' : val_lineno}

def eliminarRegistro(tabla_simbolos, val_nombre, val_type):
    #Obtener el indice del primer registro encontrado, el primer registro encontrado debe coincidir con los criterios
    registro = obtener_registro(val_type, val_nombre, tabla_simbolos)
    print("registro eliminado: ", registro)
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['nombre'] == val_nombre and tabla_simbolos[i]['type'] == val_type:
            del tabla_simbolos[i]
            break


def obtenerValorReciente(tabla_simbolos, val_nombre, val_type):
    registro = obtener_registro(val_type, val_nombre, tabla_simbolos)

#def obtenerUltimaLineaCodigo:

def mostrarTabla():
    for tabla_simbolos in stack_TS:
        for item in tabla_simbolos:
            print("Tabla: {}".format(item['scope']), item)