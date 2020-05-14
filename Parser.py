import ply.yacc as yacc
from lexer import tokens
import sys
from globalTypes import *
start = 'program'

list_args = []
list_local_declarations = []
list_statement_list = []
list_param_list = []
var_decl = None
list_declaration_list = []
str_trace = ''
prompt_pos = ''
token_error = ''
line_error = ''
mensaje = ''

class Node:
     def __init__(self,type,children=None,leaf=None, lineno = None):
          self.type = type #Puede tener el token
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf #Tiene el valor del Lexema
          self.lineno = lineno
class MessageError:
     def __init__(self, message, line_error_content, promt_pos):
          self.message = message
          self.line_error_content = line_error_content
          self.prompt_pos
VERBOSE = 1
masInfo = True

def inOrder(arbol, linear_tree):
     if arbol != None:
          if arbol.children != []:
               inOrder(arbol.children[0], linear_tree)
          linear_tree.append(arbol.leaf)
          if arbol.children != []:
               inOrder(arbol.children[1], linear_tree)
     return linear_tree
                    
def p_program(p):
     'program : declaration_list'
     new_declaration_list = []
     if masInfo:
          print("program: ", p[1])
     for declaration in list_declaration_list:
          if declaration != None:
               new_declaration_list.append(declaration)
     list_declaration_list.clear()

     if new_declaration_list == []:
          node = Node("global_1", [p[1]], "program")
     else:
          node = Node("global_2", new_declaration_list, "program")
     p[0] = node

def p_declaration_list_1(p):
     'declaration_list : declaration_list declaration'
     if masInfo:
          print("declaration_list_1: ", p[1], p[2])
     global list_declaration_list
     list_declaration_list.append(p[1])
     list_declaration_list.append(p[2])

def p_declaration_list_2(p):
     'declaration_list : declaration'
     if masInfo:
          print("declaration_list_2: ", p[1])
     p[0] = p[1]

def p_declaration(p):
     '''declaration : var_declaration 
     | fun_declaration'''
     if masInfo:
          print("declaration: ", p[1])
     p[0] = p[1]

def p_var_declaration_1(p):
     'var_declaration : type_specifier ID SEMICOLON'
     p[2] = Node("identifier", None, p[2])
     if masInfo:
          print("var_declaration_1: ", p[1], p[2], p[3])
     global var_decl
     var_decl = Node(NodeType.VAR_DECLARATION_1, [p[2]], p[1], p.lineno(2))
     p[0] = var_decl

def p_var_declaration_1_error(p):
     'var_declaration : type_specifier ID'
     global parser
     str_trace = "{} {}".format(p[1], p[2])
     prompt_pos = str_trace.index(p[2])#Reubicamos el error
     mensaje ="Linea {}: Error en la expresión de declaracion".format(p.lineno(2))
     print(mensaje)
     print(str_trace)
     print((prompt_pos) * " ","^")
     parser.errok()

        
def p_var_declaration_2(p):
     'var_declaration : type_specifier ID LBRACKET NUMBER RBRACKET SEMICOLON'
     p[2] = Node("var_1", None, p[2])
     p[4] = Node("num", None, p[4])
     if masInfo:
          print("var_declaration_2: ", p[1], p[2], p[3], p[4], p[5], p[6])
     p[0] = Node(NodeType.VAR_DECLARATION_2, [p[2], p[4]], p[1], p.lineno(2))

def p_var_declaration_2_error(p):
     'var_declaration : type_specifier ID LBRACKET NUMBER RBRACKET'
     global parser
     str_trace = "{} {} {}{}{}".format(p[1], p[2], p[3], p[4], p[5])
     prompt_pos = str_trace.index(p[5])#Reubicamos el error
     mensaje ="Linea {}: Error en la expresión falta un ;".format(p.lineno(2))
     print(mensaje)
     print(str_trace)
     print((prompt_pos) * " ","^")
     parser.errok()

def p_type_specifier_1(p):
     'type_specifier : INT'
     if masInfo:
          print("type_specifier_1: ", p[1])
     p[0] =  p[1]

def p_type_specifier_2(p):
     'type_specifier : VOID'
     if masInfo:
          print("type_specifier_2", p[1])
     p[0] = p[1]

