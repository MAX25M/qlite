import math

def print_ascii_histogram(probabilities, precision=4):
    """
    Renders a text-based histogram of quantum state probabilities.
    Perfect for Termux, SSH, and headless environments.
    """
    print("\n" + "="*50)
    print(f"{'STATE':<10} | {'PROBABILITY':<30} | {'%'}")
    print("-" * 50)

    # Filter out near-zero probabilities for a cleaner view
    active_states = {s: p for s, p in probabilities.items() if round(p, precision) > 0}
    
    if not active_states:
        print("No measurable states detected (Zero State).")
        return

    # Configuration for the bar chart
    max_width = 30
    # Block characters: Full '█', Half '▌', or Hash '#' for maximum compatibility
    full_block = "█"
    
    # Sort by state string (e.g., |00>, |01>)
    for state in sorted(active_states.keys()):
        prob = active_states[state]
        
        # Calculate bar length
        # We ensure at least 1 block if prob > 0
        bar_length = max(1, int(prob * max_width)) if prob > 0 else 0
        bar = full_block * bar_length
        
        # Format strings for alignment
        state_label = f"|{state}>"
        percentage = f"{prob * 100:>6.1f}%"
        
        print(f"{state_label:<10} | {bar:<30} | {percentage}")

    print("="*50 + "\n")

def print_state_vector(state_vector):
    """Displays the raw complex amplitudes for debugging."""
    print("Raw State Vector Amplitudes:")
    for i, amp in enumerate(state_vector):
        if abs(amp) > 1e-6:
            # Format complex numbers: (real + imag j)
            print(f"|{bin(i)[2:].zfill(int(math.log2(len(state_vector))))}>: {amp:.4f}")
          
