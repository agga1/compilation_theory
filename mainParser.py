# object oriented version

import sys
import scanner  # scanner.py is a file you create, (it is not an external library)
import mparser
file = None
lexer = scanner.lexer

def get_token():
    while True:
        tok = lexer.token()
        if tok is not None: return tok
        try:
            line = next(file)
            lexer.input(line)
        except StopIteration:
            return None

if __name__ == '__main__':
    # -------from file
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = mparser.parser
    parser.parse(text)
    # for l in text:
    #     parser.parse(l)

    console = True
    # ------from console
    if console:
        parser = mparser.parser
        s = input('scanner >')
        while(s != 'q'):
            res = parser.parse(s)
            s = input('scanner >')