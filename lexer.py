

# -*- encondig: utf-8 -*-

# --------------------------------------
# c minus lexer
# --------------------------------------

# NEW: 	comments in classic C
# 		comentario in C99 standard

import ply.lex as lex

no_of_characters_passed = 0
saved_string = ''
data = ''
stack_of_error_messages = []

class ErrorMessage:
        def __init__(self, message, line_of_code_content ,pos_prompt):
                self.message = message
                self.line_of_code_content = line_of_code_content
                self.pos_prompt = pos_prompt
        

# list of tokens
tokens = (

	# Reserverd words
	'ELSE',
	'IF',
	'INT',
	'RETURN',
	'VOID',
	'WHILE',
	
	# Symbols
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'LESS',
	'LESSEQUAL',
	'GREATER',
	'GREATEREQUAL',
	'ASSIGN',
	'DEQUAL',
	'DISTINT',
	'SEMICOLON',
	'COMMA',
	'LPAREN',
	'RPAREN',
	'LBRACKET',
	'RBRACKET',
	'LBLOCK',
	'RBLOCK',
        'COMMENTS',

	# Others	
	'ID', 
	'NUMBER',
        'SPACES',
        # Tokens de Error
        'ERROR'
)
# Regular expressions rules for a simple tokens
def t_ASSIGN(t):
        r'\='
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_PLUS(t):
        r'\+'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_MINUS(t):
        r'\-'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_TIMES(t):
        r'\*'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_DIVIDE(t):
        r'\/'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_LESS(t):
        r'\<'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_GREATER(t):
        r'\>'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_SEMICOLON(t):
        r'\;'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_COMMA(t):
        r'\,'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_RPAREN(t):
        r'\)'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_LPAREN(t):
        r'\('
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t
def t_LBRACKET(t):
        r'\['
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_RBRACKET(t):
        r'\]'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_LBLOCK(t):
        r'\{'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_RBLOCK(t):
        r'\}'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t




def t_ELSE(t):
        r'else'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string = t.value
        return t

def t_IF(t):
        r'if'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string = t.value
        return t

def t_INT(t):
        r'int'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t
	
def t_RETURN(t):
        r'return'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        return t
	
def t_VOID(t):
        r'void'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t
	
def t_WHILE(t):
        r'while'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t
	
def t_NUMBER(t):
        r'[0-9][0-9]*\b'
        t.value = int(t.value)
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(str(t.value))
        saved_string += str(t.value)
        return t

def t_ERROR(t):
        r'([a-zA-Z]*(%|\*|\.|[0-9]|_|-)[a-zA-Z]*)+|([0-9]+([a-zA-Z]|%|\.|_|-))+'
        #Caracteres especiales que no deberia llevar un identificador
        special_characters = ['%','_','-','.','1','2','3','4','5','6','7','8','9','0']
        
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(str(t.value))
        saved_string += str(t.value)
        prompt_error = ''
        
        for i in range(len(saved_string)):
                c = saved_string[i]
                if len([x for x in special_characters if x == c]) == 1:
                        prompt_error += '^'
                        break
                prompt_error += ' '
        errorMessage = ErrorMessage("Linea {}: Error en la formacion de un ID/NUMBER".format(t.lexer.lineno),
                                    saved_string, prompt_error)
        stack_of_error_messages.append(errorMessage)
       # print(prompt_error)
        #print(saved_string)
        return t

def t_ID(t):
        r'[a-zA-Z][a-zA-Z]*'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_LESSEQUAL(t):
        r'<='
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_GREATEREQUAL(t):
        r'>='
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string = t.value
        return t

def t_DEQUAL(t):
        r'=='
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_DISTINT(t):
        r'!='
        global no_of_characters_passed, saved_string
        no_of_characters_passed += len(t.value)
        saved_string += t.value
        return t

def t_newline(t):
        r'\n+'
        global no_of_characters_passed, saved_string
        no_of_characters_passed = 0
        saved_string = ''
        t.lexer.lineno += len(t.value)
#Blank spaces ignored
def t_SPACES(t):
        r'\s'
        global no_of_characters_passed, saved_string
        no_of_characters_passed += 1
        saved_string += t.value
        pass

def t_COMMENTS(t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        global no_of_characters_passed
        no_of_characters_passed = len(t.value)
        return t

def t_comments_C99(t):
	r'//(.)*?\n'
	t.lexer.lineno += 1

def t_error(t):
        global data, saved_string
        print("Illegal character {} line {}  pos {}".format(t.value[0], t.lexer.lineno ,no_of_characters_passed + 1) )
        lexpos= t.lexer.lexpos
        line_of_code_content, prompt_error = genMessageAndPromptError(no_of_characters_passed,
                                                                      lexpos, saved_string)
        messageError = ErrorMessage("Error Sintactico",line_of_code_content, prompt_error)
        stack_of_error_messages.append(messageError)
        t.lexer.skip(1)
def genMessageAndPromptError(spaces, lexpos, saved_string):
        pos_prompt_error = ''
        for i in range(spaces):
                pos_prompt_error += ' '
        pos_prompt_error += "^"
        
        while data[lexpos] != '\n':
                saved_string += data[lexpos]
                lexpos += 1
        
        return saved_string, pos_prompt_error

def test(data, lexer):
        lexer.input(data)
        while True:
                tok = lexer.token()
                if not tok:
                        break
                if tok.type == 'ERROR':
                        print("{}  ''".format(tok.type))
                else:
                        print("{}  {}".format(tok.type, tok.value))
        # Print all the token Errors
        print("\n")
        for message_error in stack_of_error_messages:
                print(message_error.message)
                print(message_error.line_of_code_content)
                print(message_error.pos_prompt)
lexer = lex.lex()

# Test 
if __name__ == '__main__':
        f = open('data.c', 'r')
        data = f.read()
        # Build lexer and try on
        lexer.input(data)
        test(data, lexer)


