from main import QuantumApp

# Searching for the "marked" state |11>
grover_code = """
qubit q[2];

# 1. Initialization: Put both qubits in superposition
H q[0]; 
H q[1];

# 2. The Oracle: Flip the sign of |11> specifically
# For 2 qubits, a CZ gate acts as the oracle for |11>
# CZ is H -> CNOT -> H
H q[1];
CNOT(q[0], q[1]);
H q[1];

# 3. The Diffuser: Amplifies the marked state
H q[0]; H q[1];
X q[0]; X q[1];
H q[1]; CNOT(q[0], q[1]); H q[1]; # Another CZ
X q[0]; X q[1];
H q[0]; H q[1];
"""

app = QuantumApp(num_qubits=2)
app.compile(grover_code)
app.run()

print("\nGrover Search Results for '11':")
app.visualize()