def p_fun_declaration(p):
     'fun_declaration : type_specifier ID LPAREN params RPAREN compound_stmt'
     if masInfo:
          print("fun_declaration: ", p[1], p[2], p[3], p[4], p[5], p[6])
     p[2] = Node(NodeType.PARAMS_1, p[4], p[2])
     p[0] = Node(NodeType.FUN_DECLARATION, [p[2], p[6]], p[1], p.lineno(2))


def p_params_1(p):
     'params : param_list'
     if masInfo:
          print("params_1: ", p[1])
     new_list_param = []
     for param in list_param_list:
          if param != None:
               new_list_param.append(param)
     list_param_list.clear()
     
     p[0] =  new_list_param 
     
def p_params_2(p):
     'params : VOID'
     new_list_param = []
     node = Node(NodeType.PARAMS_2, None, p[1])
     new_list_param.append(node)
     p[0] = new_list_param

def p_param_list_1(p):
     'param_list : param_list COMMA param'
     if masInfo:
          print("param_list_1: ", p[1], p[2], p[3].leaf)
     global list_param_list
     list_param_list.append(p[1])
     list_param_list.append(p[3])

def p_param_list_2(p):
     'param_list : param'
     if masInfo:
          print("param_list_2: ", p[1].leaf)
     list_param_list.append(p[1])

def p_param_list_3(p):
     'param_list : empty'
	

def p_param_1(p):
     'param : type_specifier ID'
     if masInfo:
          print("param_1: ", p[1], p[2])    
     p[2] = Node("var_1", None, p[2])
     p[0] = Node(NodeType.PARAM_1,[p[2]], p[1], p.lineno(1))

def p_param_2(p):
     'param : type_specifier ID LBRACKET RBRACKET'
     if masInfo:
          print("param_2: ", p[1], p[2], p[3], p[4])
     p[2] = Node("nulle", None, p[2])
     p[0] = Node(NodeType.PARAM_2, [p[2]] ,p[1])

def p_compound_stmt(p):
     'compound_stmt : LBLOCK local_declarations statement_list RBLOCK'
     if masInfo:
          print("compund_stmt: ", p[1], p[2], p[3])
     new_list_local_declarations = []
     new_statement_list = []
     for item in list_local_declarations:
          if item != None:
               new_list_local_declarations.append(item)
     list_local_declarations.clear()
     for item in list_statement_list:
          if item != None:
               new_statement_list.append(item)
     list_statement_list.clear()
     
     p[0] = Node("compound_stmt", [new_list_local_declarations, new_statement_list],
                 "compound_Stmt")

def p_local_declarations_1(p):
     'local_declarations : local_declarations var_declaration'
     if masInfo:
          print("local_declarations_1: ", p[1], p[2].leaf, p[2].children)
     global list_local_declarations
     list_local_declarations.append(p[1])
     list_local_declarations.append(p[2])

def p_local_declarations_2(p):
     'local_declarations : empty'

def p_statement_list_1(p):
     'statement_list : statement_list statement'
     if masInfo:
          if p[2] != None:
               print("statement_list: ", p[1], p[2].leaf)
     global list_statement_list
     list_statement_list.append(p[1])
     list_statement_list.append(p[2])
     
def p_statement_list_2(p):
     'statement_list : empty'	
     pass

def p_statement(p):
     '''statement : expression_stmt 
     | compound_stmt
     | selection_stmt
     | iteration_stmt
     | return_stmt'''	
     if masInfo:
          print("statement: ", p[1])
     global parser
     p[0] = p[1]

def p_expression_stmt_1(p):
     'expression_stmt : expression SEMICOLON'
     global parser, str_trace, prompt_pos, token_error, mensaje
     if masInfo:
          print("expression_stmt_1: ", p[1], p[2])
     if p[1] != None:
          p[0] = p[1]
     else:
          print(mensaje)
          print(str_trace)
          prompt_pos = str_trace.index(token_error)#Reubicamos el error
          print((prompt_pos-1) * " ","^")

