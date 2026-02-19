import numpy as np

# Fundamental Constants
I = np.array([[1, 0], [0, 1]], dtype=complex)
H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
# Projectors for control logic
P0 = np.array([[1, 0], [0, 0]], dtype=complex) # |0><0|
P1 = np.array([[0, 0], [0, 1]], dtype=complex) # |1><1|
X = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli-X
I = np.eye(2, dtype=complex)                   # Identity

# Standard 2-qubit CNOT matrix
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# Rotational Gate Generator
def rx(theta):
    return np.array([
        [np.cos(theta/2), -1j*np.sin(theta/2)],
        [-1j*np.sin(theta/2), np.cos(theta/2)]
    ], dtype=complex)


def cp_matrix(k):
    theta = (2 * np.pi) / (2**k)
    # 2-qubit Controlled-Phase Matrix
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, np.exp(1j * theta)]
    ], dtype=complex)
  

