import numpy as np

def expression_factory(num_or_ndarray):

    if isinstance(num_or_ndarray, np.ndarray):
        return ExpressionList(num_or_ndarray)
    else:
        return Expression(num_or_ndarray)

class Expression:

    def __init__(self, value):
        self.value = value

    def eval(self, operator: str, other):
        if operator == '+':
            return self + other
        elif operator == '-':
            return self - other
        elif operator == '*':
            return self * other
        elif operator == '/':
            return self / other
        return None

    def __add__(self, o):
        return self.value + o.value

    def __sub__(self, o):
        return self.value - o.value

    def __mul__(self, o):
        return self.value * o.value

    def __truediv__(self, o):
        return self.value / o.value

    def __str__(self):
        return str(self.value)

class ExpressionList(Expression):

    def __init__(self, value):
        super(ExpressionList, self).__init__(value)
        assert isinstance(self.value, np.ndarray)

    def eval(self, operator: str, other):
        ans = super().eval(operator, other)
        if ans is None:
            if operator == '.+':
                return self + other
            elif operator == '.-':
                return self - other
            elif operator == '.*':  # careful! a*b works like dot multiplication in numpy!
                return self.value * other.value
            elif operator == './':
                return self / other
            return None
        return ans

    def __mul__(self, o):
        return self.value.dot(o.value)

    def transpose(self):
        return self.value.T
