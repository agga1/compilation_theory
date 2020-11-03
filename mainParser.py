import sys
import mparser

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

    console = True
    # ------from console
    if console:
        parser = mparser.parser
        s = input('scanner >')
        while(s != 'q'):
            res = parser.parse(s)
            s = input('scanner >')