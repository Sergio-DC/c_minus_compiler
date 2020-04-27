import math

stack_TS = [] # Stack de tabla de simbolos
#tabla_simbolos = []


def tabla(tree, imprime = True):
    # Recorremos el arbol en Preorden
    preorden(tree, 'global', None)


    print("stack_TS: ", stack_TS)
    
    for tabla_simbolos in stack_TS:
        for item in tabla_simbolos:
            print("Tabla: {}".format(item['scope']), item)




def preorden(arbol, scope, tabla_temp):
    global stack_TS
    if arbol != None:
        
        if arbol.type == 'funcion':
            tabla_temp = []
            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}
            fila['tipo'] = arbol.children[0].leaf
            fila['nombre'] = arbol.children[1].leaf
            fila['rol'] = 'funcion'
            fila['scope'] = arbol.children[1].leaf
            scope = arbol.children[1].leaf
            tabla_temp.append(fila)
            stack_TS.append(tabla_temp)
        if arbol.type == "compound_stmt":
                #tabla_temp = []
                for i in range(len(arbol.children)):
                    for node in arbol.children[i]:
                        if node.type == 'variable':
                            fila = {'nombre': '', 'tipo': '', 'valor':'', 'rol' : '', 'scope': ''}

                            # Buscamos si el simbolo ya existe en la TS, si existe se actualiza el valor, sino lo agregamos
                            registro =buscar_ST('variable', node.children[0].leaf, tabla_temp)#param derecha, NOMBRE variable
                            if registro != None: # Actualizamos simbolo
                                if len(node.children) == 2:#Si la variable se usa para asignacion, obtenemos el valor guardado en la variable
                                    if registro['valor'] != '':
                                        valor_aux = registro['valor'] # Valor anterior de Y

                                    resultado = calculoAritmeticoArbol(node.children[1])#Calculo del string de la derecha de la variable
                                    registro['valor'] = resultado
                            else: # Se crea y agrega un nuevo registro a una tabla
                                fila['tipo'] = node.leaf
                                fila['rol'] = 'variable'
                                fila['nombre'] = node.children[0].leaf
                                fila['scope'] = scope                            
                                tabla_temp.append(fila)# Agregar registros/objetos a la Tabla de Simbolos
                #stack_TS.append(tabla_temp)    
        elif arbol.children:
            for child in range(len(arbol.children)):
                if arbol.children[child] != []:
                    preorden(arbol.children[child], scope, tabla_temp)

#Buscar en la tabla de simbolos, Devuelve un objeto/registro que contiene los atrubutos del simbolo
def buscar_ST(rol, nombre, tabla_simbolos):
    for i in range(len(tabla_simbolos)):
        if tabla_simbolos[i]['rol'] == rol and tabla_simbolos[i]['nombre'] == nombre:
            #print("i_ ", tabla_simbolos[i]['nombre'])
            registro = tabla_simbolos[i]
            # tabla_simbolos[i]['valor'] = valor
            return registro
    return None

def preOrder(arbol, resultado):
    if arbol != None:
        if str(arbol.leaf) not in '+-*/':
            return arbol.leaf
        if arbol.children != []:
            hijoLeft = preOrder(arbol.children[0], resultado)
        if arbol.children != []:
            hijoDer = preOrder(arbol.children[1], resultado)
        #print('HijoLeft: {}  HijoDer: {}'.format(hijoLeft, hijoDer))
        resultado = operacion(arbol.leaf, hijoLeft, hijoDer)
        #print('resultado = ', resultado)
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

