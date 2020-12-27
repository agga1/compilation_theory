import sys
import mparser
from type_check.TypeChecker import TypeChecker
from interpreter import Interpreter

if __name__ == '__main__':
    # -------from file
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/ASTexample1.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = mparser.parser
    print("---------------ast")
    ast = parser.parse(text)
    ast.print_tree()
    print("---------------TypeCheck")
    typeChecker = TypeChecker()
    correct = typeChecker.check(ast)
    print("---------------Interpret")
    if not correct:
        print("type errors - not interpreting this mess")
    else:
        interpreter = Interpreter()
        interpreter.visit(ast)
