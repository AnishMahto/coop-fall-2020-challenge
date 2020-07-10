from collections import deque

class EventSourcer():
    # Do not change the signature of any functions

    # Global deques to maintain history of operations. Deques are used to maintain constant time operations
    operations_history = []
    operations_undone = []

    class Operation:

        # static dictionary that provides list of supported operations
        types = {
            "ADD": "ADD",
            "SUBTRACT": "SUBTRACT"
        }

        def __init__(self, type: str, value):
            #assert that the operation being handled is supported
            assert type in self.types.keys(), "Unsupported operation"
            self.type = self.types[type]
            self.value = value;

    def __init__(self):
        self.value = 0
        #initialize lists as deques, for constant time O(1) operations
        self.operations_history = deque (self.operations_history)
        self.operations_undone = deque (self.operations_undone)

    def add(self, num: int):
        self.value += num;
        self.operations_history.append(self.Operation("ADD", num))

    def subtract(self, num: int):
        self.value -= num;
        self.operations_history.append(self.Operation("SUBTRACT", num))

    def reverseOperation (self, op: Operation):
        if op.type==self.Operation.types['ADD']:
            self.value -= op.value
        elif op.type==self.Operation.types['SUBTRACT']:
            self.value += op.value

    def applyOperation (self, op: Operation):
        if op.type==self.Operation.types['ADD']:
            self.value += op.value
        elif op.type==self.Operation.types['SUBTRACT']:
            self.value -= op.value        

    def undo(self):
        # when undoing an operation, take last operation and reverse it, then move it the front of the operations undone deque
        if len(self.operations_history) > 0:
            self.reverseOperation(self.operations_history[-1])
            self.operations_undone.appendleft(self.operations_history[-1])
            self.operations_history.pop()

    def redo(self):
        # when redoing an operation, take the last operation that was undone, apply it, then move it to the back of the operations history deque
        if len(self.operations_undone) > 0:
            self.applyOperation(self.operations_undone[0])
            self.operations_history.append(self.operations_undone[0])
            self.operations_undone.popleft()

    def bulk_undo(self, steps: int):
        while steps > 0 and len(self.operations_history) > 0:
            steps -= 1
            self.undo()

    def bulk_redo(self, steps: int):
        while steps > 0 and len(self.operations_undone) > 0:
            steps -= 1
            self.redo()

