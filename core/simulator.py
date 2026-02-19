import numpy as np
import re

# --- Standard Gate Matrices ---
I = np.array([[1, 0], [0, 1]], dtype=complex)
H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

def rx(theta):
    """Returns the rotation matrix for the X-axis."""
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

class Simulator:
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0
        self.history = [] 

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
        """Dispatcher for all gate types using a dictionary mapping."""
        if isinstance(target_indices, int):
            target_indices = [target_indices]

        self.history.append((gate_name, target_indices))
        
        # --- Clean Dictionary Dispatcher ---
        gate_map = {
            'H':    lambda: self._apply_1q_gate(H, target_indices[0]),
            'X':    lambda: self._apply_1q_gate(X, target_indices[0]),
            'Y':    lambda: self._apply_1q_gate(Y, target_indices[0]),
            'Z':    lambda: self._apply_1q_gate(Z, target_indices[0]),
            'RX':   lambda: self._apply_1q_gate(rx(angle), target_indices[0]) if angle is not None else None,
            'CNOT': lambda: self._apply_controlled_gate(X, target_indices[0], target_indices[1]),
            'CZ':   lambda: self._apply_controlled_gate(Z, target_indices[0], target_indices[1]),
        }

        action = gate_map.get(gate_name.upper())
        if action:
            action()
        else:
            raise ValueError(f"Gate '{gate_name}' is not supported by QLite.")

    def _apply_1q_gate(self, gate_matrix, target_qubit):
        """Applies a 1-qubit gate using the Kronecker product."""
        op = np.array([[1.0]])
        for i in range(self.num_qubits):
            if i == target_qubit:
                op = np.kron(op, gate_matrix)
            else:
                op = np.kron(op, I)
        self.state = np.dot(op, self.state)

    def _apply_controlled_gate(self, matrix, control, target):
        """Applies a controlled matrix efficiently."""
        new_state = np.zeros_like(self.state)
        for i in range(len(self.state)):
            # Check if control bit is 1
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
        """Prints an ASCII representation of the circuit."""
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
        """Executes a program from an AST."""
        statements = ast_root.statements if hasattr(ast_root, 'statements') else ast_root
        for node in statements:
            if hasattr(node, 'name'):
                indices = self.parse_indices(node.target)
                self.apply_gate(node.name, indices, angle=getattr(node, 'angle', None))

    def parse_indices(self, target_str):
        """Extracts numerical indices from string like 'q[0]'."""
        if not isinstance(target_str, str): 
            return [target_str] if isinstance(target_str, int) else target_str
        indices = re.findall(r'\[(\d+)\]', target_str)
        return [int(i) for i in indices]

# Keep compatibility for testing
QuantumSimulator = Simulator
