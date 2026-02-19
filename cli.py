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
    run_parser.add_argument("-a", "--ascii", action="store_true", help="Force ASCII visualization")

    # 'transpile' command: convert to OpenQASM
    trans_parser = subparsers.add_parser("transpile", help="Convert .qlite to OpenQASM")
    trans_parser.add_argument("file", help="Path to the .qlite source file")
    trans_parser.add_argument("-o", "--output", default="output.qasm", help="Output filename")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 1. Load source code
    try:
        with open(args.file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    # 2. Initialize the App
    app = QuantumApp(num_qubits=args.qubits)

    # 3. Handle Commands
    if args.command == "run":
        app.compile(source)
        app.run()
        
        # Get probabilities from the simulator
        probs = app.sim.get_probabilities()

        # Visualization Logic
        if args.ascii:
            from core.ascii_plotter import print_ascii_histogram
            print_ascii_histogram(probs)
        elif args.visualize:
            try:
                from core.visualizer import plot_probabilities
                plot_probabilities(probs)
            except Exception:
                print("\n[!] GUI Visualization failed (possibly Termux/Headless).")
                print("Falling back to ASCII...")
                from core.ascii_plotter import print_ascii_histogram
                print_ascii_histogram(probs)
        else:
            # Default to state vector print if no flags are passed
            print("\nSimulation complete. Use --visualize or --ascii to see results.")
            
    elif args.command == "transpile":
        app.compile(source)
        app.export_qasm(args.output)
        print(f"Successfully transpiled to {args.output}")

if __name__ == "__main__":
    main()

