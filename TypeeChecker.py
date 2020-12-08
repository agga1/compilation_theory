from SymbolTable import SymbolTable, Symbol
from ast import *


class NodeVisitor(object):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node):
        for child in node.children:
            if child:
                self.visit(child)


class TypeChecker(NodeVisitor):

    def put_symbol(self, name, symbol_type, symbol_size=None):
        self.symbol_table.put(name, Symbol(name, symbol_type, symbol_size))

    def visit_and_push_scope(self, node, scope_name):
        self.symbol_table.push_scope(scope_name)
        for ch in node.children:
            self.visit(ch)
        self.symbol_table.pop_scope()

    def visit_Program(self, node: Program):
        self.visit_and_push_scope(node, "program")

    # Lists, id --------------------------
    def visit_Identifier(self, node: Identifier):
        symbol = self.symbol_table.get(node.identifier)
        if symbol is not None:
            node.type = symbol.type
            node.size = symbol.size
        else:
            node.type = Type.NULL  # id doesnt yet exist

    def visit_PartialId(self, node: PartialId):
        self.visit(node.identifier)
        if node.identifier.type == Type.NULL:
            error(node.pos, "accessing uninitialized memory")
        elif node.identifier.type not in [Type.STRING, Type.MATRIX, Type.VECTOR]:
            error(node.pos, f"cannot slice this element - element of type {node.identifier.type}")
        else:  # check if within size
            self.visit(node.index_ref) # errors for 3 or above
            if len(node.index_ref.values) == 2:
                if node.identifier.type != Type.MATRIX: # check if matrix
                    error(node.pos, "too many indexes for 1 dimensional variable")
                if node.index_ref.const_value is not None: # check if constants available
                    row, col = node.index_ref.const_value
                    if node.identifier.size[0] <= row or node.identifier.size[1] <= col:
                        error(node.pos, f"index [{row}, {col}] out of bounds")
            elif len(node.index_ref.values) == 1 and node.index_ref.const_value is not None:  # index reference is a constant value
                ind = node.index_ref.const_value
                if node.identifier.type == Type.STRING and node.identifier.size <= ind:
                    error(node.pos, "string index out of bounds")
                if node.identifier.type == Type.VECTOR and node.identifier.size <= ind:
                    error(node.pos, "vector index out of bounds")
                if node.identifier.type == Type.MATRIX and node.identifier.size[0] <= ind:
                    error(node.pos, "matrix index out of bounds")

    def visit_IndexRef(self, node: IndexRef):
        self.generic_visit(node)
        if len(node.values) > 2:
            error(node.pos, "too many indexes given")
            return
        if len(node.values) == 1 and node.values[0].const_value:  # assign constant value is reference is a constant
            node.const_value = node.values[0].const_value
        if len(node.values) == 2 and node.values[0].const_value and node.values[1].const_value:
            node.const_value = (node.values[0].const_value, node.values[1].const_value)

    def visit_List(self, node: List):
        if not node.value_list:
            node.type = Type.NULL
        else:
            self.visit(node.value_list)
            node.type = node.value_list.type
            node.size = node.value_list.size

    def visit_ValueList(self, node: ValueList):
        self.generic_visit(node)
        if node.values[0].type not in [Type.VECTOR, Type.MATRIX]:
            node.type = Type.VECTOR
            node.size = len(node.values)
        elif node.values[0].type == Type.VECTOR:  # check size of vectors
            length = node.values[0].size
            for ch in node.values:
                if ch.type != Type.VECTOR:
                    error(node.pos, "Matrix row is not a vector!")
                if ch.size != length:
                    error(node.pos, f"Matrix row bad size ({ch.size} instead of {length})")
            node.type = Type.MATRIX
            node.size = (len(node.values), length)

    def visit_Range(self, node: Range):
        self.visit(node.fr)
        self.visit(node.to)
        if node.fr.type != Type.INTNUM or node.to.type != Type.INTNUM:
            error(node.pos, f"range must be defined with integers, found {node.fr.type}, {node.to.type}")
        else:
            node.type = Type.VECTOR

    # operations --------------------------------------------------
    def visit_Assign(self, node: Assign):
        self.visit(node.left)
        self.visit(node.right)
        if isinstance(node.left, Identifier):
            if node.left.type == Type.NULL and node.op != '=':  # uninitialized
                    error(node.pos, "binary operation for uninitialized variable")
            else:
                if node.op == '=':
                    node.left.type = node.right.type
                    node.left.size = node.right.size
                    self.put_symbol(node.left.identifier, node.right.type, node.right.size)

                if node.op != '=':
                    self.check_binop(node.left, node.right, node.op[1], node.pos)

        else:
            node.left.type = node.right.type
            node.left.size = node.right.size

    def visit_MatrixCreator(self, node: MatrixCreator):
        self.visit(node.n)
        node.type = Type.MATRIX
        assert node.n.type == Type.VECTOR, "argument list should always be vector"
        if node.n.size == 1 and node.n.values[0].type == Type.INTNUM:
            node.size = ( node.n.values[0].const_value, node.n.values[0].const_value)  # argument check is at parser level !!
        elif node.n.size == 2:
            if node.n.values[0].type == node.n.values[1].type == Type.INTNUM:
                node.size = (node.n.values[0].const_value, node.n.values[1].const_value)
            else:
                error(node.pos, f"function '{node.keyword}' takes only integers as argument")
        else:
            error(node.pos, f"function '{node.keyword}' takes 1 or 2 arguments, but {node.n.size} were given")

    def visit_Transpose(self, node: Transpose):
        self.visit(node.expr)
        if node.expr.type not in [Type.VECTOR, Type.MATRIX]:
            error(node.pos, f"cannot transpose variable of type {node.expr.type}")

    def visit_BinOp(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)
        node.type = node.left.type
        node.size = node.left.size
        self.check_binop(node.left, node.right, node.op, node.pos)

    @staticmethod
    def check_binop(left, right, op, pos):
        if left.type != right.type:
            error(pos, f"binop type mismatch: {left.type} ! {right.type}")
        else:
            types = left.type
            if op in ['.+', './', '.*', '.-'] and types not in [Type.VECTOR, Type.MATRIX]:
                error(pos, f"operation '{op}' undefined for type {types}")
            if left.type == Type.VECTOR and left.size != right.size:
                error(pos, f"binop on vectors with different sizes: {left.size} ! {right.size}")
            if left.type == Type.MATRIX:
                if op in ['-', '+', '.+', './', '.*', '.-'] and left.size != right.size:
                    error(pos,
                          f"incompatible sizes ({left.size} ! {right.size}) for elementwise operation '{op}' ")
                if op in ['*', '/']:
                    if left.size[1] != right.size[0]:
                        error(pos,
                              f"incompatible sizes ({left.size} ! {right.size}) for matrix operation '{op}' ")

    # Loops -------------------------------------------------------------
    def visit_For(self, node: For):
        self.visit(node.identifier)
        self.visit(node.mrange)
        self.put_symbol(node.identifier.identifier, Type.INTNUM) # iterator inside for is INTNUM
        self.symbol_table.push_scope("for")
        self.visit(node.statement)
        self.symbol_table.pop_scope()

    def visit_While(self, node: While):
        self.visit_and_push_scope(node, "while")

    def visit_Break(self, node: Break):
        if not self.symbol_table.is_in_loop():
            error(node.pos, "'break' outside loop")

    def visit_Continue(self, node: Continue):
        if not self.symbol_table.is_in_loop():
            error(node.pos, "'continue' outside loop")

    def visit_Empty(self, node: Empty):
        pass

    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    def visit_Expression(self, node: Expression):
        self.visit(node.expression)
        node.type = node.expression.type
        node.size = node.expression.size
        node.const_value = node.expression.const_value
        # print("--expression type", node.type)

    def visit_Logical(self, node: Logical):
        self.visit(node.left)
        self.visit(node.right)
        node.type = Type.BOOLEAN

    def visit_UMinus(self, node: UMinus):
        self.visit(node.expr)
        node.type = node.expr.type
        if node.expr.const_value:
            node.const_value = -1 * node.expr.const_value

    def visit_Number(self, node: Number):
        self.visit(node.number)
        node.type = node.number.type
        node.const_value = node.number.const_value

    def visit_IntNum(self, node: IntNum):
        node.type = Type.INTNUM
        node.const_value = node.number

    def visit_FloatNum(self, node: FloatNum):
        node.type = Type.FLOAT
        node.const_value = node.number

    def visit_StringM(self, node: StringM):
        node.type = Type.STRING
        node.size = len(node.string)
        node.const_value = node.string


def error(pos, message):
    print(f"[line {pos}]: {message}")
