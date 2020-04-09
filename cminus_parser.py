
# -*- enconding: utf-8 -*-

# Referencia: http://www.juanjoconti.com.ar/2007/11/02/minilisp-un-ejemplo-de-ply/

import ply.yacc as yacc
from cminus_lexer import tokens
import cminus_lexer
import sys
start = 'compound_stmt'

list_args = []
list_local_declarations = []
list_statement_list = []
list_param_list = []
var_decl = None

class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type #Puede tener el token
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf #Tiene el valor del Lexema

VERBOSE = 1
masInfo = True
'''
def p_program(p):
	'program : declaration_list'
	pass

def p_declaration_list_1(p):
	'declaration_list : declaration_list declaration'
	 #p[0] = p[1] + p[2]  
	pass

def p_declaration_list_2(p):
	'declaration_list : declaration'
	pass

def p_declaration(p):
	'  declaration : var_declaration | fun_declaration
	pass'''

def p_var_declaration_1(p):
     'var_declaration : type_specifier ID SEMICOLON'
     p[1] = Node("type_specifier", None, p[1])
     if masInfo:
          print("var_declaration_1: ", p[1], p[2], p[3])
     global var_decl
     var_decl = Node("var_declaration_1", [p[1]], p[2])
     p[0] = var_decl
        
'''
def p_var_declaration_2(p):
     'var_declaration : type_specifier ID LBRACKET NUMBER RBRACKET SEMICOLON'
     p[2] = Node("var_1", None, p[2])
     p[4] = Node("num", None, p[4])
     if masInfo:
          print("var_declaration_2: ", p[1].leaf, p[2].leaf, p[3], p[4].leaf, p[5], p[6])
     p[0] = Node("var_declaration_2", [p[1],p[2], p[4]], "var_declaration_2") '''


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
     p[4] = Node("params",p[4], "params")
     p[2] = Node("identifier", None, p[2])
     p[0] = Node("fun_declaration", [p[1],p[2], p[4], p[6]], "fun_declaration")


def p_params_1(p):
     'params : param_list'
     if masInfo:
          print("params_1: ", p[1])
     new_list_param = []
     for param in list_param_list:
          if param != None:
               print(param.leaf)
               new_list_param.append(param)
     list_param_list.clear()
     
     p[0] =  new_list_param 
     
def p_params_2(p):
     'params : VOID'
     p[0] = Node("type-specifier", None, p[1])

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
     p[0] = Node("param_1",[p[2]], p[1].leaf)

def p_param_2(p):
     'param : type_specifier ID LBRACKET RBRACKET'
     if masInfo:
          print("param_2: ", p[1].leaf, p[2], p[3], p[4])
     var_1 = Node("var_1", p[2], "var_1")
     p[0] = Node("param_2", [p[1], var_1] ,"param_2")

def p_compound_stmt(p):
     'compound_stmt : LBLOCK local_declarations RBLOCK'
     if masInfo:
          print("compund_stmt: ", p[1], p[2], p[3])
     new_list_local_declarations = []
     #new_statement_list = []
     for item in list_local_declarations:
          if item != None:
               print("for_1: ", item.leaf, item.children)
               new_list_local_declarations.append(item)
     list_local_declarations.clear()
     #for item in list_statement_list:
     #     if item != None:
     #          print("for_2: ", item)
     #          new_statement_list.append(item.leaf)
     #list_statement_list.clear()
     
     #local_declarations = Node("local_declarations", None, new_list_local_declarations)
     #statement_list = Node("statement_list", None, new_statement_list)
     p[0] = Node("compound_stmt", new_list_local_declarations,
                 "compound_stmt")
def p_local_declarations_1(p):
     'local_declarations : local_declarations var_declaration'
     if masInfo:
          print("local_declarations_1: ", p[1], p[2].leaf, p[2].children)
     global list_local_declarations
     list_local_declarations.append(p[1])
     list_local_declarations.append(p[2])
     #if p[1] != None:
     #p[0] = Node("local_declarations_1", [p[1]], p[2].leaf)
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
          print("statement: ", p[1].children)
     p[0] = p[1]

def p_expression_stmt_1(p):
     'expression_stmt : expression SEMICOLON'
     if masInfo:
          print("expression_stmt_1: ", p[1].leaf, p[2])
     p[0] = p[1]
 

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
         # for i in range(len(p[3].children)):
          #     print("Papa: {} Hijos: {}".
           #          format(p[3].leaf, p[3].children[i].leaf) )
          #for i in range(len(p[5].children)):
           #    print("Papa: {} Hijos: {}".
            #         format(p[5].leaf, p[5].children[i].leaf) )

     p[0] = Node("iteration_stmt", [p[3], p[5]], p[1])

def p_return_stmt_1(p):
     'return_stmt : RETURN SEMICOLON'
     if masInfo:
          print("return_stmt_1: ", p[1], p[2])
     p[0] = Node("return_stmt_1",None ,p[1])

def p_return_stmt_2(p):
     'return_stmt : RETURN expression SEMICOLON'
     if masInfo:
          print("return_stmt_2: ", p[1],[p[2]], p[3])
     p[0] = Node("return_stmt_2",[p[2]],p[1])
