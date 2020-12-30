import sys
from src.parser import mparser
from src.type_check.TypeChecker import TypeChecker
from src.interpreter.interpreter import Interpreter

if __name__ == '__main__':
    # -------from file
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "../../examples/range.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = mparser.parser

    ast = parser.parse(text)
    ast.print_tree()

    typeChecker = TypeChecker()
    correct = typeChecker.check(ast, verbose=True)

    print("---------------Interpret")
    if not correct:
        print("type errors - not interpreting this mess")
    else:
        interpreter = Interpreter()
        interpreter.visit(ast)
