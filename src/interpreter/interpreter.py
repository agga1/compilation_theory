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

    @when(Range)
    def visit(self, node: Range): # todo check if working
        val = range(self.visit(node.fr), self.visit(node.to))
        print("range:", list(val))
        return val

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
        if(node.op=='+'): # todo more operations
            return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(Assign)
    def visit(self, node: Assign):
        old_val = self.visit(node.left)
        new_val = self.visit(node.right)
        new_val = self.eval_assign(old_val, new_val, node.op)
        if isinstance(node.left, Identifier):
            print("assigning", node.left.identifier, "to", new_val)
            self.memory_stack.set(node.left.identifier, new_val)
        elif isinstance(node.left, PartialId):
            updated_id = self.visit(node.left.identifier)
            refs = self.visit(node.left.index_ref)
            if len(refs) == 1:
                updated_id[refs[0]] = new_val
            else:
                updated_id[refs[0]][refs[1]] = new_val
            print("assigning", node.left.identifier.identifier, "to", updated_id)
            self.memory_stack.set(node.left.identifier.identifier, updated_id)

    def eval_assign(self, left, right, op):
        if op == "=":
            return right
        if op == '+=':
            return left + right
        if op == '-=':
            return left - right
        if op == '*=':
            return left*right
        if op == '/=':
            return left/right


