import sys
import unittest
from io import StringIO

import scanner


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = scanner.parser

    def test_group(self):
        input = "(1+2)*4"
        answer = "12\n"
        output = self.get_ans(input)
        self.assertEqual(output, answer, f"Should be {answer}")

    def test_binop_ndarray(self):
        a = "[1,2]"
        b = "[3,4]"
        ans_add = "[4 6]\n"
        ans_dotadd = "[4 6]\n"
        ans_dotmul = "[3 8]\n"
        ans_mul = "11\n"
        output = self.get_ans(f"{a} + {b}")
        self.assertEqual(output, ans_add, f"Should be {ans_add}")
        output = self.get_ans(f"{a} .+ {b}")
        self.assertEqual(output, ans_dotadd, f"Should be {ans_dotadd}")
        output = self.get_ans(f"{a} .* {b}")
        self.assertEqual(output, ans_dotmul, f"Should be {ans_dotmul}")
        output = self.get_ans(f"{a} * {b}")
        self.assertEqual(output, ans_mul, f"Should be {ans_mul}")

    def test_binop(self):
        a = 3
        b = 6
        ans_add = "9\n"
        ans_sub = "-3\n"
        ans_div = "0.5\n"
        ans_mul = "18\n"
        output = self.get_ans(input_str=f"{a} + {b}")
        self.assertEqual(output, ans_add, f"Should be {ans_add}")
        output = self.get_ans(input_str=f"{a} - {b}")
        self.assertEqual(output, ans_sub, f"Should be {ans_sub}")
        output = self.get_ans(input_str=f"{a} / {b}")
        self.assertEqual(output, ans_div, f"Should be {ans_div}")
        output = self.get_ans(input_str=f"{a} * {b}")
        self.assertEqual(output, ans_mul, f"Should be {ans_mul}")

    def get_ans(self, input_str):
        backup = sys.stdout
        captured = StringIO()  # Create StringIO object
        sys.stdout = captured  # and redirect stdout.
        self.parser.parse(input_str)
        sys.stdout = backup  # Reset redirect.
        return captured.getvalue()




if __name__ == '__main__':
    unittest.main()
