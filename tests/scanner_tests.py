import sys
import unittest
import scanner


class TestScanner(unittest.TestCase):

    def test_whole(self):
        test_name = "../example.txt"
        answer_name = "../answer.txt"
        try:
            test_file = open(test_name, "r")
            text = test_file.read()
            test_file.close()
            answer_file = open(answer_name, "r")
            answer = answer_file.read()
            answer_file.close()
        except IOError:
            print("Cannot open files")
            sys.exit(0)

        lexer = scanner.lexer
        lexer.input(text)  # Give the lexer some input
        ans = ""
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            ans += ("(%d): %s(%s)\n" % (tok.lineno, tok.type, tok.value))
        self.assertEqual(ans, answer, "Should be 6")


if __name__ == '__main__':
    unittest.main()
