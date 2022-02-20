#La estructura de la TS(Tabla de Simbolos) esta construida la siguiente forma:
# Un lista de diccionarios que tienen las siguietes claves:
# Nombre del Formato: TUPLA_TS
# {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : ''}
#

from enum import Flag
from Parser import Node, setParserDebugMode
from globalTypes import *
semanticsDebugMode = False

stack_TS = [] # Stack de tabla de simbolos
tabla_global_1 = []
showTableEnabled = False
test_output = []
errorMessagesFlag = False

#Cuenta el numero de coincidencias de algun NodeType (Fue creada con el proposito de contar las variables declaradas en una funcion) 
def getMatches(type,tabla_simbolos):
    matches = 0
    for tupla in tabla_simbolos:
        if type == tupla['type']:
            matches = matches + 1
    return matches

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atributos del simbolo
def getTupla(type, val_name, tabla_simbolos):
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['type'] == type and tabla_simbolos[i]['nombre'] == val_name:
            registro = tabla_simbolos[i]
            return registro
    return None

def updateTupla(type, name, clave, nuevo_valor, tabla_simbolos):
    tupla = getTupla(type, name, tabla_simbolos)
    if tupla != None:
        tupla[clave] = nuevo_valor
        return 0
    else:
        return -1

def preOrder(arbol, resultado, tabla_simbolos):
    if arbol != None:
        # print("arbol leaf: {}  {}".format(arbol.leaf, arbol.children))
        if str(arbol.leaf) not in '+-*/':
            return arbol
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado, tabla_simbolos)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado, tabla_simbolos)
        #resultado = operacion(arbol.leaf, hijoLeft, hijoDer, tabla_simbolos)
        #print("L: {}  R: {}". format(hijoLeft, hijoDer))
        typeCheckArithmetic(arbol.leaf, hijoLeft, hijoDer, tabla_simbolos)
    #return resultado


