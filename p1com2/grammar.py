# IMPORTS
# PLY
import ply.lex as lex
import ply.yacc as yacc


# lexer
#reserved words 
rw = {

    # GENERAL RW
    "END" : "END",
    "TRUE" : "TRUE",
    "FALSE" : "FALSE",

    # FUNCTIONS SENTENCE
    "FUNCTION" : "FUNCTION",
    "RETURN" : "RETURN",

    # IFELSE SENTENCE
    "IF" : "IF",
    "ELSE" : "ELSE",
    "ELSEIF" : "ELSEIF",

    # WHILE SENTENCE
    "WHILE" : "WHILE",
    "CONTINUE" : "CONTINUE",
    "BREAK": "BREAK",

    # STRUCTS
    "STRUCT" : "STRUCT",

    # NATIVES
    "PRINTLN" : "PRINTLN",
    "PRINT" : "PRINT"

}
#lista para guardar todos los nombre de los tokens
tokens = [
    "ID",

    # NATIVE VALUES
    "INTLITERAL",
    "FLOATLITERAL",
    "STRINGLITERAL",

    # SYMBOLS
    # GENERAL SYMBOLS
    "EQUALS",
    "POINT",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "LEPAR",
    "RIPAR",

    # ARITHMETIC SYMBOLS
    "POWER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIV",
    

    # LOGICAL SYMBOLS
    "AND",
    "OR",
    "NOT",

    # RELATIONAL SYMBOLS
    "GREATER",
    "LESS",
    "GREATEREQUAL",
    "LESSEQUAL",
    "EQUALSEQUALS",
    "DISTINT",

] + list(rw.values())


# USAMOS EXPRECIONES REGULARES PARA DEFINIR QUE ES CADA TOKEN

# SYMBOLS
# GENERAL SYMBOLS
t_EQUALS                = r'='
t_POINT                 = r'\.'
t_COLON                 = r':'
t_SEMICOLON             = r';'
t_COMMA                 = r','
t_LEPAR                 = r'\('
t_RIPAR                 = r'\)'

# ARITHMETIC SYMBOLS
t_PLUS                  = r'\+'
t_MINUS                 = r'-'
t_TIMES                 = r'\*'
t_DIV                   = r'/'
t_POWER = r'\^'

# LOGICAL SYMBOLS
t_AND                   = r'&&'
t_OR                    = r'\|\|'
t_NOT                   = r'!'

# RELATIONAL SYMBOLS
t_GREATER               = r'>'
t_LESS                  = r'<'
t_GREATEREQUAL          = r'>='
t_LESSEQUAL             = r'<='
t_EQUALSEQUALS          = r'=='
t_DISTINT               = r'!='


#PLY TIENE UNA VARIABLE t_ignore ESPECIAL QUE NOS PERMITE DEFINIR CARACTERES
# QUE EL LEXER VA A IGNORAR
t_ignore = r' \t'

def t_ID (t):
    r'[a-zA-Z_][a-zA-z_0-9]*'
    t.type = rw.get(t.value.upper(), 'ID')
    return t


def t_FLOATLITERAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("ERROR IN PARSE TO FLOAT")
        t.value = 0
    return t


def t_INTLITERAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print ("ERROR IN PARSE TO INT")
        t.value = 0
    return t


def t_STRINGLITERAL(t):
    r'\".*?\"'
    t.value = t.value [1:-1]
    return t


def t_MLCOMMENT(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count("\n")


def t_OLCOMMENT(t):
    r'\#.*\n'
    t.lexer.linero += 1


def t_newline(t):
    r'\n+'
    t.lexer.linero += t.value.count("\n")


def t_error(t):
    print('CARACTER ILEGAL! XD')
    t.lexer.skip(1)

# CONSTRUIR EL ANALIZADOR LEXICO
lexer = lex.lex()



lexer.input("1^ 1")


while True:
      #  s = input ('>>')
    #    lexer.input(s)
        tokenns = lexer.token()

        if not tokenns:
            break
        print(tokenns)
        









#ASEGURARSE QUE NUESTRO PARSER ENTIENDE EL CORRECTO ORDEN DE OPERACIONES.
# LA PRECEDENCIA DE OPERACIONES ES UNA VARIABLE ESPECIAL DE PLY

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALSEQUALS', 'DISTINT'),
    ('left', 'GREATEREQUAL', 'LESSEQUAL', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV','POWER'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

# SYNTACTIC ANALYSIS
#DEFINIMOS NUESTRA GRAMATICA.








"""
def p_start(t):
    '''
    start : instructions
    '''
    t[0] = t[1]
    return t[0]

def p_start(t):
    '''
    start : istructions
         | var_assign
         | empty
    '''
    print(run(p[1]))
"""