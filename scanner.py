import ply.lex as lex
import sys

input = ""

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
    'ID',
    'NUMBER',
    'FNUMBER'
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
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t


def t_FNUMBER(t):
    r'^ [-+]?[0 - 9]*\.?[0 - 9]+([eE][-+]?[0-9]+)?$'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Illegal character '%s' at: '%d', '%d'" % (t.value[0], t.lineno,  find_column(t)))
    t.lexer.skip(1)


lexer = lex.lex()