def typeCheckArithmetic(op, valIzq, valDer, tabla_simbolos):
    resultado = None
    #print("valIzq: ", valIzq)
    #print("valDer: ", valDer)

    tipo_dato_call_izq = None
    tipo_dato_call_der = None
    # ]print("{}  {}   {}".format(op ,valIzq, valDer.leaf))

    try:
        if valIzq.type == NodeType.CALL:
            nombre_call_izq = valIzq.leaf
            tupla_func_izq = getTupla(NodeType.FUN_DECLARATION, nombre_call_izq, tabla_simbolos)
            tipo_dato_call_izq = tupla_func_izq['tipo_dato']
    except AttributeError:
        tipo_dato_call_izq = None

    try:
        if valDer.type == NodeType.CALL:
            nombre_call_der = valDer.leaf
            tupla_func_der = getTupla(NodeType.FUN_DECLARATION, nombre_call_der, tabla_simbolos)
            tipo_dato_call_der = tupla_func_der['tipo_dato']
    except AttributeError:
        tipo_dato_call_der = None

    if tipo_dato_call_izq != None:
        if tipo_dato_call_izq != 'int':
            msgError("en el tipo de la expresion: IZQ {}".format(nombre_call_izq), valIzq.lineno)
    
    if tipo_dato_call_der != None:
        if tipo_dato_call_der != 'int':
            msgError("en el tipo de la expresion DER {}".format(nombre_call_der), valDer.lineno)

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
paramsIngresadosLocalmente = False
seHaPregargado = False
offset = 1
index_scope = 1 #Etiqueta las scopes de las declaraciones de funciones entradas, se incementa en 1 despues de haber asigando el scope_index a la funcion declarada
def crearTabla(arbol, table, stack_TS, tabla_params):
    global scope, YaPase, seHaPregargado, paramsIngresadosLocalmente, offset, index_scope, semanticsDebugMode
    if arbol.type == NodeType.VAR_DECLARATION_1:
        if semanticsDebugMode == True:
            print("[log] init node:" + NodeType.VAR_DECLARATION_1.name)
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params' : '--', 'lineno' : '', 'offset' : offset, 'index_scope' : '--'}
        nombre_variable = arbol.children[0].leaf
        offset += 1
        #Insertar Parametros de la función en el scope local, solo si 
        if tabla_params != [] and paramsIngresadosLocalmente == False:
            for tupla_param in tabla_params[::-1]:
                table.insert(0,tupla_param)
            paramsIngresadosLocalmente = True

        #Busqueda en TS
        tupla_var_decl_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable tipo 1 fue declarada
        tupla_var_decl_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable tipo 2 fue declarada
        tupla_param_1 = getTupla(NodeType.PARAM_1, nombre_variable, table) # Buscar en TS si el param tipo 1 fue declarado
        tupla_param_2 = getTupla(NodeType.PARAM_2, nombre_variable, table) # Buscar en TS si el param tipo 2 fue declarado

        #Si el nombre de la variable no esta repetido se puede agregar a la TS
        if tupla_var_decl_1 == None and tupla_var_decl_2 == None and  tupla_param_1 == None and tupla_param_2 == None:
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_1,  table)   
        else:
            msgError("Variable Repetida", arbol.lineno)
    elif arbol.type == NodeType.VAR_DECLARATION_2: # Declaracion de variable de tipo array []
        if semanticsDebugMode:
            print("[log] init node:", NodeType.VAR_DECLARATION_2.name)
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params' : '--', 'lineno' : '', 'offset' : offset, 'index_scope' : '--'}
        nombre_variable = arbol.children[0].leaf
        offset += 1

        #Insertar Parametros de la función en el scope local
        if tabla_params != [] and paramsIngresadosLocalmente == False:
            for tupla_param in tabla_params[::-1]:
                table.insert(0,tupla_param)
            paramsIngresadosLocalmente = True
        tamano = arbol.children[1].leaf
        #Se busca en la TS el nombre de la variable
        tupla_var_decl_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_var_decl_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_param_1 = getTupla(NodeType.PARAM_1, nombre_variable, table) # Buscar en TS si el param tipo 1 fue declarado
        tupla_param_2 = getTupla(NodeType.PARAM_2, nombre_variable, table) # Buscar en TS si el param tipo 2 fue declarado

        if tupla_var_decl_1 == None and tupla_var_decl_2 == None and tupla_param_1 == None and tupla_param_2 == None:            
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_2, table)
        else:
            msgError("Variable Repetida", arbol.lineno)
    elif arbol.type == NodeType.FUN_DECLARATION:
        if semanticsDebugMode == True:
            print("[log] init node:", NodeType.FUN_DECLARATION.name, "stack_TS:", stack_TS)
        offset = 1
        #Precargamos TS con input() y output()
        if not seHaPregargado:
            fila = {'nombre': 'input', 'tipo_dato': 'int', 'valor': '', 'type' : NodeType.FUN_DECLARATION, 'scope': 'global', 'params':[],'return': '', 'lineno' : '', 'offset' : '--', 'index_scope' : '--'}
            table.append(fila)
            fila = {'nombre': 'output', 'tipo_dato': 'void', 'valor': '', 'type' : NodeType.FUN_DECLARATION, 'scope': 'global', 'params':['int'],'return': '', 'lineno' : '', 'offset' : '--', 'index_scope' : '--'}
            table.append(fila)
            seHaPregargado = True
        tabla_params.clear()
        paramsIngresadosLocalmente = False

        nombre_func = arbol.children[0].leaf
        fila = {'nombre': '', 'tipo_dato': '', 'valor': '', 'type' : '', 'scope': '', 'params':[],'return': '', 'lineno' : '', 'offset' : '--', 'index_scope' : index_scope}
        index_scope = index_scope + 1
        tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, table)

        if tupla_func_decl == None:        
            if semanticsDebugMode == True:
                print("[log] node:", NodeType.FUN_DECLARATION.name, " method:insertarRegistro()")
            tupla_func_decl = insertarRegistro(fila, arbol, scope, NodeType.FUN_DECLARATION, table)
            scope = tupla_func_decl['nombre'] # Esta variable es critica para que las variables declaradas localmente tengan el scope correcto
        else:
            msgError("Función Repetida", arbol.lineno)
        
        if not YaPase:
            stack_TS.append(table)
        YaPase = True
    elif arbol.type == NodeType.EXPRESSION_1:
        if semanticsDebugMode == True:
            print("[log] init node:", NodeType.EXPRESSION_1.name)
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params' : '--', 'lineno' : '', 'index_scope' : '--'}
        nombre_variable = arbol.children[0].leaf#Variable a la que se le asigna el valor
        node_valor = arbol.children[1]# Nodo que tiene Valor que sera asignado/Expresion

        tupla_var_decl_1_global = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, stack_TS[0])
        tupla_var_decl_2_global = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, stack_TS[0])
        tupla_var_decl_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table) #Buscar en TS local si la variable fue declarada dentro del cuerpo
        tupla_var_decl_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table) #Buscar en TS local si la variable fue declarada dentro del cuerpo
        tupla_param_1 = getTupla(NodeType.PARAM_1, nombre_variable, table) #Buscar en la TS local si un param tipo1 fue declarado
        tupla_param_2 = getTupla(NodeType.PARAM_2, nombre_variable, table) # Buscar en la TS local si un param tipo 2 fue declarado

        if tupla_var_decl_1_global == None and tupla_var_decl_2_global == None and tupla_var_decl_1 == None and tupla_var_decl_2 == None and tupla_param_1 == None and tupla_param_2 == None:
            msgError("Variable no declarada 1.5", arbol.lineno)
        else:
            if(node_valor.type == NodeType.NUMBER): # Si el valor de la derecha es una simple constante, se agrega a la TS
                if tupla_var_decl_1_global:
                    tupla_var_decl_1_global['valor'] = node_valor.leaf
                elif tupla_var_decl_2_global:
                    print("En construccion")
                elif tupla_var_decl_1:
                    tupla_var_decl_1['valor'] = node_valor.leaf
                elif tupla_var_decl_2:
                    print("En construccion") 
                elif tupla_param_1:
                    print("En construccion")   
                elif tupla_param_2:
                    print("En construccion") 
    elif arbol.type == NodeType.RETURN_STMT_2:
        if semanticsDebugMode == True:
            print("[log] init node:", NodeType.RETURN_STMT_2.name)
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params' : '--', 'lineno' : '', 'offset' : '--', 'index_scope' : '--'}
        valueToReturn = arbol.children[0].leaf
        #Insertar Parametros de la función en el scope local, solo si 
        if tabla_params != [] and paramsIngresadosLocalmente == False:
            for tupla_param in tabla_params[::-1]:
                table.insert(0,tupla_param)
            paramsIngresadosLocalmente = True
        
        if isinstance(valueToReturn, int):
            numberNode = Node(NodeType.NUMBER, None, valueToReturn, arbol.lineno)
            #REMINDER to know the reason the last param is stack_TS[0], place a breakpoint here and debug
            if semanticsDebugMode == True:  
                print("[log] node:", NodeType.RETURN_STMT_2.name, " method:insertarRegistro()")
            insertarRegistro(fila, numberNode, scope, NodeType.NUMBER, stack_TS[0])#TODO figure out whats the table you have to use
            func_decl = getTupla(NodeType.FUN_DECLARATION, scope, tabla_simbolos=stack_TS[0])
            func_decl['return'] = 'int'
        else:
            #Buscar en TS si la variable fue declarada
            #FIXME change the last param 'table' to 'stack_TS' because it doesn't have any value
            tupla_var_decl_1 = getTupla(NodeType.VAR_DECLARATION_1, valueToReturn, table)# Buscar en TS si existe declaracion de varible tipo 1
            tupla_var_decl_2 = getTupla(NodeType.VAR_DECLARATION_2, valueToReturn, table)# Buscar en TS si existe declaracion de varible tipo 2
            tupla_param_1 = getTupla(NodeType.PARAM_1, valueToReturn, table)# Buscar en TS si existe declaracion de parametros tipo 1
            tupla_param_2 = getTupla(NodeType.PARAM_2, valueToReturn, table)# Buscar en TS si existe declaracion de parametros tipo 2
            if semanticsDebugMode == True: 
                print("[log] node:", NodeType.RETURN_STMT_2.name, " method:alternativa")
            tabla_simbolos_global = stack_TS[0]
            if tupla_var_decl_1 == None and tupla_param_1 == None and tupla_var_decl_2 == None and tupla_param_2 == None:
                test_output.append("Error variable no declarada 2")
                msgError("variable no declarada 2", arbol.lineno) #Arrojamos Error
            elif tupla_var_decl_1 != None: #Se guarda el tipo de retorno en la declaracion de la funcion para variable tipo 1           
                nombre_func = tupla_var_decl_1['scope']
                tipo_dato_var = tupla_var_decl_1['tipo_dato']
                tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
                tupla_func_decl['return'] = tipo_dato_var
            elif tupla_var_decl_2 != None: #Se guarda el tipo de retorno en la declaracion de la funcion para variable tipo 2
                nombre_func = tupla_var_decl_2['scope']
                tipo_dato_var = tupla_var_decl_2['tipo_dato']
                tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
                tupla_func_decl['return'] = tipo_dato_var
            elif tupla_param_1 != None: #Se guarda el tipo de retorno en la declaracion de la funcion para parametro tipo 1
                nombre_func = tupla_param_1['scope']
                tipo_dato_var = tupla_param_1['tipo_dato']
                tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
                tupla_func_decl['return'] = tipo_dato_var
            elif tupla_param_2 != None: #Se guarda el tipo de retorno en la declaracion de la funcion para parametro tipo 2
                nombre_func = tupla_param_2['scope']
                tipo_dato_var = tupla_param_2['tipo_dato']
                tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
                tupla_func_decl['return'] = tipo_dato_var
    elif arbol.type == NodeType.PARAMS_1:
        if semanticsDebugMode == True:
            print("[log] init node:", NodeType.PARAMS_1.name)
        try:
            lista_params = arbol.children[0]
            #print("lista_params: ", lista_params)
        except IndexError:
            msgError("falta void en los parametros", arbol.lineno)
            #exit()
    elif arbol.type == NodeType.PARAM_1:
        if semanticsDebugMode == True:
            print("[log] init node:", NodeType.PARAM_1.name)
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params' : '--', 'lineno' : '', 'offset' : offset, 'index_scope' : '--'}
        offset += 1
        tipo_dato = arbol.leaf
        nombre_variable = arbol.children[0].leaf
        if tipo_dato == 'void':
            msgError("Tipo de dato Invalido", arbol.lineno)# No pueden exitir params con tipo de dato void, se arroja Error
            #exit()
        else:
            registro = insertarRegistro(fila, arbol, scope, NodeType.PARAM_1,tabla_params)# Se agregan los parametros a una tabla auxiliar de params    
            #print("tabla_params: ", tabla_params)
            #Agregar tipos de datos a la declaracion de la funcion
            table_global = stack_TS[0] #Obtener referencia de la tabla del fondo (Contexto Global)
            tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, scope, table_global)#Obtenemos la refencia a la funcion que contiene los PARAMS
            tupla_func_decl['params'].append(arbol.leaf)#Actualizamos el campo de PARAM de la declaracion de funcion
    elif arbol.type == NodeType.PARAM_2:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'params': '--', 'lineno' : '', 'offset': offset, 'index_scope' : '--'}
        offset += 1
        nombre_variable = arbol.children[0].leaf
        tipo_dato = arbol.leaf
        if tipo_dato == 'void':
            msgError("Tipo de dato Invalido", arbol.lineno)# No pueden exitir params con tipo de dato void, se arroja Error
            #exit()
        else:
            registro = insertarRegistro(fila, arbol, scope, NodeType.PARAM_2,tabla_params)# Se agregan los parametros a la tabla local
            #Agregar tipos de datos a la declaracion de la funcion
            table_global = stack_TS[0] #Obtener referencia de la tabla del fondo (Contexto Global)
            tupla = getTupla(NodeType.FUN_DECLARATION, scope, table_global)#Obtenemos a refencia a la funcion que contiene los PARAMS
            tupla['params'].append(arbol.leaf)#Actualizamos el campo de PARAM de la declaracion de funcion

        ##Agregar aqio
    if arbol != None:
        if arbol.type == "compound_stmt":
            table = []
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    crearTabla(node, table, stack_TS, tabla_params)
            stack_TS.append(table)
            scope = 'global'
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    crearTabla(arbol.children[child], table, stack_TS, tabla_params)
    return stack_TS

