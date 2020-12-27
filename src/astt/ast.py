from src.type_check.SymbolTable import Type


class Node:
    def __init__(self, pos,  children=None):
        self.pos = pos
        self.children = [] if children is None else children
        self.type = Type.UNKNOWN
        self.size = None
        self.const_value = None

    def __str__(self):
        return f" {self.__class__.__name__} (type: {self.type} size: {self.size})"


class Program(Node):
    def __init__(self, pos,  statements):
        super().__init__(pos, [statements])
        self.statements = statements


class Empty(Node):
    def __init__(self, pos):
        super().__init__(pos)

class Expression(Node):
    def __init__(self, pos,  expression):
        super().__init__(pos, [expression])
        self.expression = expression

class Statements(Node):
    def __init__(self, pos,  statements):
        super().__init__(pos, statements)
        self.statements = statements

class Statement(Node):
    def __init__(self, pos,  statement):
        super().__init__(pos, [statement])
        self.statement = statement

class Number(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])
        self.number = number

class IntNum(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])
        self.number = number

class FloatNum(Node):
    def __init__(self, pos,  number):
        super().__init__(pos, [number])
        self.number = number

class StringM(Node):
    def __init__(self, pos,  string):
        super().__init__(pos, [string])
        self.string = string[1:-1]

class Identifier(Node):
    def __init__(self, pos, identifier: StringM):
        super().__init__(pos, [identifier])
        self.identifier = identifier

class PartialId(Node):
    def __init__(self, pos,  identifier, index_ref):
        super().__init__(pos, [identifier, index_ref])
        self.identifier = identifier
        self.index_ref = index_ref

class IndexRef(Node):
    def __init__(self, pos,  values):
        super().__init__(pos, values)
        self.values = values

class List(Node):
    def __init__(self, pos, value_list):
        super().__init__(pos, [value_list])
        self.value_list = value_list

class ValueList(Node):
    def __init__(self, pos,  values):
        super().__init__(pos, values)
        self.values = values

class Transpose(Node):
    def __init__(self, pos,  expr):
        super().__init__(pos, [expr])
        self.expr = expr

class MatrixCreator(Node):
    def __init__(self, pos,  keyword, n):
        super().__init__(pos, [keyword, n])
        self.keyword = keyword
        self.n = n

class Logical(Node):
    def __init__(self, pos,  left, cmp, right):
        super().__init__(pos, [left, cmp, right])
        self.left = left
        self.cmp = cmp
        self.right = right

class Range(Node):
    def __init__(self, pos,  fr, to):
        super().__init__(pos, [fr, to])
        self.fr = fr
        self.to = to

class UMinus(Node):
    def __init__(self, pos,  expr):
        super().__init__(pos, [expr])
        self.expr = expr

class BinOp(Node):
    def __init__(self, pos,  left, op, right):
        super().__init__(pos, [left, op, right])
        self.left = left
        self.op = op
        self.right = right

class Assign(Node):
    def __init__(self, pos,  left, op, right: Expression):
        super().__init__(pos, [left, op, right])
        self.left = left
        self.op = op
        self.right = right

class Print(Node):
    def __init__(self, pos,  value_list):
        super().__init__(pos, [value_list])
        self.value_list = value_list

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
        self.expr = expr

# ---------------------if while for

class If(Node):
    def __init__(self, pos,  logical, statement, else_block=None):
        if else_block:
            super().__init__(pos, [logical, statement, else_block])
        else:
            super().__init__(pos, [logical, statement])
        self.logical = logical
        self.statement = statement
        self.else_block = else_block

class ElseBlock(Node):
    def __init__(self, pos,  statement):
        super().__init__(pos, [statement])
        self.statement = statement

class While(Node):
    def __init__(self, pos,  logical, statement):
        super().__init__(pos, [logical, statement])
        self.statement = statement
        self.logical = logical

class For(Node):
    def __init__(self, pos,  identifier, mrange, statement):
        super().__init__(pos, [identifier, mrange, statement])
        self.identifier = identifier
        self.mrange = mrange
        self.statement = statement
