import unittest
import mparser
import io
from contextlib import redirect_stdout
from tests.scanner_tests import get_text


def get_ast(text):
    with io.StringIO() as buf, redirect_stdout(buf):
        parser = mparser.parser
        ast = parser.parse(text)
        ast.print_tree()
        output = buf.getvalue()
    return output

class TestAst(unittest.TestCase):

    # def setUp(self):
    #     self.parser = mparser.parser

    def test_slice(self):
        text = get_text("../examples_for_tests/ast_slice.txt")
        exp_result = get_text("../examples_for_tests/ast_slice_out.txt")
        actual = get_ast(text)
        self.assertEqual(exp_result, actual, "Scanner failed")




if __name__ == '__main__':
    unittest.main()