index = 0
index_aux = 0
def typeCheck(tree, stack):
    global index
    tabla_global = stack[0]
    tupla_aux_main = tabla_global[len(tabla_global_1) - 1] #Ultima declaracion debe ser MAIN
    nombre_funcion = tupla_aux_main['nombre']
    #print("tabla_global: ", tabla_global)
    if nombre_funcion == "main":
        chequeoTipos(tree, checkNode, stack, index)
    else:
         msgError("La funcion main no ha sido declarada/No se encuentra al final de la declaracion")
         #exit()       

def chequeoTipos(arbol, checkNode, stack, index):
    global index_aux
    if arbol != None:
        
        if arbol.type == "compound_stmt":
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    chequeoTipos(node, checkNode, stack, index)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    chequeoTipos(arbol.children[child], checkNode, stack, index)
            checkNode(arbol, stack, index)

def checkNode(t, stack_TS, index):
    #print("Type: {}  Index: {}".format(t.type, index))
    if t.type == NodeType.VAR_DECLARATION_1 or t.type == NodeType.VAR_DECLARATION_2:# declaracion de variable
            tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
            if (t.leaf != 'int'): # la declaracion de una varible debe ser INT
                test_output.append("Error el tipo debe ser INT")
                msgError("el tipo debe ser INT", t.lineno)        
    elif t.type == NodeType.FUN_DECLARATION:
        tabla_simbolos_global = stack_TS[0]#TS local
        tabla_simbolos_local = stack_TS[index]

        nombre_func = t.children[0].leaf

        tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
        tipo_dato_func = tupla_func_decl['tipo_dato']
        tipo_dato_return = tupla_func_decl['return']
        #if tupla_func_decl == 

        if tipo_dato_func == 'void' and tipo_dato_return == 'int':
            msgError("Tipos Incompatibles, valor de retorno inesperado", t.lineno)
        elif tipo_dato_func != 'void' and tipo_dato_func != tipo_dato_return:
            test_output.append("Error missing return statement")
            msgError("missing return statement", t.lineno)
    elif t.type == NodeType.ADDITIVE_EXPRESSION_1:
        tabla_simbolos_global = stack_TS[0]#TS local
        tabla_simbolos_local = stack_TS[index]

        preOrder(t, 0, tabla_simbolos_global)
    elif t.type == NodeType.CALL:
        tabla_simbolos_global = stack_TS[0]
        tabla_simbolos_local = stack_TS[index]

        call_name = t.leaf
        list_params_name_call = [item.leaf for item in t.children] # Lista de parametros del call, solo se tiene el nombre o identificador
        list_params_tipo_dato_call = []
        for nombre_param in list_params_name_call:
            tupla_var = getTupla(NodeType.VAR_DECLARATION_1, nombre_param, tabla_simbolos_local)
            tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_param, tabla_simbolos_global)
            if tupla_var != None:
                list_params_tipo_dato_call.append(tupla_var['tipo_dato'])#Se guarda el tipo de dato que tienen los params del call
            elif tupla_func_decl != None:
                list_params_tipo_dato_call.append(tupla_func_decl['tipo_dato'])#Se guarda el tipo de dato que tienen los params del call
            elif tupla_var == None and tupla_func_decl == None:
                msgError("Variable No Declarada :(", t.lineno)
                #exit()
            elif tupla_func_decl == None:
                msgError("Funcion No declarada :(", t.lineno)
                #exit()                

        tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, call_name, tabla_simbolos_global)
        
        if tupla_func_decl == None: # Si la funcion no ha sido declarada
            msgError("Funcion No declarada", t.lineno)# Arrojar Error
        else:
            list_params_tipo_dato_decl = tupla_func_decl['params']# Se toman los parametros de la declaracion
            if list_params_tipo_dato_call != list_params_tipo_dato_decl: #Se comparan los parametros de la declaracion con los de la llamada
                msgError("Los parametros no coinciden con la declaracion", t.lineno)        
    #elif t.type == NodeType.PARAM_2:
        



