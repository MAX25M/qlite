    
import numpy as np
import Base_Gates as bg

def apply_cnot(state, control, target, num_qubits):
    # Projectors for the control qubit
    P0 = np.array([[1, 0], [0, 0]]) # |0><0|
    P1 = np.array([[0, 0], [0, 1]]) # |1><1|
        """
    Applies a CNOT gate between any two qubits in an n-qubit system.
    """
    # 1. Component for Control being in state |0>
    op0 = 1
    for i in range(num_qubits):
        if i == control_idx:
            op0 = np.kron(op0, bg.P0)
        else:
            op0 = np.kron(op0, bg.I)
            
    # 2. Component for Control being in state |1> (Flips the target)
    op1 = 1
    for i in range(num_qubits):
        if i == control_idx:
            op1 = np.kron(op1, bg.P1)
        elif i == target_idx:
            op1 = np.kron(op1, bg.X)
        else:
            op1 = np.kron(op1, bg.I)
            
    # Combined Operator: CNOT = (|0><0| ⊗ I) + (|1><1| ⊗ X)
    full_cnot_matrix = op0 + op1
    return np.dot(full_cnot_matrix, state)

def apply_toffoli(state, ctrl_a, ctrl_b, target, num_qubits):
    """
    Applies a CCNOT (Toffoli) gate to a system of n-qubits.
    """
    # 1. Logic: If (A=1 AND B=1), Flip Target
    # This requires constructing the operator where A and B are projected to |1>
    op_flip = 1
    for i in range(num_qubits):
        if i == ctrl_a:
            op_flip = np.kron(op_flip, bg.P1)
        elif i == ctrl_b:
            op_flip = np.kron(op_flip, bg.P1)
        elif i == target:
            op_flip = np.kron(op_flip, bg.X)
        else:
            op_flip = np.kron(op_flip, bg.I)
            
    # 2. Logic: For all other combinations, do nothing (Identity)
    # The Identity operator for the whole system is:
    # I_total - (Projector_A1 ⊗ Projector_B1 ⊗ I_target)
    # But a simpler way is: Identity + (Projector_A1 ⊗ Projector_B1 ⊗ (X - I))
    
    op_stay = 1
    for i in range(num_qubits):
        if i == ctrl_a:
            op_stay = np.kron(op_stay, bg.P1)
        elif i == ctrl_b:
            op_stay = np.kron(op_stay, bg.P1)
        elif i == target:
            op_stay = np.kron(op_stay, bg.I)
        else:
            op_stay = np.kron(op_stay, bg.I)
            
    # Toffoli Matrix = (Full Identity - op_stay) + op_flip
    full_identity = np.eye(2**num_qubits, dtype=complex)
    toffoli_matrix = (full_identity - op_stay) + op_flip
    
    return np.dot(toffoli_matrix, state)

def apply_controlled_phase(state, ctrl, target, k, num_qubits):
    theta = (2 * np.pi) / (2**k)
    phase_gate = np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)
    
    op0 = 1
    for i in range(num_qubits):
        op0 = np.kron(op0, bg.P0 if i == ctrl else bg.I)
            
    op1 = 1
    for i in range(num_qubits):
        if i == ctrl: op1 = np.kron(op1, bg.P1)
        elif i == target: op1 = np.kron(op1, phase_gate)
        else: op1 = np.kron(op1, bg.I)
            
    return np.dot(op0 + op1, state)
          


