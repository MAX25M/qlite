from AST_Node import GateNode, Program
from library import QuantumLibrary

class Decomposer:
    def __init__(self, ast):
        self.ast = ast

    def decompose(self):
        new_statements = []
        for node in self.ast.statements:
           # Look for a special 'FUNCTION' node (you'll need to add this to your AST/Parser)
            if hasattr(node, 'type') and node.type == 'FUNCTION_CALL':
                if node.name == 'QFT':
                    # Expand QFT into its component gates
                    qubit_indices = node.indices # e.g., [0, 1, 2]
                    expanded_gates = QuantumLibrary.get_qft(qubit_indices)
                    new_statements.extend(expanded_gates)
                else:
                    new_statements.append(node)
            else isinstance(node, GateNode) and node.name == 'H':
                # Decompose H into: RZ(pi/2), RX(pi/2), RZ(pi/2)
                # This is a common decomposition for hardware compatibility
                new_statements.append(GateNode('RZ', node.target, angle=1.5708))
                new_statements.append(GateNode('RX', node.target, angle=1.5708))
                new_statements.append(GateNode('RZ', node.target, angle=1.5708))
            else:
                new_statements.append(node)
        self.ast.statements = new_statements
        return self.ast