#Podriamos mejorar esta funcion para que recupere metadatos de un Nodo o de un Registro (Ts)
def formatearNodo(node, type, scope):
    if type == NodeType.FUN_DECLARATION:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_type = NodeType.FUN_DECLARATION
        val_valor = ''
        val_scope = 'global'
        val_dimension = "1"
        val_lineno = node.lineno
    elif type == NodeType.VAR_DECLARATION_1:
        val_nombre = node.children[0].leaf
        val_tipo_dato = node.leaf
        val_valor = '0'
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
    elif type == NodeType.PARAM_1 or type == NodeType.PARAM_2:
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
    elif type == NodeType.NUMBER:
        val_nombre = 'number'
        val_tipo_dato = 'int'
        val_valor = node.leaf
        val_type = NodeType.NUMBER
        val_scope = scope
        val_dimension = "1"
        val_lineno = node.lineno 
    return {'nombre':val_nombre, 'tipo_dato':val_tipo_dato, 'valor':val_valor, 'type': val_type , 'scope': val_scope, 'dimension': val_dimension, 'lineno' : val_lineno}

def msgError(mensaje, lineno = "x"):
    if errorMessagesFlag == True:
        print("Linea {}: Error {}".format(lineno, mensaje))

def semantica(AST, imprime_short_format = True, imprime_long_format = False):
    global stack_TS, scope, YaPase, paramsIngresadosLocalmente, seHaPregargado, offset, index_scope
    tabla = []
    tabla_params = []
 
    stack = crearTabla(AST, tabla, stack_TS, tabla_params)
    typeCheck(AST, stack)
    if showTableEnabled:
        mostrarTabla(stack,imprime_short_format, imprime_long_format)
    stack_TS.clear()
    tabla.clear()
    tabla_params.clear()
    scope = 'global'
    YaPase = False
    paramsIngresadosLocalmente = False
    seHaPregargado = False
    offset = 1
    index_scope = 1

