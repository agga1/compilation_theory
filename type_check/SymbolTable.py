from enum import Enum, auto
from typing import Optional

class Type(Enum):
    INTNUM = auto()
    FLOAT = auto()
    STRING = auto()
    VECTOR = auto()
    MATRIX = auto()
    BOOLEAN = auto()
    NULL = auto()
    UNKNOWN = auto()

class Symbol:
    def __init__(self, name, mtype, size):
        self.name = name
        self.type = mtype
        self.size = size

class SymbolTable(object):
    def __init__(self):
        self.scopes = []

    def push_scope(self, name):
        self.scopes.append((name, {}))

    def pop_scope(self):
        self.scopes.pop()

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.scopes[-1][1][name] = symbol

    def check_exists(self, name: str) -> bool:
        return self.get(name) is not None

    def get(self, name: str) -> Optional[Symbol]:  # get variable symbol or fundef from <name> entry
        for _, scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def is_in_loop(self) -> bool:
        for name, _ in self.scopes:
            if name in ["while", "for"]:
                return True
        return False
