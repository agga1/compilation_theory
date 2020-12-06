import sys
import mparser

if __name__ == '__main__':
    # -------from file
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/ASTexample3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = mparser.parser
    ast = parser.parse(text)
    ast.print_tree()

    # typeChecker = TypeChecker()
    # typeChecker.visit(ast)

    # ------interactive console
    print("-----------------------------------")
    print("console mode -- type 'q' to quit ")
    parser = mparser.parser
    s = input('scanner >')
    while(s != 'q'):
        res = parser.parse(s)
        res.print_tree()
        s = input('scanner >')