def mostrarTabla(stack,imprime_short_format, imprime_long_format):
    if imprime_long_format:
        print("name       dataType  scope       Type                params            Valor      lineno      offset     index_scope")
        for ts in stack:
            for i in range(len(ts)):
                lista_params = '{}'.format(ts[i]['params']) # List of Params
                print(f"{ts[i]['nombre']:11}{ts[i]['tipo_dato']:10}{ts[i]['scope']:12}{ts[i]['type'].name:20}{lista_params:10}{ts[i]['valor']:10}{ts[i]['lineno']:13}{ts[i]['offset']:10}{ts[i]['index_scope']:15}")
    elif imprime_short_format:
        print("name       dataType  scope   Lineno")
        for ts in stack:
            for i in range(len(ts)):
                print(f"{ts[i]['nombre']:11}{ts[i]['tipo_dato']:10}{ts[i]['scope']:6}{ts[i]['lineno']:5}")

def setShowTable(flag):
    global showTableEnabled
    showTableEnabled  = flag

def getTestOutput():
    global test_output
    return test_output

def semanticsDebugMode(flag = False):
    global semanticsDebugModeFlag
    semanticsDebugModeFlag = flag

def semanticsErrorMessages(flag):
    global errorMessagesFlag
    errorMessagesFlag = flag