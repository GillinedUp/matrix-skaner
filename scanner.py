import ply.lex as lex;

keywords = {
    'if': "IF",
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = [
    'PLUSEQUALS',
    'MINUSEQUALS',
    'TIMESEQUALS',
    'DIVIDEEQUALS',
    'MATRIXPLUS',
    'MATRIXMINUS',
    'MATRIXDIVIDE',
    'MATRIXTIMES',
    'NUMBER',
    'FNUMBER'
    'ID'
] + list(keywords.values())


t_PLUSEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_TIMESEQUALS = r'\*='
t_DIVIDEEQUALS = r'/='
t_MATRIXPLUS = r'.\+'
t_MATRIXMINUS = r'.-'
t_MATRIXDIVIDE = r'./'
t_MATRIXTIMES = r'.\*'


literals = [ '+','-','*','/','(',')','=','{','}','[',']',',',';','\'',':' ]

t_ignore = ' \t'
t_ignore_comment = r'\#.*'

def t_ID(t):
    r'[a-zA-Z[a-zA-Z0-9]\w*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_FNUMBER(t):


def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


