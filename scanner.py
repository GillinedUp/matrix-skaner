import ply.lex as lex

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
             'ADDASSIGN',
             'SUBASSIGN',
             'MULASSIGN',
             'DIVASSIGN',
             'DOTADD',
             'DOTSUB',
             'DOTDIV',
             'DOTMUL',
             'ID',
             'INT',
             'FLOAT',
             'STRING',
             'EQUAL',
             'NOTEQUAL',
             'TRANSP',
             'LESSEQUAL',
             'GREATEREQUAL',

         ] + list(keywords.values())

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_DOTADD = r'.\+'
t_DOTSUB = r'.-'
t_DOTDIV = r'./'
t_DOTMUL = r'.\*'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_TRANSP = r'\''
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='


literals = ['+', '-', '*', '/', '(', ')', '=', '{', '}', '[', ']', ',', ';', ':', '<', '>']

t_ignore = ' \t'
t_ignore_comment = r'\#.*'


def t_STRING(t):
    r'".+"'
    t.value = str(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t


def t_FLOAT(t):
    r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'-?\b[0-9]+\b'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(my_text, token):
    line_start = my_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Unrecognized token '%s' at: '%d', '%d'"
          % (t.value[0], t.lineno, find_column(lexer.lexdata, t)))
    t.lexer.skip(1)


lexer = lex.lex()
