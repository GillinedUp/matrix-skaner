import sys
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
             'FLOAT'
         ] + list(keywords.values())

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_DOTADD = r'.\+'
t_DOTSUB = r'.-'
t_DOTDIV = r'./'
t_DOTMUL = r'.\*'

literals = ['+', '-', '*', '/', '(', ')', '=', '{', '}', '[', ']', ',', ';', '\'', ':']

t_ignore = ' \t'
t_ignore_comment = r'\#.*'


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
    print("Unrecognized token '%s' at: '%d', '%d'" % (t.value[0], t.lineno, find_column(text, t)))
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)  # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        column = find_column(text, tok)
        print("(%d,%d): %s(%s)" % (tok.lineno, column, tok.type, tok.value))