def p_expression_stmt_1_error(p):
     'expression_stmt : expression error'
     global parser, str_trace, line_error
     if p[1] != None:
          linear_tree = []
          linear_tree = inOrder(p[1], linear_tree)#Recorre el conjunto de instrucciones en el arbol y los devuelve de forma lineal
          str_terms = len(linear_tree) * "{} "
          str_trace = str_terms.format(*[term for term in linear_tree])# string de error e.g {*+ 7}
          str_len = len(str_trace)# longitud del string de error
          aux_list = list(str(linear_tree[len(linear_tree) - 1])) # string de error para el programador
          last_element = aux_list[-1] # último caracter del string de error
          prompt_pos = len(str_trace) - 1 - str_trace[::-1].index(last_element) # gorrito que apunta al último caracter, ya que es un error por falta de COMMA
          print("Linea {}: Error en la expresión falta un ;".format(p.lineno(2)))
          print(str_trace)
          print((prompt_pos) * " ","^")
          
          parser.errok()
     else:
          last_element = str_trace[-1]
          prompt_pos = len(str_trace) - 1 - str_trace[::-1].index(last_element) # gorrito que apunta al último caracter, ya que es un error por falta de COMMA
          print(str_trace)
          print((prompt_pos-1) * " ","^")

def p_expression_stmt_2(p):
     'expression_stmt : SEMICOLON'
     if masInfo:
          print("expression_stmt_2: ", p[1])
     p[0] = Node("expression_stmt_2",None,p[1])

def p_selection_stmt_1(p):
     'selection_stmt : IF LPAREN expression RPAREN statement'
     if masInfo:
          print("selection_stmt_1: ", p[1], p[2], p[3], p[4], p[5])
     p[0] = Node("selection_stmt_1",[p[3], p[5]] ,p[1])
def p_selection_stmt_2(p):
     'selection_stmt : IF LPAREN expression RPAREN statement ELSE statement'
     if masInfo:
          print("selection_stmt_2: ", p[1], p[2], p[3], p[4], p[5], p[6], p[7])
     p[0] = Node("selection_stmt_2",[p[3], p[5], p[7]] ,p[1])
     
def p_iteration_stmt(p):
     'iteration_stmt : WHILE LPAREN expression RPAREN statement'
     if masInfo:
          print("iterarion_stmt: ", p[1], p[2], p[3], p[4], p[5].leaf)
     p[0] = Node("iteration_stmt", [p[3], p[5]], p[1])

def p_return_stmt_1(p):
     'return_stmt : RETURN SEMICOLON'
     if masInfo:
          print("return_stmt_1: ", p[1], p[2])
     p[0] = Node("return_stmt_1",None ,p[1])

def p_return_stmt_1_error(p):
     'return_stmt : RETURN'
     global parser
     str_trace = "{}".format(p[1])
     prompt_pos = len(str_trace) - 1 - str_trace[::-1].index("n") # gorrito que apunta al último caracter, ya que es un error por falta de COMMA
     mensaje ="Linea {}: Error en la expresión return falta un ;".format(p.lineno(1))
     print(mensaje)
     print(str_trace)
     print((prompt_pos) * " ","^")
     parser.errok()


def p_return_stmt_2(p):
     'return_stmt : RETURN expression SEMICOLON'
     if masInfo:
          print("return_stmt_2: ", p[1],[p[2]], p[3])
     p[0] = Node(NodeType.RETURN_STMT_2,[p[2]],p[1], lineno=p.lineno(1))

def p_return_stmt_2_error(p):
     'return_stmt : RETURN expression'
     global parser, str_trace
     linear_tree = []
     linear_tree = inOrder(p[2], linear_tree)
     str_terms = len(linear_tree) * "{} "
     str_terms += " {}"
     str_trace = str_terms.format(p[1], *[term for term in linear_tree])
     last_element = str_trace[-1]
     prompt_pos = len(str_trace) - 1 - str_trace[::-1].index(last_element) # gorrito que apunta al último caracter, ya que es un error por falta de COMMA
     mensaje ="Linea {}: Error en la expresión return falta un ;".format(p.lineno(1))
     print(mensaje)
     print(str_trace)
     print((prompt_pos) * " ","^")
     parser.errok()

def p_expression_1(p):
     'expression : var EQUAL expression'
     global parser, str_trace, prompt_pos
     if masInfo:
          print("expression_1: ", p[1], p[2], p[3])
     if p[3] != None:
          p[0]= Node(NodeType.EXPRESSION_1, [p[1],p[3]], p[2], p.lineno(2))
     else: # Configuraciones para preparar el ERROR
          str_trace_aux = p[1].leaf + " " + p[2] + " "
          str_trace_aux += str_trace
          str_trace = str_trace_aux
          prompt_pos = str_trace_aux.index(token_error)#Reubicamos el error      
          p[0] = None