# Impresion Nodo
def p_expression_1(p):
        'expression : var EQUAL expression'
        if masInfo:
             print("expression_1: ", p[1].leaf, p[2], p[3].leaf)
        else:
             print(p[2])
        p[0]= Node("expression_1", [p[1],p[3]], p[2])
        print("Papaito '{}'   Hijos '{}' '{}'".
              format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )

def p_expression_2(p):
        'expression : simple_expression'
        if masInfo:
             print("expression_2: ", p[1])
            # for i in range(len(p[1].children)):
             #     print("Papa: {} Hijos: {} {}".
             #          format(p[1].leaf, p[1].children[i].leaf, p[1].children[i].leaf) )
        p[0]= p[1]        

def p_var_1(p):
        'var : ID'
        if masInfo:
             print("var_1: ", p[1])
        else:
             print(p[1])
        p[0]= Node("var_1",None , p[1])
def p_var_2(p):
     'var : ID LBRACKET expression RBRACKET'
     if masInfo:
          print("var_2: ", p[1], p[2], p[3], p[4])
     else:
          print(p[1], p[2], p[3], p[4])
     p[1]= Node("var_1",None , p[1])
     p[0]= Node("var_2", [p[1],p[3]], "var_2")

def p_simple_expression_1(p):
        'simple_expression : additive_expression relop additive_expression'
        if masInfo:
             print('simple_expression_1: ', p[1], p[2], p[3])
        p[0] = Node("simple_expression_1", [p[1], p[3]], p[2].leaf)
        print("Papa '{}'   Hijos '{}' '{}'".
              format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )

def p_simple_expression_2(p):
        'simple_expression : additive_expression'
        if masInfo:
             print('simple_expression_2: ', p[1])
        p[0] = p[1]
        #print("Papa2 '{}'   Hijos '{}' '{}'".
         #     format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )

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
        else:
             print( p[1])
        p[0] = Node("relop", None, p[1])
# Impresion Nodo
def p_additive_expression_1(p):
        'additive_expression : additive_expression addop term'
        if masInfo:
             print('additive_expression_1: ', p[1].leaf, p[2].leaf, p[3].leaf)
        p[0] = Node('additive_expression_1', [p[1], p[3]],p[2].leaf)
        print("Papa '{}'   Hijos '{}' '{}'".
              format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )
        
#Aqui 3
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
        else:
             print(p[1])
             
        p[0] = Node("addop", None, p[1])
     
## Impresion de Nodo
def p_term_1(p):
        'term : term mulop factor'
        if masInfo:
             print("term_1: ", p[1].leaf, p[2].leaf, p[3].leaf)
        p[0] = Node("term_1", [p[1], p[3]], p[2].leaf)
        print("Papa '{}'   Hijos '{}' '{}'".
              format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )

def p_term_2(p):
     'term : factor'
     if masInfo:
          print("term_2: ", p[1])
     p[0] = p[1]

def p_mulop(p):
        '''mulop : TIMES
                        | DIVIDE
        '''
        if masInfo:
             print("mulop: ", p[1])
        else:
             print(p[1])
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
        else:
             print(p[1])
        p[0] = Node("NUMBER", None, p[1])

def p_call(p):
        'call : ID LPAREN args RPAREN'
        if masInfo:
             print("call: ",  p[1], p[2], p[3], p[4])             
        p[0] = Node("call", [p[1], p[3]], "call")

def p_args(p):
     '''
     args : args_list 
     | empty '''
     new_list_args = []
     if masInfo:
          for arg in list_args:
               if arg != None:
                    new_list_args.append(arg)
                    print("argui: ", arg.leaf)
     list_args.clear()
     p[0] = new_list_args
   
def p_args_list_1(p):
     'args_list : args_list COMMA expression'
     if masInfo:
             print("args_list_1: ", p[1], p[2], p[3].leaf)
     else:
          print( p[1], p[2], p[3])
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

def p_error(p):
	#print str(dir(p))
	#print str(dir(cminus_lexer))
        if VERBOSE:
                if p is not None:
                        print("Syntax error at line {}  Unexpected token  {}"
                              .format( str(p.lexer.lineno),str(p.value)) )
                else:
                        print("Syntax error at line: "
                              .format( str(cminus_lexer.lexer.lineno)))
        else:
             raise Exception('syntax', 'error')
		
def imprimeAST(arbol):
     global endentacion
     endentacion += 2
     if arbol != None:
          imprimeEspacios()

          print(arbol.leaf)
          if arbol.type == "call":
               endentacion += 2
               imprimeEspacios()
               print(arbol.children[0])
               for i in range(len(arbol.children[1])):
                    imprimeEspacios()
                    print(arbol.children[1][i].leaf)
               endentacion -= 2
          elif arbol.children:
               for child in range(len(arbol.children)):
                    if arbol.children[child] != []:
                        # print(":) ", var_decl)
                         #print(":) ", var_decl.leaf)
                         #print(":) ", var_decl.children)
                         imprimeAST(arbol.children[child])                        
          endentacion -= 2
     else:
          print("arbol vacio: ")
def imprimeEspacios():
    print(" "*endentacion, end="")

parser = yacc.yacc()
endentacion = 0

if __name__ == '__main__':

     if (len(sys.argv) > 1):
          fin = sys.argv[1]
     else:
          fin = 'examples/input.c'

     f = open(fin, 'r')
     data = f.read()
     print(data)
     arbol = parser.parse(data, tracking=True)

     imprimeAST(arbol)
     
