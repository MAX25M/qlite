# Command Line Interface
import argparse
import sys
from main import QuantumApp

def main():
    parser = argparse.ArgumentParser(description="Q-Lite Quantum Compiler & Simulator CLI")
    
    # Subcommands: run or transpile
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # 'run' command: simulate and show results
    run_parser = subparsers.add_parser("run", help="Simulate a .qlite file")
    run_parser.add_argument("file", help="Path to the .qlite source file")
    run_parser.add_argument("-q", "--qubits", type=int, default=5, help="Number of qubits")
    run_parser.add_argument("-v", "--visualize", action="store_true", help="Show probability histogram")

    # 'transpile' command: convert to OpenQASM
    trans_parser = subparsers.add_parser("transpile", help="Convert .qlite to OpenQASM")
    trans_parser.add_argument("file", help="Path to the .qlite source file")
    trans_parser.add_argument("-o", "--output", default="output.qasm", help="Output filename")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Load source code
    try:
        with open(args.file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    # Initialize the App
    app = QuantumApp(num_qubits=args.qubits)

    if args.command == "run":
        app.compile(source)
        app.run()
        if args.visualize:
            app.visualize()
            
    elif args.command == "transpile":
        app.compile(source)
        app.export_qasm(args.output)

if __name__ == "__main__":
    main()
  
