import math

stack_TS = [] # Stack de tabla de simbolos

def tabla(tree, imprime = True):
    tabla_temp = []
    declaracion_global = None

    for declaracion_global in tree.children:#Acceder al array de variables y funciones globales
        if declaracion_global.type == 'declaracion-var': # Variables globales
            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'dimension' : '', 'scope': ''}
            tabla_temp = insertar_actualizar_variables(declaracion_global, tabla_temp, 'global', fila)
        if declaracion_global.type == 'declaracion-array':
            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'dimension' : '', 'scope': ''}
            tabla_temp = insertar_actualizar_variables(declaracion_global, tabla_temp, 'global', fila)
        if declaracion_global.type == 'funcion': # Funciones Globales
            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': '', 'params':[]}
            # Devuelve el scope que usaran las variable interiores del cuerpo
            fila, scope = insertarRegistro(fila, declaracion_global, 'global', 'funcion',tabla_temp)
            nueva_tabla = []
            #recorrido del los params de la funcion
            nueva_tabla = recorrido_params(declaracion_global.children[0], scope, nueva_tabla)
            valores = []
            for registro in nueva_tabla:              
                valores.append(registro['tipo'])
            actualizar_TS('funcion', fila['nombre'], tabla_temp, valores) if nueva_tabla else print("No hacer Nada")       
            # recorrido del cuerpo de la funcion
            nueva_tabla = recorrido_compound(declaracion_global.children[1], scope, nueva_tabla)
            
    stack_TS.append(tabla_temp)     
    
    for tabla_simbolos in stack_TS:
        for item in tabla_simbolos:
            print("Tabla: {}".format(item['scope']), item)

def recorrido_params(arbol, scope, nueva_tabla):
    if arbol.type == "params":
        for node in arbol.children:
            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}
            insertar_actualizar_variables(node, nueva_tabla, scope, fila, 'params')
    return nueva_tabla
                 

def recorrido_compound(arbol, scope, nueva_tabla):
    #nueva_tabla = []
    for i in range(len(arbol.children)):
        for node in arbol.children[i]:
            if node.type == 'declaracion-var':
                fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}
                insertar_actualizar_variables(node, nueva_tabla, scope, fila, 'declaracion-var')
            elif node.type == 'declaracion-array':
                fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': 'de'}
                insertar_actualizar_variables(node, nueva_tabla, scope, fila, '', 'declaracion-array')
            elif node.type == 'variable':
                fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}
                insertar_actualizar_variables(node, nueva_tabla, scope, fila, 'variable')
            elif node.type == 'return_stmt_2':
                fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}
                insertarRegistro(fila, node, scope, 'return',nueva_tabla, 'return')
    stack_TS.append(nueva_tabla)

    return nueva_tabla

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atributos del simbolo
def buscar_ST(rol, nombre, tabla_simbolos):
    """
    Parameters:

    rol : (str) este puede ser 'variable'|'funcion'|'arreglo'

    nombre : (str) este lo da el programador a 'variable'|'funcion'|'arreglo'

    tabla_simbolos : (list) TS que sera actualizada

    Returns:
    registro : (dict) un simbolo con sus metadatos, en caso contrario None
    """
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['rol'] == rol and tabla_simbolos[i]['nombre'] == nombre:
            registro = tabla_simbolos[i]
            return registro
    return None

def actualizar_TS(rol, nombre, tabla_simbolos, valores):
    """
    Parameters:

    rol : (str) este puede ser 'variable'|'funcion'|'arreglo'

    nombre : (str) este lo da el programador a 'variable'|'funcion'|'arreglo'

    tabla_simbolos : (list) TS que sera actualizada

    valores : (list) con los que sera actualizada la TS
    """
    registro = buscar_ST(rol, nombre, tabla_simbolos)
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
    if not isinstance(valIzq, int):
        registro = buscar_ST('variable', valIzq)
        valIzq = registro['valor']#Reasignamos un valor de tipo INT
    if not isinstance(valDer, int):
        registro = buscar_ST('variable', valDer)
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

