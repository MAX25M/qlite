import numpy as np
import matplotlib.pyplot as plt
import re

# Helper for Gate matrices
I = np.array([[1, 0], [0, 1]], dtype=complex)
H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)

def rx(theta):
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

class Simulator:
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        # Initialize state to |00...0>
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0

    def get_statevector(self):
        """Returns the current state vector. Required for TestSimulator."""
        return self.state

    def get_probabilities(self):
        """Returns a dictionary mapping bitstrings to probabilities. Required for TestSimulator."""
        probs = np.abs(self.state)**2
        return {
            format(i, f'0{self.num_qubits}b'): float(p) 
            for i, p in enumerate(probs)
        }

    def apply_gate(self, gate_name, target_indices, angle=None):
        """
        Unified gate application. 
        Supports string names (H, CNOT, RX) to match run_program and tests.
        """
        if gate_name == 'H':
            self._apply_1q_gate(H, target_indices[0])
        elif gate_name == 'RX' and angle is not None:
            self._apply_1q_gate(rx(angle), target_indices[0])
        elif gate_name == 'CNOT':
            self._apply_cnot(target_indices[0], target_indices[1])

    def _apply_1q_gate(self, gate_matrix, target_qubit):
        """Internal helper for Kronecker product single-qubit gates."""
        full_op = np.array([1.0])
        for i in range(self.num_qubits):
            if i == target_qubit:
                full_op = np.kron(full_op, gate_matrix)
            else:
                full_op = np.kron(full_op, I)
        self.state = np.dot(full_op, self.state)

    def _apply_cnot(self, control, target):
        """Applies a CNOT gate using state manipulation."""
        new_state = np.zeros_like(self.state)
        for i in range(len(self.state)):
            # Check if control bit is set
            if (i >> (self.num_qubits - 1 - control)) & 1:
                # Flip the target bit
                target_bit = (i ^ (1 << (self.num_qubits - 1 - target)))
                new_state[target_bit] = self.state[i]
            else:
                new_state[i] = self.state[i]
        self.state = new_state

    def measure(self):
        """Collapses the state and returns the result string."""
        probs_dict = self.get_probabilities()
        probs_array = np.array(list(probs_dict.values()))
        probs_array /= np.sum(probs_array)
        
        outcome_idx = np.random.choice(len(self.state), p=probs_array)
        self.state = np.zeros_like(self.state)
        self.state[outcome_idx] = 1.0
        return format(outcome_idx, f'0{self.num_qubits}b')

    def run_program(self, ast_root):
        """Executes the Abstract Syntax Tree."""
        statements = ast_root.statements if hasattr(ast_root, 'statements') else ast_root
        
        for node in statements:
            if hasattr(node, 'name'):
                indices = self.parse_indices(node.target)
                # Pass the node.name and indices to the unified apply_gate
                self.apply_gate(node.name, indices, angle=getattr(node, 'angle', None))
            
            elif hasattr(node, 'bit_name'):
                self.measure()

    def parse_indices(self, target_str):
        """Extracts [0, 1] from 'q[0], q[1]'."""
        indices = re.findall(r'\[(\d+)\]', str(target_str))
        return [int(i) for i in indices]

    def plot_probabilities(self):
        probs_dict = self.get_probabilities()
        plt.bar(probs_dict.keys(), probs_dict.values(), color='skyblue')
        plt.xlabel('Quantum State')
        plt.ylabel('Probability')
        plt.title('Output Distribution')
        plt.show()

# Alias for compatibility with TestSimulator
QuantumSimulator = Simulator
