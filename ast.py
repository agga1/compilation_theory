class Node:
    def __init__(self, children=None):
        self.children = [] if children is None else children


class Program(Node):
    def __init__(self, statements):
        super().__init__([statements])

class Empty(Node):
    def __init__(self):
        super().__init__()

class Expression(Node):
    def __init__(self, expression):
        super().__init__([expression])

class Statements(Node):
    def __init__(self, statements):
        super().__init__(statements)

class Statement(Node):
    def __init__(self, statement):
        super().__init__([statement])

class Number(Node):
    def __init__(self, number):
        super().__init__([number])

class IntNum(Node):
    def __init__(self, number):
        super().__init__([number])

class FloatNum(Node):
    def __init__(self, number):
        super().__init__([number])

class String(Node):
    def __init__(self, string):
        super().__init__([string])

class Identifier(Node):
    def __init__(self, id):
        super().__init__([id])

class PartialId(Node):
    def __init__(self, identifier, index_ref):
        super().__init__([identifier, index_ref])

class IndexRef(Node):
    def __init__(self, values):
        super().__init__(values)

class ValueList(Node):
    def __init__(self, values):
        super().__init__(values)

class Transpose(Node):
    def __init__(self, expr):
        super().__init__([expr])

class MatrixCreator(Node):
    def __init__(self, keyword, n):
        super().__init__([keyword, n])

class Logical(Node):
    def __init__(self, left, cmp, right):
        super().__init__([left, cmp, right])

class Range(Node):
    def __init__(self, fr, to):
        super().__init__([fr, to])

class UMinus(Node):
    def __init__(self, expr):
        super().__init__([expr])

class BinOp(Node):
    def __init__(self, left, op, right):
        super().__init__([left, op, right])

class Assign(Node):
    def __init__(self, left, op, right):
        super().__init__([left, op, right])

class Print(Node):
    def __init__(self, value_list):
        super().__init__([value_list])

class Break(Node):
    def __init__(self):
        super().__init__([])

class Continue(Node):
    def __init__(self):
        super().__init__([])

class Return(Node):
    def __init__(self, expr=None):
        if expr:
            super().__init__([expr])
        else:
            super().__init__([])

# ---------------------if while for

class If(Node):
    def __init__(self, logical, statement, else_block=None):
        if else_block:
            super().__init__([logical, statement, else_block])
        else:
            super().__init__([logical, statement])

class ElseBlock(Node):
    def __init__(self, statement):
        super().__init__([statement])

class While(Node):
    def __init__(self, logical, statement):
        super().__init__([logical, statement])

class For(Node):
    def __init__(self, identifier, mrange, statement):
        super().__init__([identifier, mrange, statement])
