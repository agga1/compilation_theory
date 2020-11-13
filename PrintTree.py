from ast import *


def add_to_class(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
    return decorator

def add_to_classes(*classes):
    def decorator(func):
        for cls in classes:
            setattr(cls, func.__name__, func)
    return decorator


def print_with_indent(indent, msg):
    for i in range(indent):
        print("|  ", end="")
    print(msg)


class TreePrinter:
    def __init__(self):
        pass

    @staticmethod
    @add_to_classes(Program, Empty, Number, Expression, Statements, Statement)
    def print_tree(self, indent=0):
        """ silent print - no extra indentation, no messages, only recurse """
        for ch in self.children:
            ch.print_tree(indent)

    @staticmethod
    @add_to_class(IntNum)
    def print_tree(self, indent=0):
        print_with_indent(indent, f"int: {self.children[0]}")

    @staticmethod
    @add_to_class(FloatNum)
    def print_tree(self, indent=0):
        print_with_indent(indent, f"float: {self.children[0]}")


    @staticmethod
    @add_to_class(PartialId)
    def print_tree(self, indent=0):
        print_with_indent(indent,"PartialID")
        self.children[0].print_tree(indent+1)
        self.children[1].print_tree(indent+1)

    @staticmethod
    @add_to_class(ValueList)
    def print_tree(self, indent=0):
        print_with_indent(indent, "values")
        for ch in self.children:
            ch.print_tree(indent+1)

    @staticmethod
    @add_to_class(IndexRef)
    def print_tree(self, indent=0):
        print_with_indent(indent, "index_refs")
        for ch in self.children:
            ch.print_tree(indent+1)

    @staticmethod
    @add_to_class(Assign)
    def print_tree(self, indent=0):
        print_with_indent(indent, self.children[1])
        self.children[0].print_tree(indent + 1)
        self.children[2].print_tree(indent + 1)

    @staticmethod
    @add_to_class(BinOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, self.children[1])
        self.children[0].print_tree(indent + 1)
        self.children[2].print_tree(indent + 1)

    @staticmethod
    @add_to_class(Logical)
    def print_tree(self, indent=0):
        print_with_indent(indent, self.children[1])
        self.children[0].print_tree(indent + 1)
        self.children[2].print_tree(indent + 1)

    @staticmethod
    @add_to_class(UMinus)
    def print_tree(self, indent=0):
        print_with_indent(indent, "UMINUS")
        print(self.children[0].print_tree(indent+1))

    @staticmethod
    @add_to_class(Identifier)
    def print_tree(self, indent=0):
        print_with_indent(indent, f"id: {self.children[0]}")

    @staticmethod
    @add_to_class(String)
    def print_tree(self, indent=0):
        print_with_indent(indent, f"string: {self.children[0]}")

    @staticmethod
    @add_to_class(Return)
    def print_tree(self, indent=0):
        print_with_indent(indent, "RETURN")
        if len(self.children) > 0:
            print(self.children[0].print_tree(indent+1))

    @staticmethod
    @add_to_class(Print)
    def print_tree(self, indent=0):
        print_with_indent(indent, "PRINT")
        self.children[0].print_tree(indent+1)

    @staticmethod
    @add_to_class(Break)
    def print_tree(self, indent=0):
        print_with_indent(indent, "BREAK")

    @staticmethod
    @add_to_class(Continue)
    def print_tree(self, indent=0):
        print_with_indent(indent, "CONTINUE")


    @staticmethod
    @add_to_class(Range)
    def print_tree(self, indent=0):
        print_with_indent(indent, "RANGE")

        self.children[0].print_tree(indent + 1)
        self.children[1].print_tree(indent + 1)


    @staticmethod
    @add_to_class(MatrixCreator)
    def print_tree(self, indent=0):
        print_with_indent(indent, self.children[0])
        self.children[1].print_tree(indent+1)


    @staticmethod
    @add_to_class(If)
    def print_tree(self, indent=0):
        print_with_indent(indent, "IF")
        self.children[0].print_tree(indent+1)

        print_with_indent(indent, "THEN")
        self.children[1].print_tree(indent + 1)

        if len(self.children) == 3:
            self.children[2].print_tree(indent)

    @staticmethod
    @add_to_class(ElseBlock)
    def print_tree(self, indent=0):
        print_with_indent(indent, "ELSE")
        self.children[0].print_tree(indent+1)

    @staticmethod
    @add_to_class(While)
    def print_tree(self, indent=0):
        print_with_indent(indent, "WHILE")
        self.children[0].print_tree(indent+1)
        print_with_indent(indent, "DO")
        self.children[1].print_tree(indent + 1)

    @staticmethod
    @add_to_class(For)
    def print_tree(self, indent=0):
        print_with_indent(indent, "FOR")
        self.children[0].print_tree(indent+1)
        self.children[1].print_tree(indent+1)
        print_with_indent(indent, "DO")
        self.children[2].print_tree(indent + 1)

    # @staticmethod
    # @add_to_class(Expression)
    # def print_tree(self, indent=0):
    #     self.children[0].print_tree(indent)
    #
    # @staticmethod
    # @add_to_class(Statements)
    # def print_tree(self, indent=0):
    #     # print("statements")
    #     for ch in self.children:
    #         ch.print_tree(indent)
    #
    # @staticmethod
    # @add_to_class(Statement)
    # def print_tree(self, indent=0):
    #     # print("statement")
    #     self.children[0].print_tree(indent)

    # @staticmethod
    # @add_to_class(Program)
    # def print_tree(self, indent=0):
    #     self.children[0].print_tree(indent)
    #
    # @staticmethod
    # @add_to_class(Empty)
    # def print_tree(self, indent=0):
    #     print("empty")
    #     pass

    # @staticmethod
    # @add_to_class(Number)
    # def print_tree(self, indent=0):
    #     # print("number")
    #     self.children[0].print_tree(indent) # todo +1? >> no coz quiet print
