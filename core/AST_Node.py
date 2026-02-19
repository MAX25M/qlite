class Program:
    def __init__(self, statements):
        self.statements = statements

class GateNode:
    def __init__(self, name, target, angle=None):
        self.name = name
        self.target = target
        self.angle = angle  # None for fixed gates like H or CNOT

class MeasurementNode:
    def __init__(self, qubit, classical_reg):
        self.qubit = qubit
        self.classical_reg = classical_reg
      

