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

# Recibe un ast de expresiones aritmeticas y devuelve el resultado del calculo
#La TS la ocupamos cuando la expresion esta compuesta por literales, en este caso recurrimos a la TS para localizar el valor
def calculoAritmeticoArbol(arbol, tabla_simbolos):
    resultado = 0;    
    resultado = preOrder(arbol, resultado , tabla_simbolos)
    return resultado

def preOrder(arbol, resultado, tabla_simbolos):
    if arbol != None:
        print("arbol type: {}".format(arbol.type))
        if str(arbol.leaf) not in '+-*/':
            return arbol
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado, tabla_simbolos)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado, tabla_simbolos)
        #resultado = operacion(arbol.leaf, hijoLeft, hijoDer, tabla_simbolos)
        typeCheckArithmetic(arbol.leaf, hijoLeft, hijoDer, tabla_simbolos)
    return resultado


def typeCheckArithmetic(op, valIzq, valDer, tabla_simbolos):
    resultado = None
    print("valIzq: ", valIzq)
    print("valDer: ", valDer)

    tipo_dato_call_izq = None
    tipo_dato_call_der = None
    print("Entre 1")
    if valIzq.type == NodeType.CALL:
        nombre_call_izq = valIzq.leaf
        tupla_func_izq = getTupla(NodeType.FUN_DECLARATION, nombre_call_izq, tabla_simbolos)
        tipo_dato_call_izq = tupla_func_izq['tipo_dato']

    if valDer.type == NodeType.CALL:
        nombre_call_der = valDer.leaf
        tupla_func_der = getTupla(NodeType.FUN_DECLARATION, nombre_call_der, tabla_simbolos)
        if tupla_func_der == None:
            msgError("Funcion no declarada")
            exit()
        else:
            tipo_dato_call_der = tupla_func_der['tipo_dato']


    if tipo_dato_call_izq != None:
        if tipo_dato_call_izq != 'int':
            msgError("en el tipo de la expresion: ", valIzq.lineno)
            exit()
    
    if tipo_dato_call_der != None:
        if tipo_dato_call_der != 'int':
            msgError("en el tipo de la expresion", valDer.lineno)
            exit()
    
    # if op == '+':
        
    #     resultado = int(valIzq) + int(valDer)
    # if op == '-':
    #     resultado = int(valIzq) - int(valDer)
    # if op == '*':
    #     resultado = int(valIzq) * int(valDer)
    # if op == '/':
    #     resultado = int(valIzq) / int(valDer)

    # return resultado
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
tabla_params = []
seHaPregargado = False
def crearTabla(arbol, table, stack_TS):
    global scope, YaPase, tabla_params, seHaPregargado
    # print("Ora: ", arbol.type)
    if arbol.type == NodeType.VAR_DECLARATION_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        tupla_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable fue declarada
        if tupla_1 == None and tupla_2 == None:
            tupla_var = insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_1,  table)

            if tabla_params != []:
                for tupla_param in tabla_params[::-1]:
                    table.insert(0,tupla_param)
        else:
            msgError("Variable Repetida", arbol.lineno)
            exit()
    elif arbol.type == NodeType.VAR_DECLARATION_2: # Declaracion de variable de tipo array []
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'dimension' : '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        tamano = arbol.children[1].leaf
        tupla_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)# Buscar en TS si la variable fue declarada
        tupla_2 = getTupla(NodeType.VAR_DECLARATION_2, nombre_variable, table)# Buscar en TS si la variable fue declarada
        if tupla_1 == None and tupla_2 == None:            
            insertarRegistro(fila, arbol, scope, NodeType.VAR_DECLARATION_2, table)
            if tabla_params != []:
                for tupla_param in tabla_params[::-1]:
                    table.insert(0,tupla_param)
        else:
            msgError("Variable Repetida", arbol.lineno)
    elif arbol.type == NodeType.FUN_DECLARATION:
        #Precargamos TS con input() y output()
        if not seHaPregargado:
            fila = {'nombre': 'input', 'tipo_dato': 'int', 'valor': '', 'type' : NodeType.FUN_DECLARATION, 'scope': 'global', 'params':[],'return': '', 'lineno' : ''}
            table.append(fila)
            fila = {'nombre': 'output', 'tipo_dato': 'void', 'valor': '', 'type' : NodeType.FUN_DECLARATION, 'scope': 'global', 'params':['int'],'return': '', 'lineno' : ''}
            table.append(fila)
            seHaPregargado = True
        tabla_params.clear()
        fila = {'nliombre': '', 'tipo_dato': '', 'valor': '', 'type' : '', 'scope': '', 'params':[],'return': '', 'lineno' : ''}
        tupla_fun_decl = insertarRegistro(fila, arbol, scope, NodeType.FUN_DECLARATION, table)
        scope = tupla_fun_decl['nombre']
        if not YaPase:
            stack_TS.append(table)
        YaPase = True
        # table = []
    elif arbol.type == NodeType.EXPRESSION_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf#Variable a la que se le asigna el valor
        valor = arbol.children[1].leaf # Valor que sera asignado
        print("valor: ", valor)
        tupla_var = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table) #Buscar en TS si la variable fue declarada
        tupla_param = getTupla(NodeType.PARAM_1, nombre_variable, table)
        if tupla_var != None: #Actualizar si la variable ya existe
            if isinstance(valor, int):               
                tupla_var['valor'] = valor #Actualizamos la variable
            else: # En este punto el valor ya no es un numero
                tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, valor, stack_TS[0])
                if valor in '+-*/':
                    print("pase bien")
                    preOrder(arbol, None, table) 
                else:
                    print("pase: ", tupla_func_decl)
                    print("tupla_func_decl: ", tupla_func_decl['tipo_dato'])
                    print("tupla_var: ", tupla_var['tipo_dato'])
                    if tupla_func_decl['tipo_dato'] != tupla_var['tipo_dato']:
                        msgError("Tipos de datos Incompatibles", arbol.lineno)
                        exit()
        elif tupla_param == None:
            msgError("Variable no declarada 1.5", arbol.lineno)
            exit()
    elif arbol.type == NodeType.RETURN_STMT_2:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        print("nombre_variable: ", nombre_variable)
        print("table: ", table)
        #Buscar en TS si la variable fue declarada
        tupla_var_1 = getTupla(NodeType.VAR_DECLARATION_1, nombre_variable, table)
        tupla_var_2 = getTupla(NodeType.PARAM_1, nombre_variable, table)
        print("tupla_var_1: ", tupla_var_1)
        print("tupla_var_2: ", tupla_var_2)
        if tupla_var_1 == None and tupla_var_2 == None:
            msgError("Variable no declarada 2", arbol.lineno) #Arrojamos Error
            exit()
        elif tupla_var_1 != None:
            tabla_simbolos_global = stack_TS[0]
            nombre_func = tupla_var_1['scope']
            tipo_dato_var = tupla_var_1['tipo_dato']
            tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
            tupla_func_decl['return'] = tipo_dato_var
        elif tupla_var_2 != None:
            tabla_simbolos_global = stack_TS[0]
            nombre_func = tupla_var_2['scope']
            tipo_dato_var = tupla_var_2['tipo_dato']
            tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
            print("return: ", tipo_dato_var)
            tupla_func_decl['return'] = tipo_dato_var
    elif arbol.type == NodeType.PARAMS_1:
        try:
            lista_params = arbol.children[0]
            #print("lista_params: ", lista_params)
        except IndexError:
            msgError("Falta void", arbol.lineno)
            exit()
    elif arbol.type == NodeType.PARAM_1:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        tipo_dato = arbol.leaf
        nombre_variable = arbol.children[0].leaf
        if tipo_dato == 'void':
            msgError("Tipo de dato Invalido", arbol.lineno)# No pueden exitir params con tipo de dato void, se arroja Error
            exit()
        else:
            registro = insertarRegistro(fila, arbol, scope, NodeType.PARAM_1,tabla_params)# Se agregan los parametros a la tabla local            
            #Agregar tipos de datos a la declaracion de la funcion
            table_global = stack_TS[0] #Obtener referencia de la tabla del fondo (Contexto Global)
            tupla = getTupla(NodeType.FUN_DECLARATION, scope, table_global)#Obtenemos a refencia a la funcion que contiene los PARAMS
            tupla['params'].append(arbol.leaf)#Actualizamos el campo de PARAM de la declaracion de funcion
    elif arbol.type == NodeType.PARAM_2:
        fila = {'nombre': '', 'tipo_dato': '', 'valor':'', 'type' : '', 'scope': '', 'lineno' : ''}
        nombre_variable = arbol.children[0].leaf
        tipo_dato = arbol.leaf
        if tipo_dato == 'void':
            msgError("Tipo de dato Invalido", arbol.lineno)# No pueden exitir params con tipo de dato void, se arroja Error
            exit()
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
                    crearTabla(node, table, stack_TS)
            stack_TS.append(table)
            scope = 'global'
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    crearTabla(arbol.children[child], table, stack_TS)
    return stack_TS

