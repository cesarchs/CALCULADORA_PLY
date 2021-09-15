import ply.lex as lex
import ply.yacc as yacc


#lista para guardar todos los nombre de los tokens
tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'POWER'

]

# USAMOS EXPRECIONES REGULARES PARA DEFINIR QUE ES CADA TOKEN
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_POWER = r'\^'

#PLY TIENE UNA VARIABLE t_ignore ESPECIAL QUE NOS PERMITE DEFINIR CARACTERES
# QUE EL LEXER VA A IGNORAR, EN ESTE CASO SOLO IGNORAMOS EL ESPACIO
t_ignore = r' '

#TOKENS MAS COMPLICADOS, TALES COMO TOKENS QUE TIENEN MAS DE UN CARACTER DE
#LARGO, SON DEFINIDOS USANDO FUNCIONES 
# UN FLOAT ES DE UNO O MAS MUNEROS, SEGUIDOS DE UN PUNTO, SEGUIDO DE UNO O VARIOS NUMEROS DE NUEVO
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#un INT es de uno o mas numeros
def t_INT(t):
    r'\d+'
    t.value = int (t.value)
    return t

# un NAME es una variable de nombre. UNA VARIABLE PUEDE SER DE UN O MAS 
#CARACTERES DE LARGO, EL PRIMER CARACTER DEBE SER EN EL RANGO DE a-z A-Z o ser un guion bajo.
#CUALQUIER CARACTER SIGIENDO DEL PRIMERO PUEDE SER a-z A-Z 0-9 o un guion bajo
def t_NAME (t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

#SALTARSE EL TOKEN ACTUAL, Y SACAR 'CARACTER ILEGAL' USANDO LA 
# FUNCION ESPECIAL PLY t_error 
def t_error(t):
    print('CARACTER ILEGAL! XD')
    t.lexer.skip(1)

# CONSTRUIR EL ANALIZADOR LEXICO
lexer = lex.lex()

#ASEGURARSE QUE NUESTRO PARSER ENTIENDE EL CORRECTO ORDEN DE OPERACIONES.
# LA PRECEDENCIA DE OPERACIONES ES UNA VARIABLE ESPECIAL DE PLY
precedence = (
    ('left', 'PLUS','MINUS'),
    ('left', 'MULTIPLY','DIVIDE')

)

#DEFINIMOS NUESTRA GRAMATICA. NOSOTROS PERMITIMOS expressions, var_assign's y empty's
def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    #CONTRUIMOS NUESTRO ARBOL (UNA TUBLA A LA VEZ)
    p[0]= ('=',p[1],p[3])

#expressions SON RECURSIVOS 
def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression POWER expression
    '''
    #CONSTRUIMOS NUESTRO ARBOL (UNA TUBLA A LA VEZ)
    p[0]= (p[2],p[1],p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0]=p[1]

def p_expression_var (p):
    '''
    expression : NAME
    '''
    p[0]=('var',p[1])

#PARA DESPLEGARLE AL USUARIO QUE HAY UN ERROR EN LA ENTRADA, QUE NO ES 
#ACEPATADO EN LA GRAMATICA 
def p_error(p):
    print("ERROR SINTACTICO ENCONTRADO")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

#CONTRUIMOS EL PARSER
parser = yacc.yacc()

#CREAMOS EL ENTORNO SOBRE EL CUAL VAMOS A ALMACENAR Y RECUPERAR LAS VARIABLES
env = {}

#LA FUNCION "RUN" ES NUESTRA FUNCION QUE CAMINA (RECORRE) EL ARBOL QUE GENERAMOS POR MEDIO DE NUESTRO PARSER
def run (p):
    global env 
    if type(p) == tuple:
        if p[0]=='+':
            return run(p[1]) + run(p[2])
        elif p[0]=='-':
            return run(p[1]) - run(p[2])
        elif p[0]== '*':
            return run(p[1]) * run(p[2])
        elif p[0]== '/':
            return run(p[1]) / run(p[2])
        elif p[0]== '^':
            return run(p[1]) ** run(p[2])
        elif p[0]=='=':
            env[p[1]]= run(p[2])
            return ''
        elif p[0]== 'var':
            if p[1] not in env:
                return 'SE ENCONTRO UNA VARIABLE NO DECLARADA'
            else:
                return env[p[1]]
    else:
        return p





while True:
    try:
        s = input ('>>')
    except EOFError:
        break
    parser.parse(s)