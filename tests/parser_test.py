import sys
import unittest
from io import StringIO
import mparser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = mparser.parser

    def test_group(self):
        self.assertAccepted("(1+2)*4;")
        self.assertAccepted("(1+(2+(3*2)-5));")

    def test_binop(self):
        self.assertAccepted(f"a + 3;")
        self.assertAccepted(f"2 - b;")
        self.assertAccepted(f"a / b;")
        self.assertAccepted(f"a * b;")
        self.assertAccepted(f"a .+ b;")
        self.assertAccepted(f"a .- b;")
        self.assertAccepted(f"a ./ b;")
        self.assertAccepted(f"a .* b;")

    def test_assign(self):
        self.assertAccepted(f"a += b;")
        self.assertAccepted(f"a = b;")
        self.assertAccepted(f"a[1:n,y] = b;")
        self.assertAccepted(f"a[1,3] = b;")
        self.assertAccepted(f"a[1:5,3] = b;")
        self.assertAccepted(f"a[1:5,3] += b;")

    def test_if(self):
        self.assertAccepted("if(2==3) print \"hi\";")
        self.assertAccepted("if(2==3) print \"hi\"; else a = 4;")
        self.assertAccepted("if(2==3) {print \"hi\";} else a = 4;")
        self.assertFailed("if(2==3) {print \"hi\"; else a = 4;}")

    def test_for(self):
        self.assertAccepted("for i = 1:10 print 3;")
        self.assertAccepted("for i = n:10 -3;")
        self.assertAccepted("for i = 1:n -3;")
        self.assertAccepted("for i = 1:10 {print 3;}")


    def assertAccepted(self, input):
        output = self.get_ans(input)
        self.assertEqual(output, "", f"Got syntax error")

    def assertFailed(self, input):
        output = self.get_ans(input)
        self.assertNotEqual(output, "", f"Expression falsely accepted")

    def get_ans(self, input_str):
        backup = sys.stdout
        captured = StringIO()  # Create StringIO object
        sys.stdout = captured  # and redirect stdout.
        self.parser.parse(input_str)
        sys.stdout = backup  # Reset redirect.
        return captured.getvalue()




if __name__ == '__main__':
    unittest.main()
