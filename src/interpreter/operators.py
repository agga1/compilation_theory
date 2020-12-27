import operator
import numpy
operations = {"+": operator.add,
              "-": operator.sub,
              "/": operator.truediv,
              "*": numpy.dot,
              "=": lambda x, y: y,
              "+=": operator.add,
              "-=": operator.sub,
              "/=": operator.truediv,
              "*=": numpy.dot,
              ".+": operator.add,
              ".-": operator.sub,
              "./": operator.truediv,
              ".*": operator.mul,
              ">=": operator.ge,
              "<=": operator.le,
              "==": operator.eq,
              }