def p_expression_1_error(p):
     'expression : var error expression'
     global parser, str_trace, prompt_pos, token_error, mensaje
     linear_tree = []
     linear_tree = inOrder(p[3], linear_tree)
     str_terms = "{} {}{} " # Se agregan 3 más
     str_terms += len(linear_tree) * "{} "    
     str_trace = str_terms.format(p[1].leaf, '=', p[2].value ,*[term for term in linear_tree])
     str_len = len(str_trace)
     token_error = p[2].value
     mensaje = "Linea {}: error en la expresion de asignacion:".format(p.lineno(2))     
     parser.errok()

def p_expression_2(p):
     'expression : simple_expression'
     global parser, str_trace, prompt_pos, token_error
     if masInfo:
          print("expression_2: ", p[1])
     p[0]= p[1]

def p_var_1(p):
        'var : ID'
        if masInfo:
             print("var_1: ", p[1])
        p[0]= Node(NodeType.VAR_1,None , p[1])
def p_var_2(p):
     'var : ID LBRACKET expression RBRACKET'
     if masInfo:
          print("var_2: ", p[1], p[2], p[3], p[4])
     p[1]= Node("var_1",None , p[1])
     p[0]= Node("var_2", [p[1],p[3]], "var_2")

def p_simple_expression_1(p):
     'simple_expression : additive_expression relop additive_expression'
     if masInfo:
          print('simple_expression_1: ', p[1], p[2], p[3])
     p[0] = Node("Nada", [p[1], p[3]], p[2].leaf)

def p_simple_expression_2(p):
        'simple_expression : additive_expression'
        if masInfo:
             print(NodeType.EXPRESSION_2, p[1])
        p[0] = p[1]

def p_relop(p):
     '''relop : LESS 
     | LESSEQUAL
     | GREATER
     | GREATEREQUAL
     | DEQUAL
     | DISTINT
        '''
     if masInfo:
          print('relop: ', p[1])
     p[0] = Node("relop", None, p[1])

def p_additive_expression_1(p):
     'additive_expression : additive_expression addop term'
     if masInfo:
          print('additive_expression_1: ', p[1], p[2].leaf, p[3])

     global parser, str_trace, prompt_pos, token_error
     if p[1] != None and p[3] != None:          
          p[0] = Node(NodeType.ADDITIVE_EXPRESSION_1, [p[1], p[3]],p[2].leaf)
     elif p[1] == None: #Configuración para preparar el error
          str_trace +=  " " + str(p[2].leaf) + " " + str(p[3].leaf)
          prompt_pos = str_trace.index(token_error)#Reubicamos el error  
     elif p[3] == None:
          linear_tree = []
          linear_tree = inOrder(p[1], linear_tree)
          str_trace_aux = p[1].leaf + " " + p[2].leaf + " " + str_trace
          str_terms = "{}" # Se agregan 2 más
          str_terms += len(linear_tree) * "{} " 
          str_trace = str_terms.format(*[term for term in linear_tree], p[2].leaf)
          str_trace = str_trace_aux
          prompt_pos = str_trace_aux.index(token_error)#Reubicamos el error      
             

def p_additive_expression_1_error(p):
        'additive_expression : additive_expression addop error term'
        global parser, str_trace, prompt_pos, token_error, mensaje
        linear_tree = []
        linear_tree = inOrder(p[1], linear_tree)
        str_terms = len(linear_tree) * "{} "
        str_terms += "{}{} {}" #Agregar 3 parametros más para considerar p[2], p[3] y p[4] que son estáticos   
        str_trace = str_terms.format(*[term for term in linear_tree], p[2].leaf, p[3].value, p[4].leaf)
        token_error = p[3].value
        mensaje = "Linea {}: Error en la expresion de adicion: ".format(p.lineno(3))
        parser.errok()

def p_additive_expression_2(p):
        'additive_expression : term'
        if masInfo:
             print('additive_expression_2: ', p[1])
        p[0] = p[1]

