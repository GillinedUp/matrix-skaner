import sys
import Mparser
from scanner import lexer
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from io import StringIO

debug = False


def test_parser():
    try:
        filename = "all_examples"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    lexer.input(text)
    ast = parser.parse(text, lexer=lexer)

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    print(ast.printTree())

    sys.stdout = old_stdout

    with open('actual_tree', 'w') as test_file:
        test_file.write(mystdout.getvalue())


def run():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "error"
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
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
    print('Checked')


if __name__ == '__main__':

    if debug:
        test_parser()
    else:
        run()
