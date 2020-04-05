
# -*- enconding: utf-8 -*-

# Referencia: http://www.juanjoconti.com.ar/2007/11/02/minilisp-un-ejemplo-de-ply/

import ply.yacc as yacc
from cminus_lexer import tokens
import cminus_lexer
import sys

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
	pass

def p_var_declaration_1(p):
	'var_declaration : type_specifier ID SEMICOLON'
	pass

def p_var_declaration_2(p):
	'var_declaration : type_specifier ID LBRACKET NUMBER RBRACKET SEMICOLON'
	pass

def p_type_specifier_1(p):
	'type_specifier : INT'
	pass

def p_type_specifier_2(p):
	'type_specifier : VOID'
	pass


def p_fun_declaration(p):
	'fun_declaration : type_specifier ID LPAREN params RPAREN compount_stmt'
	pass


def p_params_1(p):
	'params : param_list'
	pass


def p_params_2(p):
	'params : VOID'
	pass

def p_param_list_1(p):
	'param_list : param_list COMMA param'
	pass

def p_param_list_2(p):
	'param_list : param'
	pass

def p_param_list_3(p):
	'param_list : empty'
	pass

def p_param_1(p):
	'param : type_specifier ID'
	pass

def p_param_2(p):
	'param : type_specifier ID LBRACKET RBRACKET'
	pass

def p_compount_stmt(p):
	'compount_stmt : LBLOCK local_declarations statement_list RBLOCK'
	pass

def p_local_declarations_1(p):
	'local_declarations : local_declarations var_declaration'
	pass

def p_local_declarations_2(p):
	'local_declarations : empty'
	pass

def p_statement_list_1(p):
	'statement_list : statement_list statement'
	pass

def p_statement_list_2(p):
	'statement_list : empty'	
	pass

def p_statement(p):
	statement : expression_stmt
				| compount_stmt
				| selection_stmt
				| iteration_stmt
				| return_stmt
	
	pass

def p_expression_stmt_1(p):
	'expression_stmt : expression SEMICOLON'
	pass

def p_expression_stmt_2(p):
	'expression_stmt : SEMICOLON'
	pass

def p_selection_stmt_1(p):
	'selection_stmt : IF LPAREN expression RPAREN statement'
	pass

def p_selection_stmt_2(p):
	'selection_stmt : IF LPAREN expression RPAREN statement ELSE statement'
	pass

def p_iteration_stmt(p):
	'iteration_stmt : WHILE LPAREN expression RPAREN statement'
	pass

def p_return_stmt_1(p):
	'return_stmt : RETURN SEMICOLON'
	pass

def p_return_stmt_2(p):
	'return_stmt : RETURN expression SEMICOLON'
	pass'''
# Impresion Nodo
def p_expression_1(p):
        'expression : var EQUAL expression'
        if masInfo:
             print("expression_1: ", p[1].leaf, p[2], p[3])
        else:
             print(p[2])
        p[0]= Node("expression_1", [p[1],p[3]], p[2])
        print("Papaito '{}'   Hijos '{}' '{}'".
              format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )

def p_expression_2(p):
        'expression : simple_expression'
        if masInfo:
             print("expression_2: ", p[1].leaf)
             for i in range(len(p[1].children)):
                  print("Papa: {} Hijos: {} {}".
                        format(p[1].leaf, p[1].children[i].leaf, p[1].children[i].leaf) )
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
     identifier= Node("var_1",None , p[1])
     p[0]= Node("var_2", [identifier,p[3]], "var_2")

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
             print('simple_expression_2: ', p[1].leaf)
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
             print('additive_expression_2: ', p[1].leaf)
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
          print("term_2: ", p[1].leaf)
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
             print("factor_3: ",  p[1], p[1].children[0])
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
        else:
             print(p[1], p[2], p[3], p[4])
        p[0] = Node("call", [p[1], p[3]], "call")

def p_args(p):
        '''args : args_list
                          | empty
        '''
        if masInfo:
             print("args: ", p[1])
        p[0] = p[1]

def p_args_list_1(p):
     'args_list : args_list COMMA expression'
     if masInfo:
             print("args_list_1: ", p[1], p[2], p[3].leaf)
     else:
          print( p[1], p[2], p[3])
     aux_list = []
     aux_list.append(p[3].leaf)
     arguments = [arg for arg in (p[1] + aux_list)]
     print("argui: ", arguments)
     p[0] = arguments
     #p[0] = Node("args_list_1", [p[1], p[3]],
     #print("Papa '{}'   Hijos '{}' '{}'".
     #     format(p[0].leaf, p[0].children[0].leaf, p[0].children[1].leaf) )
def p_args_list_2(p):
        'args_list : expression'
        if masInfo:
             print("args_list_2: ",  p[1])
        p[0] = [arg for arg in str(p[1].leaf)]

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
          '''
          if arbol.exp == TipoExpresion.OP:
          print("OP: ", arbol.op)
          elif arbol.exp == TipoExpresion.CONST:
          print("CONST: ", arbol.val," ")
          else:
          print("ExpNode de tipo desconocido")'''
          print(arbol.leaf)
          if arbol.type == "call":
               #endentacion += 2
               imprimeEspacios()
               print(arbol.children[0])
               for i in range(len(arbol.children[1])):
                    imprimeEspacios()
                    print(arbol.children[1][i])
               print()
               endentacion -= 2
               return
          '''if arbol.type == "type_2":
               endentacion += 2
               imprimeEspacios()
               print(arbol.children[0])
               for i in range(len(arbol.children[1])):
                    imprimeEspacios()
                    print(arbol.children[1][i])
               endentacion -= 2
               return'''
          if(arbol.children != []):
               imprimeAST(arbol.children[0])
               imprimeAST(arbol.children[1])
          endentacion -= 2
    
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
     
