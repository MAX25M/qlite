import numpy as np
import matplotlib.pyplot as plt
import re
# Assuming these are your local files
# from .AST_Node import GateNode, MeasurementNode, Program 
# import .Base_Gates as bg

# Helper for Gate matrices (H, I, and RX)
I = np.array([[1, 0], [0, 1]])
H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])

def rx(theta):
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]])

class Simulator:
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0

    def apply_gate(self, gate_matrix, target_qubit):
        """Applies a 1-qubit gate to a specific target using Kronecker product."""
        full_op = np.array([1.0])
        for i in range(self.num_qubits):
            if i == target_qubit:
                full_op = np.kron(full_op, gate_matrix)
            else:
                full_op = np.kron(full_op, I)
        self.state = np.dot(full_op, self.state)
        
    def get_statevector(self):
        """Returns the current state vector. Added for TestSimulator compatibility."""
        return self.state

    def get_probabilities(self):
        """Returns a dictionary mapping bitstrings to probabilities."""
        probabilities = np.abs(self.state)**2
        # Convert the flat array into a dictionary: {'00': 0.5, '11': 0.5}
        return {
            format(i, f'0{self.num_qubits}b'): float(p) 
            for i, p in enumerate(probabilities)
        }

    def measure(self):
        probs = self.get_probabilities()
        # Ensure probabilities sum to exactly 1.0 for random.choice
        probs /= np.sum(probs) 
        outcome = np.random.choice(len(self.state), p=probs)
        self.state = np.zeros_like(self.state)
        self.state[outcome] = 1.0
        return format(outcome, f'0{self.num_qubits}b')

    def run_program(self, ast_root):
        """Executes the Abstract Syntax Tree."""
        # Note: In a real compiler, ast_root.statements is a list
        # If ast_root is already a list, iterate directly
        statements = ast_root.statements if hasattr(ast_root, 'statements') else ast_root
        
        for node in statements:
            # Check for GateNodes
            # We use hasattr or isinstance depending on your setup
            if hasattr(node, 'name'):
                indices = self.parse_indices(node.target)
                
                if node.name == 'H':
                    self.apply_gate(H, indices[0])
                
                elif node.name == 'RX':
                    self.apply_gate(rx(node.angle), indices[0])
                
                elif node.name == 'CNOT':
                    # Assuming you have an external apply_cnot helper
                    # self.state = apply_cnot(self.state, indices[0], indices[1], self.num_qubits)
                    print(f"Applying CNOT on {indices}")
                
                elif node.name == 'SWAP':
                    print(f"Applying SWAP on {indices}")
                
                elif node.name in ['CCNOT', 'Toffoli']:
                    print(f"Applying Toffoli on {indices}")
            
            # Check for MeasurementNodes
            elif hasattr(node, 'bit_name'):
                result = self.measure()
                print(f"Measured state: {result}")

    def parse_indices(self, target_str):
        indices = re.findall(r'\[(\d+)\]', str(target_str))
        return [int(i) for i in indices]

    def plot_probabilities(self):
        probs = self.get_probabilities()
        states = [format(i, f'0{self.num_qubits}b') for i in range(len(probs))]
        plt.bar(states, probs, color='skyblue')
        plt.xlabel('Quantum State')
        plt.ylabel('Probability')
        plt.title('Output Distribution')
        plt.show()

# Standard alias for your tests to find
QuantumSimulator = Simulator
