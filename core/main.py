from lexer import lexer
from parser import parser
from simulator import QuantumSimulator, run_program, plot_probabilities
from transpiler import Transpiler
from decomposer import Decomposer

# 1. Your Q-Lite Source Code
code = """
qubit q[2];
H q[0];
RX(3.14159 / 2.0) q[1];
CNOT(q[0], q[1]);
q[0] => c0;
q[1] => c1;
"""

class QuantumApp:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.ast = None
        self.sim = QuantumSimulator(num_qubits)
        self.qasm = ""

    def compile(self, source_code, hardware_optimize=True):
        print(f"--- Compiling {self.num_qubits}-Qubit Program ---")
        # 1. Parse
        self.ast = parser.parse(source_code, lexer=lexer)
        
        # 2. Decompose if needed
        if hardware_optimize:
            dec = Decomposer(self.ast)
            self.ast = dec.decompose()
        
        # 3. Transpile to QASM
        tp = Transpiler(self.ast)
        self.qasm = tp.transpile()
        print("Compilation successful.")

    def run(self):
        if not self.ast:
            raise Exception("Please compile the program before running.")
        
        print("Executing on local simulator...")
        run_program(self.ast, self.sim)
        print("Execution complete.")

    def visualize(self):
        plot_probabilities(self.sim)

    def export_qasm(self, filename="output.qasm"):
        with open(filename, "w") as f:
            f.write(self.qasm)
        print(f"Hardware-ready code exported to {filename}")
        
def main():
    print("--- Starting Q-Lite Pipeline ---\n")
    # Parsing phase
    print("[1/6] Parsing code...")
    ast = parser.parse(code, lexer=lexer)

     # 1. Decomposition (Preparing for Hardware)
    print("[2/6] Decomposing high-level gates...")
    decomposer = Decomposer(ast)
    optimized_ast = decomposer.decompose()

    # 2. Transpilation
    print("[3/6] Transpiling to OpenQASM...")
    tp = Transpiler(optimized_ast)
    qasm_code = tp.transpile()
    print("\nGenerated QASM:\n", qasm_code, "\n")

    # 3. Save to File
    with open("output.qasm", "w") as f:
        f.write(qasm_code)
    print("[4/6] Hardware-ready code saved to 'output.qasm'")
    
    # 4. Simulation phase (Local)
    print("[5/6] Running local simulation...")
    # (Assuming run_program is modified to return the simulator instance)
    sim = run_program(ast) 
    
    # 5. Visualization
    print("[6/6] Generating probability distribution...")
    plot_probabilities(sim)

# Inside QuantumApp class in main.py

def compile(self, source_code, hardware_optimize=True):
    # SAFETY CHECK: The Exponential Wall
    # 24 qubits ≈ 256MB RAM; 30 qubits ≈ 16GB RAM.
    MAX_QUBITS = 24 
    if self.num_qubits > MAX_QUBITS:
        raise MemoryError(f"Quantum simulation of {self.num_qubits} qubits exceeds "
                          f"classical memory limits. Stay below {MAX_QUBITS}.")

    print(f"--- Compiling {self.num_qubits}-Qubit Program ---")
    self.ast = parser.parse(source_code, lexer=lexer)
    
    # Check if AST matches declared qubit count
    # (Additional logic to verify indices in self.ast vs self.num_qubits)
    
    if hardware_optimize:
        self.ast = Decomposer(self.ast).decompose()
    print("Compilation successful.")


if __name__ == "__main__":
    main()

  
