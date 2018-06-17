import entities


class Memory:
    def __init__(self, name):  # memory name
        self.memoryTable = {}

    def has_key(self, name):  # variable name
        return name in self.memoryTable

    def get(self, name):  # gets from memory current value of variable <name>
        return self.memoryTable[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memoryTable[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = []
        if memory:
            self.stack.append(memory)
            print("Memory layer appended!")
        self.err = -1

    def get(self, name):  # gets from memory stack current value of variable <name>
        if not isinstance(name, entities.Variable):
            return None

        for memory in reversed(self.stack):
            if memory.has_key(name.value):
                return memory.get(name.value)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)
        # print("Inserted " + str(name) + " with value: ")
        # print(str(value))

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name, value)
                return

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop()
