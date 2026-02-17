import unittest
import numpy as np
from core.simulator import Simulator

class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator(num_qubits=2)

    def test_initial_state(self):
        # State should be |00>
        state = self.sim.get_statevector()
        self.assertEqual(state[0], 1.0)
        self.assertEqual(sum(state), 1.0)

    def test_bell_state_logic(self):
        # Manual Bell State: H(0), CNOT(0,1)
        self.sim.apply_gate("H", [0])
        self.sim.apply_gate("CNOT", [0, 1])
        probs = self.sim.get_probabilities()
        
        # We expect 50% |00> and 50% |11>
        self.assertAlmostEqual(probs['00'], 0.5)
        self.assertAlmostEqual(probs['11'], 0.5)
        self.assertEqual(probs.get('01', 0), 0)

if __name__ == '__main__':
    unittest.main()
