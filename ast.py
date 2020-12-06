class Node:
    def __init__(self, pos,  children=None):
        self.pos = pos
        self.children = [] if children is None else children


class Program(Node):
    def __init__(self, pos,  statements):
        super().__init__(pos, [statements])

class Empty(Node):
    def __init__(self, pos):
        super().__init__(pos)

class Expression(Node):
    def __init__(self, pos,  expression):
        super().__init__(pos, [expression])

class Statements(Node):
    def __init__(self, pos,  statements):
        super().__init__(pos, statements)

class Statement(Node):
    def __init__(self, pos,  statement):
        super().__init__(pos, [statement])

class Number(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])

class IntNum(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])

class FloatNum(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])

class String(Node):
    def __init__(self, pos,  string):
        super().__init__(pos, [string])

class Identifier(Node):
    def __init__(self, pos,  id):
        super().__init__(pos, [id])

class PartialId(Node):
    def __init__(self, pos,  identifier, index_ref):
        super().__init__(pos, [identifier, index_ref])

class IndexRef(Node):
    def __init__(self, pos,  values):
        super().__init__(pos, values)

class ValueList(Node):
    def __init__(self, pos,  values):
        super().__init__(pos, values)

class Transpose(Node):
    def __init__(self, pos,  expr):
        super().__init__(pos, [expr])

class MatrixCreator(Node):
    def __init__(self, pos,  keyword, n):
        super().__init__(pos, [keyword, n])

class Logical(Node):
    def __init__(self, pos,  left, cmp, right):
        super().__init__(pos, [left, cmp, right])

class Range(Node):
    def __init__(self, pos,  fr, to):
        super().__init__(pos, [fr, to])

class UMinus(Node):
    def __init__(self, pos,  expr):
        super().__init__(pos, [expr])

class BinOp(Node):
    def __init__(self, pos,  left, op, right):
        super().__init__(pos, [left, op, right])

class Assign(Node):
    def __init__(self, pos,  left, op, right):
        super().__init__(pos, [left, op, right])

class Print(Node):
    def __init__(self, pos,  value_list):
        super().__init__(pos, [value_list])

class Break(Node):
    def __init__(self, pos):
        super().__init__(pos, [])

class Continue(Node):
    def __init__(self, pos):
        super().__init__(pos, [])

class Return(Node):
    def __init__(self, pos,  expr=None):
        if expr:
            super().__init__(pos, [expr])
        else:
            super().__init__(pos, [])

# ---------------------if while for

class If(Node):
    def __init__(self, pos,  logical, statement, else_block=None):
        if else_block:
            super().__init__(pos, [logical, statement, else_block])
        else:
            super().__init__(pos, [logical, statement])

class ElseBlock(Node):
    def __init__(self, pos,  statement):
        super().__init__(pos, [statement])

class While(Node):
    def __init__(self, pos,  logical, statement):
        super().__init__(pos, [logical, statement])

class For(Node):
    def __init__(self, pos,  identifier, mrange, statement):
        super().__init__(pos, [identifier, mrange, statement])
