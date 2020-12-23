import sys
import unittest
import scanner


def get_text(filename):
    with open(filename, "r") as file:
        text = file.read()
    return text

def get_lexer_result(text):
    lexer = scanner.lexer
    lexer.input(text)
    result = ""
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        result += ("(%d): %s(%s)\n" % (tok.lineno, tok.type, tok.value))
    return result

class TestScanner(unittest.TestCase):

    def test_whole(self):
        text = get_text("../examples_for_tests/scanner1.txt")
        exp_result = get_text("../examples_for_tests/scanner1_out.txt")
        actual = get_lexer_result(text)
        self.assertEqual(actual, exp_result, "Scanner failed")


if __name__ == '__main__':
    unittest.main()