index = 0
index_aux = 0
def typeCheck(tree, stack):
    global index
    tabla_global = stack[0]
    tupla_aux_main = tabla_global[len(tabla_global_1) - 1] #Ultima declaracion debe ser MAIN
    nombre_funcion = tupla_aux_main['nombre']

    if nombre_funcion == "main":
        imprimeAST(tree, checkNode, stack, index)
    else:
         msgError("La funcion main no ha sido declarada/No se encuentra al final de la declaracion")
         exit()       

def imprimeAST(arbol, checkNode, stack, index):
    global index_aux
    if arbol != None:
        
        if arbol.type == "compound_stmt":
            index_aux = index_aux + 1
            index = index_aux
            for i in range(len(arbol.children)):
                for node in arbol.children[i]:
                    imprimeAST(node, checkNode, stack, index)
        elif arbol.children or arbol.type == NodeType.CALL:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    imprimeAST(arbol.children[child], checkNode, stack, index)
            checkNode(arbol, stack, index)

def checkNode(t, stack_TS, index):
    print("Type: {}  Index: {}".format(t.type, index))
    if t.type == NodeType.VAR_DECLARATION_1:# declaracion de variable
        try:
            tabla_simbolos = stack_TS[0] #TS Global, CUIDADO: implementar un mecanismo de getion de colas
            if (t.leaf != 'int'): # la declaracion de una varible debe ser INT
                msgError("El tipo debe ser INT", t.lineno)
                exit()
        except IndexError:
            msgError("La funcion main no ha sido declarada")
            exit()
        
    elif t.type == NodeType.FUN_DECLARATION:
        tabla_simbolos_global = stack_TS[0]#TS local
        tabla_simbolos_local = stack_TS[index]

        nombre_func = t.children[0].leaf

        tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, nombre_func, tabla_simbolos_global)
        tipo_dato_func = tupla_func_decl['tipo_dato']
        tipo_dato_return = tupla_func_decl['return']

        if tipo_dato_func == 'void' and tipo_dato_return == 'int':
            print("incompatible types: unexpected return value")
            exit()
        elif tipo_dato_func != 'void' and tipo_dato_func != tipo_dato_return:
            msgError("missing return statement", t.lineno)
            exit()
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
                exit()
            elif tupla_func_decl == None:
                msgError("Funcion No declarada :(", t.lineno)
                exit()                

        tupla_func_decl = getTupla(NodeType.FUN_DECLARATION, call_name, tabla_simbolos_global)
        list_params_tipo_dato_decl = tupla_func_decl['params']
        if list_params_tipo_dato_call != list_params_tipo_dato_decl:
            msgError("Los parametros no coinciden con la declaracion", t.lineno)
            exit()

        if tupla_func_decl == None:
            msgError("Funcion No declarada", t.lineno)
            exit()
        #else:

        
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
    elif type == NodeType.PARAM_1 or NodeType.PARAM_2:
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

def msgError(mensaje, lineno = "x"):
    print("Linea {}: Error {}".format(lineno, mensaje))

def semantica(AST, imprime = True):
    tabla = []
    stack_TS = []
    stack = crearTabla(AST, tabla, stack_TS)
    typeCheck(AST, stack)

    if imprime:
        print("Variable Name  Tipo_Dato   Scope   Lineno")
        for ts in stack:
            for i in range(len(ts)):
                print(f"{ts[i]['nombre']:15}{ts[i]['tipo_dato']:12}{ts[i]['scope']:10}{ts[i]['lineno']:1}")
        #print('\n\n'.join('{}: {}'.format(*k) for k in enumerate(stack)))