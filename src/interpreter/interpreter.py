import numpy

from src.astt.ast import *
from src.interpreter.exceptions import BreakException, ContinueException
from src.interpreter.memory import *
from src.interpreter.visit import *
import sys
from src.interpreter.operators import operations

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    def generic_visit(self, node: Node):
        print("generic", node)
        for child in node.children:
            if child:
                self.visit(child)

    @on('node')
    def visit(self, node):
        pass

    # --------------------------------------------   statements (no return value) -----
    @when(Program)
    def visit(self, node: Program):
        self.visit(node.statements)

    @when(Statements)
    def visit(self, node: Statements):
        for st in node.statements:
            self.visit(st)

    @when(Statement)
    def visit(self, node: Statement):
        self.visit(node.statement)

    @when(Empty)
    def visit(self, node: Empty):
        pass

    @when(Print)
    def visit(self, node: Print):
        vals = self.visit(node.value_list)
        print(*vals)
    # --------------------------------------------  expressions ---------------------------

    @when(Expression)
    def visit(self, node: Expression):
        asd = self.visit(node.expression) # todo refactor nicely
        return asd

    @when(Number)
    def visit(self, node: Number):
        return node.const_value

    @when(StringM)
    def visit(self, node: StringM):
        return node.const_value

    @when(Logical)
    def visit(self, node: Logical):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return operations[node.cmp](left, right)

    @when(UMinus)
    def visit(self, node: UMinus):
        return -1*self.visit(node.expr)

    @when(Identifier)
    def visit(self, node: Identifier):
        val = self.memory_stack.get(node.identifier)
        return val

    @when(PartialId)
    def visit(self, node: PartialId):
        curr_val = self.memory_stack.get(node.identifier.identifier)
        refs = self.visit(node.index_ref)
        for ref in refs:
            curr_val = curr_val[ref]
        return curr_val

    @when(IndexRef)
    def visit(self, node: IndexRef):
        ref_list = []
        for ref in node.values:
            ref_val = self.visit(ref)
            if isinstance(ref, Range): # convert Range to Slice todo Type. ?
                ref_val = slice(ref_val[0], ref_val[1])
            ref_list.append(ref_val)
        return ref_list

    @when(Range)
    def visit(self, node: Range):
        val = (self.visit(node.fr), self.visit(node.to))
        return val

    @when(List)
    def visit(self, node: List):
        val = self.visit(node.value_list)
        return val

    @when(ValueList)
    def visit(self, node: ValueList):
        values = []
        for expr in node.values:
            values.append(self.visit(expr))
        return values

    # --------------------------------------------  operations --------------------------------------------

    @when(BinOp)
    def visit(self, node):
        left_val, right_val = self.visit(node.left), self.visit(node.right)
        return operations[node.op](left_val, right_val)

    @when(Assign)
    def visit(self, node: Assign):
        old_val = self.visit(node.left)
        right_val = self.visit(node.right)
        new_val = operations[node.op](old_val, right_val)
        if isinstance(node.left, Identifier):
            self.memory_stack.set(node.left.identifier, new_val)
        elif isinstance(node.left, PartialId):
            updated_id = self.visit(node.left.identifier)
            refs = self.visit(node.left.index_ref)
            print("refs:", refs)
            if len(refs) == 1:
                updated_id[refs[0]] = new_val
            else:
                updated_id[refs[0], refs[1]] = new_val
            self.memory_stack.set(node.left.identifier.identifier, updated_id)

    @when(MatrixCreator)
    def visit(self, node: MatrixCreator):
        shape = self.visit(node.n)
        if node.keyword == "eye":
            return numpy.eye(shape[0])
        if len(shape) == 1:
            shape = (shape[0], shape[0])
        if node.keyword == "ones":
            return numpy.ones(shape)
        elif node.keyword == "zeros":
            return numpy.zeros(shape)
        return None

    @when(Transpose)
    def visit(self, node: Transpose):
        matrix = self.visit(node.expr)
        return numpy.transpose(matrix)

    # ------------------------- scope functions ----------------------------------------
    @when(If)
    def visit(self, node: If):
        self.memory_stack.push(Memory('if'))
        cond = self.visit(node.logical)
        if cond:
            self.visit(node.statement)
        else:
            if node.else_block is not None:
                self.visit(node.else_block)
        self.memory_stack.pop()

    @when(ElseBlock)
    def visit(self, node: ElseBlock):
        self.memory_stack.push(Memory('else'))
        self.visit(node.statement)
        self.memory_stack.pop()

    @when(For)
    def visit(self, node: For):
        self.memory_stack.push(Memory('for'))
        mrange = self.visit(node.mrange)
        range_id = node.identifier.identifier
        for i in range(*mrange):
            try:
                self.memory_stack.set(range_id, i)
                self.visit(node.statement)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()


    @when(While)
    def visit(self, node: While):
        self.memory_stack.push(Memory('while'))
        status = self.visit(node.logical)
        while status:
            try:
                self.visit(node.statement)
                status = self.visit(node.logical)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()
        pass

    @when(Break)
    def visit(self, node: Break):
        raise BreakException()

    @when(Continue)
    def visit(self, node: Continue):
        raise ContinueException()