def p_addop(p):
        '''addop : PLUS 
                       | MINUS
        '''
        if masInfo:
             print("addop: ", p[1])
             
        p[0] = Node("addop", None, p[1])
     
def p_term_1(p):
     'term : term mulop factor'
     global parser, str_trace, prompt_pos, token_error
     if masInfo:
          print("term_1: ", p[1], p[2].leaf, p[3])
     if p[1] != None:
          p[0] = Node("term_1", [p[1], p[3]], p[2].leaf)
     else: # Hubo un error
          str_trace += " " + str(p[3].leaf) 
          
#Se queda
def p_term_1_error(p):
     'term : term mulop error factor'
     global parser, str_trace, prompt_pos, token_error, mensaje
     linear_tree = []
     linear_tree = inOrder(p[1], linear_tree)
     str_terms = len(linear_tree) * "{} "
     str_terms += "{}{} {}"
     # string de error e.g {*+ 7}
     str_trace = str_terms.format(*[term for term in linear_tree], p[2].leaf, p[3].value, p[4].leaf)
     token_error = p[3].value
     prompt_pos = str_trace.index(p[3].value)
     mensaje = "Linea {}: Error en la expresion de mult/div: ".format(p.lineno(3))
     parser.errok()
        
def p_term_2(p):
     'term : factor'
     if masInfo:
          print("term_2: ", p[1])
     if p[1] != None:
          p[0] = p[1]
     else:
          p[0] = None

def p_mulop(p):
     '''mulop : TIMES
     | DIVIDE
     '''
     if masInfo:
          print("mulop: ", p[1])
     p[0] = Node("TIMES", None, p[1])

def p_factor_1(p):
        'factor : LPAREN expression RPAREN'
        if masInfo:
             print("factor_1: ",  p[1], p[2], p[3])
        p[0] = p[2]

def p_factor_2(p):
        'factor : var'
        if masInfo:
             print("factor_2: ",  p[1].leaf)
        p[0] = p[1]

def p_factor_3(p):
        'factor : call'
        if masInfo:
             print("factor_3: ",  p[1])
        p[0] = p[1]
def p_factor_4(p):
     'factor : NUMBER'
     if masInfo:
          print("factor_4: ",  p[1])
     p[0] = Node("NUMBER", None, p[1])

def p_call(p):
        'call : ID LPAREN args RPAREN'
        if masInfo:
             print("call: ",  p[1], p[2], p[3], p[4])             
        p[0] = Node(NodeType.CALL, p[3], p[1])

def p_args(p):
     '''
     args : args_list 
     | empty '''
     new_list_args = []
     for arg in list_args:
          if arg != None:
               new_list_args.append(arg)
     list_args.clear()
     p[0] = new_list_args
   
def p_args_list_1(p):
     'args_list : args_list COMMA expression'
     if masInfo:
             print("args_list_1: ", p[1], p[2], p[3].leaf)
     global list_args
     #Pasan directamente a p_args
     list_args.append(p[1])
     list_args.append(p[3])
     
def p_args_list_2(p):
     'args_list : expression'
     if masInfo:
          print("args_list_2: ",  p[1].leaf)

     list_args.append(p[1])

def p_empty(p):
        'empty :'
        pass

def imprimeAST(arbol):
     global endentacion
     endentacion += 2
     if arbol != None:
          imprimeEspacios()
          print(arbol.leaf, arbol.type)

          if arbol.type == "compound_stmt":
               for i in range(len(arbol.children)):
                    for node in arbol.children[i]:
                         imprimeAST(node)
          elif arbol.children:
               for child in range(len(arbol.children)):
                    if arbol.children[child] != []:
                         imprimeAST(arbol.children[child])                        
          endentacion -= 2
def imprimeEspacios():
    print(" "*endentacion, end="")

parser = None
endentacion = 0

programa = ''
posicion = 0
progLong = 0

def globales(prog, pos, progL):
     global programa, posicion, progLong
     programa = prog
     posicion = pos
     progLong = progL

def parser(imprime = True):
     global programa
     global parser
     programa = programa.translate({ord('$'): None})
     
     parser = yacc.yacc()
     arbol = parser.parse(programa)
     if imprime:
          imprimeAST(arbol)
     return arbol
     
