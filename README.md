# Qlite Language & Compiler 
## Powered by Qlite language 

![Tests](https://github.com/MAX25M/qlite/actions/workflows/tests.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/qlite)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![GitHub stars](https://img.shields.io/github/stars/MAX25M/qlite.svg)](https://github.com/MAX25M/qlite/stargazers)
[![github-trophy](https://github-profile-trophy.vercel.app/?username=[MAX25M])](https://github.com/users/MAX25M/achievements/pull-shark)

---
## Quantum Computing Made Simple
**Qlite** *(`kla•yt)* is a lightweight, modular quantum compiler and simulator designed for both beginners and quantum enthusiasts. Build quantum algorithms from the command line, simulate them locally, or seamlessly export to IBM Quantum—all with a streamlined, mobile-friendly interface. It bridges the gap between high-level quantum programming and local simulation, featuring a custom AST-based Qlite interpreter and an integrated circuit visualization tool.

---
### Key Features

- **CLI to Cloud**: Program quantum algorithms directly from your terminal
- **Local Simulation**: Test and debug circuits without leaving your machine
- **IBM Quantum Integration**: Export your work to IBM's quantum processors
- **Mobile-Friendly**: Access the full development pipeline from any device. Designed with a clean, modular architecture accessible for any dev environment.
- **Modular Architecture**: Build and compose quantum components with ease
- **Custom DSL**: A streamlined syntax for defining qubits and gates.
- **Local High-Fidelity Simulation**: Full state-vector simulation supporting superposition and entanglement.
- **ASCII Circuit Drawing**: Visualize your quantum circuits directly in the terminal.
- **Advanced Gate Library**: Support for `H`, `X`, `Z`, `RX(θ)`, `CNOT`, and `CZ`.
---

## Installation

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/MAX25M/qlite.git](https://github.com/MAX25M/qlite.git)
cd qlite
pip install -r requirements.txt
```
---
Usage
1. The Qlite Language (.ql)
Write your quantum algorithms in a simple, declarative style:
```bash
// Example: Bell State
qubit q[2];
H q[0];
CNOT(q[0], q[1]);
```
2. Running the Simulator
You can use the simulator directly in Python to execute gates or process an AST:

```bash
from core.simulator import Simulator

# Initialize 2 qubits
sim = Simulator(num_qubits=2)

# Apply gates
sim.apply_gate('H', [0])
sim.apply_gate('CNOT', [0, 1])

# Visualize the circuit
sim.draw()

# Get state results
print(sim.get_probabilities())
```
3. Circuit Visualization
Q-Lite includes a built-in ASCII drawer to debug your circuit logic visually:
```bash
q0: ──[H]────●──
q1: ────────[X]─
```
---
# Qlite (.ql) Supported Gates
| Gate | Type | Description |
|---|---|---|
| H | Single | Creates superposition ($ |
| X | Single | Pauli-X (Quantum NOT gate) |
| Z | Single | Pauli-Z (Phase flip) |
| RX(θ) | Single | Rotation around the X-axis |
| CNOT | Multi | Controlled-NOT (Entangles two qubits) |
| CZ | Multi | Controlled-Z (Phase entanglement) |
---

# Testing
We use unittest to ensure mathematical accuracy of the state-vector transitions.
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m unittest discover tests
```
---
# The test suite covers:
 * Initial state |00\rangle verification.
 * Bell State probability distribution (50/50 split).
 * CZ Gate phase-interference logic.
---
## Roadmap
* ![Done](https://img.shields.io/badge/-Complete-success?style=flat-square) State-vector Simulation
* ![Done](https://img.shields.io/badge/-Complete-success?style=flat-square) ASCII Circuit Drawing
* ![Done](https://img.shields.io/badge/-Complete-success?style=flat-square) Multi-qubit Gate Support (CNOT, CZ)
* ![Planned](https://img.shields.io/badge/-Planned-lightgrey?style=flat-square) OpenQASM 3.0 Compatibility
* ![Planned](https://img.shields.io/badge/-Planned-lightgrey?style=flat-square)Integration with IBM Quantum (Qiskit)
* ![Planned](https://img.shields.io/badge/-Planned-lightgrey?style=flat-square) Qlite Quantum Programming Language Standalone IDE
* ![Planned](https://img.shields.io/badge/-Planned-lightgrey?style=flat-square) "Hardware Bridge"—a module that converts Qlite AST directly into OpenQASM,
---
## Support the Developer 

If you find **Qlite** useful, please consider supporting its development!

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/MAX25M)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal)](https://paypal.me/MarkJosephOctavo)
---
## Support the Project

If **Qlite** helped you learn quantum computing or speed up your workflow, consider buying me a coffee! Your support helps keep the project alive and free.

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/MarkJosephOctavo?locale.x=en_US&country.x=PH)
---
# License
This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details. Distributed under the MIT License. See [LICENSE](LICENSE.md)for more information.

## How to Cite
If you use this software in your work, please cite it as follows:
```bibtex
@software{Qlite,
  author = {Mark Joseph N. Octavo},
  title = {Qlite Quantum Programming Language and Compiler},
  url = {https://github.com/MAX25M/qlite},
  version = {0.0.6},
  year = {2026}
}
``` 
---
©2026 [Qlite](https://github.com/MAX25M/qlite) Distribution. All rights reserved 

