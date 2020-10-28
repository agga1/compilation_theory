import sys
import unittest
from io import StringIO

import scanner


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = scanner.parser

    def test_group(self):
        self.check("(1+2)*4", "12\n")
        self.check("(1+(2+(3*2)-5))", "4\n")

    def test_binop(self):
        a = 3
        b = 6
        ans_add = "9\n"
        ans_sub = "-3\n"
        ans_div = "0.5\n"
        ans_mul = "18\n"
        self.check(f"{a} + {b}", ans_add)
        self.check(f"{a} - {b}", ans_sub)
        self.check(f"{a} / {b}", ans_div)
        self.check(f"{a} * {b}", ans_mul)

    def test_binop_ndarray(self):
        a = "[1,2]"
        b = "[3,4]"
        ans_add = "[4 6]\n"
        ans_dotadd = "[4 6]\n"
        ans_dotmul = "[3 8]\n"
        ans_mul = "11\n"
        self.check(f"{a} + {b}", ans_add)
        self.check(f"{a} .+ {b}", ans_dotadd)
        self.check(f"{a} .* {b}", ans_dotmul)
        self.check(f"{a} * {b}", ans_mul)

    def check(self, input, answer):
        output = self.get_ans(input)
        self.assertEqual(output, answer, f"Should be {answer}")

    def get_ans(self, input_str):
        backup = sys.stdout
        captured = StringIO()  # Create StringIO object
        sys.stdout = captured  # and redirect stdout.
        self.parser.parse(input_str)
        sys.stdout = backup  # Reset redirect.
        return captured.getvalue()




if __name__ == '__main__':
    unittest.main()
