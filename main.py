# import sys
# from scanner import lexer, find_column
#
# if __name__ == '__main__':
#
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     text = file.read()
#     lexer.input(text)  # Give the lexer some input
#
#     # Tokenize
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break  # No more input
#         column = find_column(lexer.lexdata, tok)
#         print("(%d,%d): %s(%s)" % (tok.lineno, column, tok.type, tok.value))
#


import sys
import Mparser
from scanner import lexer


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    lexer.input(text)
    parser.parse(text, lexer=lexer)
