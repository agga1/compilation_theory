
from ast import *
from memory import *
from visit import *
import sys

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
        print("visiting", node)

    @when(Program)
    def visit(self, node: Program):
        self.visit(node.children)

    @when(BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

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

