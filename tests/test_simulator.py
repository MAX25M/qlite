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
        self.assertEqual(np.sum(np.abs(state)**2), 1.0)

    def test_bell_state_logic(self):
        """Check if H and CNOT create a Bell State (|00> + |11>)."""
        self.sim.apply_gate('H', [0])
        self.sim.apply_gate('CNOT', [0, 1])
        
        probs = self.sim.get_probabilities()
        # In a Bell state, 00 and 11 should both be 0.5
        self.assertAlmostEqual(probs['00'], 0.5)
        self.assertAlmostEqual(probs['11'], 0.5)
        self.assertAlmostEqual(probs['01'], 0.0)
        self.assertAlmostEqual(probs['10'], 0.0)

    def test_cz_gate_logic(self):
        """
        Verify CZ gate: A CZ gate between two Hadamards on the target 
        should behave exactly like a CNOT gate.
        Circuit: H(q1), CZ(q0, q1), H(q1) == CNOT(q0, q1)
        """
        # Prepare q0 in state |1>
        self.sim.apply_gate('X', [0]) 
        
        # Apply CZ logic sequence
        self.sim.apply_gate('H', [1])
        self.sim.apply_gate('CZ', [0, 1])
        self.sim.apply_gate('H', [1])
        
        probs = self.sim.get_probabilities()
        # Result should be |11>, meaning q1 was flipped because q0 was |1>
        self.assertAlmostEqual(probs['11'], 1.0)

    def test_get_probabilities_format(self):
        """Ensure probabilities return as a dictionary with correct bitstrings."""
        probs = self.sim.get_probabilities()
        self.assertIsInstance(probs, dict)
        self.assertIn('00', probs)
        self.assertEqual(len(probs), 4)

if __name__ == '__main__':
    unittest.main()
