from AST_Node import GateNode

class QuantumLibrary:
    @staticmethod
    def get_qft(qubits):
        """Generates a list of GateNodes representing a Quantum Fourier Transform."""
        nodes = []
        n = len(qubits)
        for i in range(n):
            nodes.append(GateNode('H', f"q[{qubits[i]}]"))
            for j in range(i + 1, n):
                # k = j - i + 1
                nodes.append(GateNode('CP', f"q[{qubits[j]}], q[{qubits[i]}]", angle=j-i+1))
        return nodes

    @staticmethod
    def get_adder(a_qubits, b_qubits, carry_qubit):
        """Generates nodes for a Ripple-Carry Adder logic."""
        # Simple example: just one bit adder
        return [
            GateNode('CCNOT', f"q[{a_qubits[0]}], q[{b_qubits[0]}], q[{carry_qubit}]"),
            GateNode('CNOT', f"q[{a_qubits[0]}], q[{b_qubits[0]}]")
        ]
      
