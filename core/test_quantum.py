import unittest
import numpy as np
from main import QuantumApp

class TestQuantumGates(unittest.TestCase):
    def test_hadamard_logic(self):
        app = QuantumApp(num_qubits=1)
        app.compile("qubit q[1]; H q[0];")
        app.run()
        # Expected: 1/sqrt(2) [1, 1]
        expected = np.array([0.70710678, 0.70710678])
        np.testing.assert_allclose(np.abs(app.sim.state), expected, atol=1e-5)

    def test_ccnot_logic(self):
        app = QuantumApp(num_qubits=3)
        # 1 + 1 + 0 -> CCNOT should flip the 0 to 1
        app.compile("qubit q[3]; X q[0]; X q[1]; CCNOT(q[0], q[1], q[2]);")
        app.run()
        # State should be |111>, which is index 7 (2^0 + 2^1 + 2^2)
        self.assertEqual(np.argmax(np.abs(app.sim.state)), 7)

if __name__ == '__main__':
    unittest.main()
  
