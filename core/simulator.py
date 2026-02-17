import matplotlib.pyplot as plt
import re
from AST_Node import GateNode, MeasurementNode, Program 
import Base_Gates as bg
from multiqubit_interpreter import apply_cnot, apply_controlled_phase

class QuantumSimulator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        # Initialize state to |00...0>
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1.0

    def apply_gate(self, gate_matrix, target_qubit):
        """Applies a 1-qubit gate to a specific target."""
        full_op = 1
        for i in range(self.num_qubits):
            if i == target_qubit:
                full_op = np.kron(full_op, gate_matrix)
            else:
                full_op = np.kron(full_op, I)
        self.state = np.dot(full_op, self.state)

    def get_probabilities(self):
        """Returns the probability of each state |00>, |01>, etc."""
        return np.abs(self.state)**2

    def measure(self):
        """Collapses the wavefunction based on probabilities."""
        probs = self.get_probabilities()
        outcome = np.random.choice(len(self.state), p=probs)
        # Collapse the state
        self.state = np.zeros_like(self.state)
        self.state[outcome] = 1.0
        return format(outcome, f'0{self.num_qubits}b')
        
    def run_program(ast_root, simulator):
    # For simplicity, assume we know we need 2 qubits
    sim = QuantumSimulator(num_qubits=2)

    for node in ast_root.statements:
        if isinstance(node, GateNode):
            # Extract indices (e.g., "q[0], q[1]" -> [0, 1])
            indices = parse_indices(node.target)
            if node.name == 'CP':
                k= node.angle  # We reuse the angle field for the 'k' parameter
                ctrl, target = parse_indices(node.target)
                simulator.state = apply_controlled_phase(simulator.state, ctrl, target, k, simulator.num_qubits)
            elif node.name == 'SWAP':
                    # A SWAP is just 3 CNOTs!
                    q1, q2 = parse_indices(node.target)
                    simulator.state = apply_cnot(simulator.state, q1, q2, simulator.num_qubits)
                    simulator.state = apply_cnot(simulator.state, q2, q1, simulator.num_qubits)
                    simulator.state = apply_cnot(simulator.state, q1, q2, simulator.num_qubits)
            elif node.name == 'H':
                    sim.apply_gate(H, 0) # Mapping q[0] to index 0
                 else node.name == 'RX':
                sim.apply_gate(rx(node.angle), 0)
            # CNOT and other logic here...
            else node.name == 'CCNOT' or node.name == 'Toffoli':
                # CCNOT(q[0], q[1], q[2]) -> q0, q1 are controls, q2 is target
                a, b, target = indices[0], indices[1], indices[2]
                simulator.state = apply_toffoli(
                    simulator.state, a, b, target, simulator.num_qubits
                # Assuming node.target is a list/tuple of [control, target]
                # You may need to parse the string "q[0], q[1]" into indices
                ctrl, targ = indices(node.target) 
                simulator.state = apply_cnot(
                    simulator.state, ctrl, targ, simulator.num_qubits
                )
        else isinstance(node, MeasurementNode):
            result = sim.measure()
            print(f"Measured state: {result}")
            print(f"Final State Vector: {sim.state}")
            
    
    def plot_probabilities(sim):
        probs = sim.get_probabilities()
        states = [format(i, f'0{sim.num_qubits}b') for i in range(len(probs))]
        plt.bar(states, probs, color='skyblue')
        plt.xlabel('Quantum State')
        plt.ylabel('Probability'
        plt.title('Output Distribution') plt.show()
        
    
    def parse_indices(target_str):
    """
    Converts "q[0], q[1]" into (0, 1) or "q[5]" into 5.
    """
    # Find all numbers inside square brackets
    indices = re.findall(r'\[(\d+)\]', target_str)
    return [int(i) for i in indices]
              
