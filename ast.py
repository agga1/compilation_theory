class Node:
    def __init__(self, children=None, leaf=None):
        self.children = [] if children is None else children
        # self.type = type
        # self.leaf = leaf


class Program(Node):
    def __init__(self, statements):
        super().__init__([statements])
        self.statements = statements

class Empty(Node):
    def __init__(self):
        super().__init__()

class Number(Node):
    def __init__(self, number):
        super().__init__([number])
        self.number = number

class IntNum(Node):
    def __init__(self, number):
        super().__init__([number])
        self.number = number

class FloatNum(Node):
    def __init__(self, number):
        super().__init__([number])
        self.number = number

class ValueList(Node):
    def __init__(self, values):
        super().__init__(values)
        self.values = values

class Logical(Node):
    def __init__(self, left, cmp, right):
        super().__init__([left, cmp, right])
        self.left = left
        self.cmp = cmp
        self.right = right

class Range(Node):
    def __init__(self, fr, to):
        super().__init__([fr, to])
        self.fr = fr
        self.to = to

class Expression(Node):
    def __init__(self, expression):
        super().__init__([expression])
        self.expression = expression

class Statements(Node):
    def __init__(self, statements):
        super().__init__(statements)
        self.statements = statements

class Statement(Node):
    def __init__(self, statement):
        super().__init__([statement])
        self.statement = statement


class UMinus(Node):
    def __init__(self, expr):
        super().__init__([expr])
        self.expr = expr

class BinOp(Node):
    def __init__(self, left, op, right):
        super().__init__([left, op, right])
        self.left = left
        self.op = op
        self.right = right

class Assign(Node):
    def __init__(self, left, op, right):
        super().__init__([left, op, right])
        self.left = left
        self.op = op
        self.right = right

#---------------------------- keywords
class Identifier(Node):
    def __init__(self, id):
        super().__init__([id])
        self.id = id

class String(Node):
    def __init__(self, string):
        super().__init__([string])
        self.string = string

class Print(Node):
    def __init__(self, value_list):
        super().__init__([value_list])
        self.value_list = value_list

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
        self.expr = expr


class MatrixCreator(Node):
    def __init__(self, keyword, n):
        super().__init__([keyword, n])
        self.keyword = keyword
        self.n = n

class PartialId(Node):
    def __init__(self, identifier, index_ref):
        super().__init__([identifier, index_ref])
        self.identifier = identifier
        self.index_ref = index_ref

class IndexRef(Node):
    def __init__(self, values):
        super().__init__(values)
        self.values = values

# ---------------------if while for

class If(Node):
    def __init__(self, logical, statement, else_block=None):
        if else_block:
            super().__init__([logical, statement, else_block])
        else:
            super().__init__([logical, statement])
        self.logical = logical
        self.statement = statement
        self.else_block = else_block

class ElseBlock(Node):
    def __init__(self, statement):
        super().__init__([statement])
        self.statement = statement

class While(Node):
    def __init__(self, logical, statement):
        super().__init__([logical, statement])
        self.statement = statement
        self.logical = logical


class For(Node):
    def __init__(self, identifier, range, statement):
        super().__init__([identifier, range, statement])
        self.statement = statement
        self.identifier = identifier
        self.range = range
