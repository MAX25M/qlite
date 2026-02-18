import unittest
import numpy as np
from core.simulator import Simulator

class TestSimulator(unittest.TestCase):
    def setUp(self):
        # Initialize a 2-qubit simulator for all tests
        self.sim = Simulator(num_qubits=2)

    def test_initial_state(self):
        """Check if the simulator starts in state |00>."""
        state = self.sim.get_statevector()
        self.assertEqual(state[0], 1.0)
        # Use np.sum(np.abs()) for complex state vectors
        self.assertAlmostEqual(np.sum(np.abs(state)**2), 1.0)

    def test_bell_state_logic(self):
        """Check if H and CNOT create a Bell State (|00> + |11>)."""
        self.sim.apply_gate("H", [0])
        self.sim.apply_gate("CNOT", [0, 1])
        
        probs = self.sim.get_probabilities()
        # In a Bell state, 00 and 11 should both be 0.5
        self.assertAlmostEqual(probs['00'], 0.5)
        self.assertAlmostEqual(probs['11'], 0.5)
        self.assertAlmostEqual(probs.get('01', 0), 0)
        self.assertAlmostEqual(probs.get('10', 0), 0)

    def test_cz_gate_logic(self):
        """
        Verify CZ gate logic using the H-CZ-H identity.
        Circuit: X(q0), H(q1), CZ(q0, q1), H(q1) 
        This should result in state |11> (100% probability).
        """
        # 1. Flip q0 to |1> (the control)
        self.sim.apply_gate("X", [0]) 
        
        # 2. Put q1 into superposition
        self.sim.apply_gate("H", [1])
        
        # 3. Apply CZ (flips the phase of |11> only)
        self.sim.apply_gate("CZ", [0, 1])
        
        # 4. Apply H again to q1 to check for interference
        self.sim.apply_gate("H", [1])
        
        probs = self.sim.get_probabilities()
        # If CZ worked, the phase flip causes H to map back to |1> instead of |0>
        self.assertAlmostEqual(probs.get('11', 0), 1.0)

    def test_get_probabilities_format(self):
        """Ensure probabilities return as a dictionary with correct bitstrings."""
        probs = self.sim.get_probabilities()
        self.assertIsInstance(probs, dict)
        self.assertIn('00', probs)
        self.assertEqual(len(probs), 4)

if __name__ == '__main__':
    unittest.main()
