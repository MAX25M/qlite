import numpy as np
import re

# --- Standard Gate Matrices ---
I = np.array([[1, 0], [0, 1]], dtype=complex)
H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def rx(theta):
    """Returns the rotation matrix for the X-axis."""
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

class Simulator:
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0
        self.history = []  # Tracks gates for the drawer

    def get_statevector(self):
        return self.state

    def get_probabilities(self):
        """Returns a dictionary mapping bitstrings to probabilities."""
        probs = np.abs(self.state)**2
        return {
            format(i, f'0{self.num_qubits}b'): float(p) 
            for i, p in enumerate(probs)
        }

    def apply_gate(self, gate_name, target_indices, angle=None):
        """Dispatcher for all gate types."""
        if isinstance(target_indices, int):
            target_indices = [target_indices]
        
        # Record for drawing
        self.history.append((gate_name, target_indices))

        if gate_name == 'H':
            self._apply_1q_gate(H, target_indices[0])
        elif gate_name == 'X':
            self._apply_1q_gate(X, target_indices[0])
        elif gate_name == 'Z':
            self._apply_1q_gate(Z, target_indices[0])
        elif gate_name == 'RX' and angle is not None:
            self._apply_1q_gate(rx(angle), target_indices[0])
        elif gate_name == 'CNOT':
            self._apply_controlled_gate(X, target_indices[0], target_indices[1])
        elif gate_name == 'CZ':
            self._apply_controlled_gate(Z, target_indices[0], target_indices[1])

    def _apply_1q_gate(self, gate_matrix, target_qubit):
        """Standard 1-qubit gate application via Kronecker product."""
        full_op = np.array([1.0])
        for i in range(self.num_qubits):
            full_op = np.kron(full_op, gate_matrix if i == target_qubit else I)
        self.state = np.dot(full_op, self.state)

    def _apply_controlled_gate(self, matrix, control, target):
        """Applies a controlled matrix (X for CNOT, Z for CZ)."""
        new_state = np.zeros_like(self.state)
        for i in range(len(self.state)):
            # Check if control bit is 1 (using big-endian bit order)
            if (i >> (self.num_qubits - 1 - control)) & 1:
                if np.array_equal(matrix, X): # CNOT logic
                    flipped_idx = i ^ (1 << (self.num_qubits - 1 - target))
                    new_state[flipped_idx] = self.state[i]
                elif np.array_equal(matrix, Z): # CZ logic
                    if (i >> (self.num_qubits - 1 - target)) & 1:
                        new_state[i] = -self.state[i]
                    else:
                        new_state[i] = self.state[i]
            else:
                new_state[i] = self.state[i]
        self.state = new_state

    def draw(self):
        """Prints an ASCII circuit representation."""
        lines = [f"q{i}: ──" for i in range(self.num_qubits)]
        for gate, targets in self.history:
            if len(targets) == 1:
                t = targets[0]
                for i in range(self.num_qubits):
                    lines[i] += f"[{gate}]──" if i == t else "─────"
            else:
                c, t = targets[0], targets[1]
                for i in range(self.num_qubits):
                    if i == c: lines[i] += "──●──"
                    elif i == t: lines[i] += f"─[{gate[1] if len(gate)>1 else gate}]─"
                    else: lines[i] += "─────"
        for line in lines:
            print(line)

    def run_program(self, ast_root):
        statements = ast_root.statements if hasattr(ast_root, 'statements') else ast_root
        for node in statements:
            if hasattr(node, 'name'):
                indices = self.parse_indices(node.target)
                self.apply_gate(node.name, indices, angle=getattr(node, 'angle', None))

    def parse_indices(self, target_str):
        if not isinstance(target_str, str): 
            return [target_str] if isinstance(target_str, int) else target_str
        indices = re.findall(r'\[(\d+)\]', target_str)
        return [int(i) for i in indices]

# Compatibility alias
QuantumSimulator = Simulator
