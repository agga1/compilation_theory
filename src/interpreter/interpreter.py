from src.astt.ast import *
from src.interpreter.memory import *
from src.interpreter.visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    def generic_visit(self, node: Node): # todo how??
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
        # print("Program")
        self.visit(node.statements)

    @when(Statements)
    def visit(self, node: Statements):
        # print("Statements")
        for st in node.statements:
            self.visit(st)

    @when(Statement)
    def visit(self, node: Statement):
        print("\n--st--")
        self.visit(node.statement)

    @when(Empty)
    def visit(self, node: Empty):
        print("Empty")

    # --------------------------------------------  expressions ---------------------------

    @when(Expression)
    def visit(self, node: Expression):
        asd = self.visit(node.expression) # todo refactor nicely
        print("Expression: ", asd)
        return asd

    @when(Number)
    def visit(self, node: Number):
        return node.const_value

    @when(StringM)
    def visit(self, node: StringM):
        return node.const_value

    @when(Identifier)
    def visit(self, node: Identifier):
        val = self.memory_stack.get(node.identifier)
        print(node.identifier, ":", val)
        return val

    @when(PartialId)
    def visit(self, node: PartialId):
        curr_val = self.memory_stack.get(node.identifier.identifier)
        refs = self.visit(node.index_ref)
        for ref in refs:
            curr_val = curr_val[ref] # todo range reference
        return curr_val

    @when(IndexRef)
    def visit(self, node: IndexRef):
        ref_list = []
        for ref in node.values:
            ref_list.append(self.visit(ref))
        return ref_list

    @when(List)
    def visit(self, node: List):
        return self.visit(node.value_list)

    @when(ValueList)
    def visit(self, node: ValueList):
        values = []
        for expr in node.values:
            values.append(self.visit(expr))
        return values

    # --------------------------------------------  operations --------------------------------------------

    @when(BinOp)
    def visit(self, node):
        print("\t evaluating binop")
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        # try sth smarter than:
        if(node.op=='+'):
            return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(Assign)
    def visit(self, node: Assign):
        print("Assign")
        self.visit(node.left)
        val = self.visit(node.right)
        if isinstance(node.left, Identifier):
            print("assigning", node.left.identifier, "to", val)
            self.memory_stack.set(node.left.identifier, val)
        else: # todo assign partialId
            pass

    # @when(ast.Assignment)
    # def visit(self, node):
    # #
    # #
    #
    # # simplistic while loop interpretation
    # @when(ast.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r