def insertar_actualizar_variables(node, tabla_temp, scope, fila, rol):
    # Busqueda del simbolo en la tabla del SCOPE actual, si ya existe en la TS se actualiza el valor 
    # sino se verifica la existencia en la tabla de SCOPE global
    nombre = node.children[0].leaf
    registro = buscar_ST(rol, nombre, tabla_temp)#param derecha, NOMBRE variable
    if registro != None: # Actualizamos simbolo
        if len(node.children) == 2:#Si la variable se usa para asignacion, obtenemos el valor guardado en la variable
            if registro['valor'] != '':
                valor_aux = registro['valor'] # Valor anterior de Y

            resultado = calculoAritmeticoArbol(node.children[1])#Calculo del string de la derecha de la variable
            registro['valor'] = resultado
    else: # Se agrega un nuevo registro a la tabla
        insertarRegistro(fila, node, scope, rol,tabla_temp)                   
    return tabla_temp

#Se inserta Funcion a la tabla de Simbolos
def insertarRegistro(fila, declaracion_global, scope, rol,  tabla_temp):
    if rol == 'declaracion-var' or rol == 'funcion':
        tipo = declaracion_global.leaf
        nombre = declaracion_global.children[0].leaf
    elif rol == 'variable' or rol == 'params':
        tipo = declaracion_global.leaf
        nombre = declaracion_global.children[0].leaf
    else: # return
        nombre = declaracion_global.children[0].leaf
        if isinstance(nombre, int):
            tipo = 'int'
        else:
            tipo = 'undefined'

    fila['tipo'] = tipo
    fila['nombre'] = nombre
    fila['rol'] = rol
    fila['scope'] = scope
    scope = declaracion_global.children[0].leaf
    tabla_temp.append(fila)

    return fila, scope

def typeCheck(tree):
    imprimeAST(tree, checkNode)

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
            #print(arbol.leaf)

def checkNode(t):
    if t.type == 'declaracion-var':# declaracion de variable
            print("Tipo: {}  id: {}".format(t.leaf, t.children[0].leaf))
            if (t.leaf != 'int'):
                typeError(t,"El tipo debe ser INT")
    elif t.type == 'funcion':
            print("Tipo: {}  id: {}".format(t.leaf, t.children[0].leaf))
            #Buscamos en la TS un RETURN, si este tiene valor INT y el retorno es VOID arrojamos ERROR
            #Buscamos en la TS un RETURN, si no hay y el retorno es INT arrojamos ERROR
            tabla_simbolos = stack_TS.pop(0)

            return_stmt = None
            for registro in tabla_simbolos:
                if registro['rol'] == 'return':# Buscamos un statement de tipo RETURN
                    return_stmt = registro
                    break

            if return_stmt != None:
                if return_stmt['tipo'] != t.leaf:#Se compara el retorno con el retorno de firma
                    print("incompatible types: unexpected return value")
            elif return_stmt == None and t.leaf == 'int':
                print("error: missing return statement")
                
            # if ((t.op == TokenType.EQ) or (t.op == TokenType.LT)):
            #     t.type = ExpType.Boolean
            # else:
            #     t.type = ExpType.Integer

        # elif t.exp in [ExpKind.ConstK, ExpKind.IdK]:
        #     t.type = ExpType.Integer
    # elif t.nodekind == NodeKind.StmtK:
    #     if t.stmt == StmtKind.IfK:
    #         if (t.child[0].type == ExpType.Integer):
    #             typeError(t.child[0],"if test is not Boolean")
    #     elif t.stmt == StmtKind.AssignK:
    #         if (t.child[0].type != ExpType.Integer):
    #             typeError(t.child[0],"assignment of non-integer value")
    #     elif t.stmt == StmtKind.WriteK:
    #         print("Escribir: ", t.child[0].type)
    #         if (t.child[0].type != ExpType.Integer):
    #             typeError(t.child[0],"write of non-integer value")
    #     elif t.stmt == StmtKind.RepeatK:
    #         print("booleano: ", t.name)
    #         if (t.child[1].type == ExpType.Integer):
    #             typeError(t.child[1],"repeat test is not Boolean")

def typeError(t, message):
    print("Type error at line", t.lineno, ":",message)
    Error = True