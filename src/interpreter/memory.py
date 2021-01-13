from src.interpreter.operators import operations
from src.type_check.SymbolTable import Symbol


class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.symbols = {}

    def has_key(self, name):  # variable name
        return name in self.symbols

    def get(self, name):  # gets from memory current value of variable <name>
        return self.symbols.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value

    def __str__(self):
        return f"<{self.name}>:\n{str(self.symbols)}"

class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        memory = Memory('global') if memory is None else memory
        self.stack = [memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        memory = self._get_memory_with_name(name)
        if memory is not None:
            return memory.get(name)
        return None

    def set(self, name, value):  # sets variable <name> to value <value>
        memory = self._get_memory_with_name(name)
        if memory is not None:
            memory.put(name, value)
        else:  # variable uninitialized
            self.insert(name, value)

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.stack.pop()

    def __str__(self):
        ans = ""
        for m in self.stack:
            ans += "\n" + str(m)
        return ans

    def _get_memory_with_name(self, name):
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem
        return None

