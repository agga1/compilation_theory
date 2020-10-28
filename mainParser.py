# object oriented version

import sys
import scanner  # scanner.py is a file you create, (it is not an external library)
if __name__ == '__main__':
    # -------from file
    # TODO currently parsing by lines, should parse whole file and recognize ';'
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/if.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.readlines()
    parser = scanner.parser
    for line in text:
        parser.parse(line)

    console = True
    # ------from console
    if console:
        parser = scanner.parser
        s = input('scanner >')
        while(s != 'q'):
            res = parser.parse(s)
            s = input('scanner >')