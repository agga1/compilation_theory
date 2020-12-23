import sys
import mparser
from TypeChecker import TypeChecker

if __name__ == '__main__':
    # -------from file
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples_for_tests/ast_slice.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = mparser.parser
    ast = parser.parse(text)
    ast.print_tree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)