import sys
import Mparser
from scanner import lexer
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker


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
    ast = parser.parse(text, lexer=lexer)
    print(ast.printTree())
    typeChecker = TypeChecker()
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    print('Checked')

