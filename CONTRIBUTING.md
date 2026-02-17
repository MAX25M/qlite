# Contributing to Q-Lite Quantum Compiler 

First off, thank you for considering contributing to Q-Lite! It’s people like you who make quantum computing more accessible for everyone.

## 🗺️ How can I contribute?

### 1. Reporting Bugs
If you find a bug (e.g., the simulator crashes at 10 qubits), please open an Issue on GitHub. Include:
* Your operating system.
* The `.qlite` code that caused the crash.
* The error message.

### 2. Adding New Gates
We are looking to expand our standard library. If you want to add a gate (like `CSWAP` or `RY`), you'll need to update:
1. `Base_Gates.py`: Add the unitary matrix.
2. `lexer.py`: Add the keyword.
3. `transpiler.py`: Add the OpenQASM mapping.

### 3. Improving the Simulator
If you have ideas for "Noise Simulation" or "Tensor Network" backends, please start a Discussion thread before submitting a Pull Request.

## 🚀 Development Setup

1. Fork the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
3. Install in editable mode:
   pip install -e .

#Running Tests
 # Before submitting a PR, ensure all unit tests pass:
   python -m unittest discover tests
   
   
Code of Conduct
Please be respectful and supportive of all contributors. We are all here to learn and build cool quantum tech!
