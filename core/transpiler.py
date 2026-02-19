import math

class Transpiler:
    def __init__(self, ast_root):
        self.ast = ast_root
        self.output = ["OPENQASM 2.0;", 'include "qelib1.inc";']

    def transpile(self):
        for node in self.ast.statements:
            # 1. Handle Register Declarations
            if isinstance(node, tuple) and node[0] == 'DECLARE':
                self.output.append(f"qreg {node[1]}[{node[2]}];")
                self.output.append(f"creg c[{node[2]}];")
            
            # 2. Handle Gate Applications
            elif isinstance(node, GateNode):
                name = node.name.upper()
                
                # Controlled Phase (CP) mapping
                if name == 'CP':
                    # theta = 2*PI / 2^k
                    theta = (2 * math.pi) / (2**node.angle)
                    self.output.append(f"cu1({theta}) {node.target};")
                
                # SWAP mapping
                elif name == 'SWAP':
                    self.output.append(f"swap {node.target};")
                
                # CCNOT (Toffoli) mapping
                elif name == 'CCNOT' or name == 'TOFFOLI':
                    self.output.append(f"ccx {node.target};")
                
                # CNOT mapping
                elif name == 'CNOT':
                    self.output.append(f"cx {node.target};")
                
                # Standard single-qubit gates
                elif name in ['H', 'X', 'Y', 'Z']:
                    self.output.append(f"{name.lower()} {node.target};")
                
                # Generic Rotational Gates (RX, RY, RZ)
                elif node.angle is not None:
                    self.output.append(f"{name.lower()}({node.angle}) {node.target};")
                
                # Fallback for any other gate names
                else:
                    self.output.append(f"{name.lower()} {node.target};")
            
            # 3. Handle Measurements
            elif isinstance(node, MeasurementNode):
                self.output.append(f"measure {node.qubit} -> {node.classical_reg};")
        
        return "\n".join(self.output)


                                              
