import unittest
from core.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_simple_parse(self):
        code = "qubit q[2]; H q[0];"
        ast = self.parser.parse(code)
        
        # 1. Check total nodes
        self.assertEqual(len(ast), 2)
        
        # 2. Check Declaration (Now returns a dictionary with 'DECLARE')
        self.assertEqual(ast[0]['type'], 'DECLARE')
        self.assertEqual(ast[0]['size'], 2)
        
        # 3. Check Gate (Now returns a GateNode object)
        self.assertEqual(ast[1].name, 'H')
        self.assertEqual(ast[1].target, 'q[0]')

    def test_rotational_gate(self):
        code = "RX(3.14) q[0];"
        ast = self.parser.parse(code)
        self.assertEqual(ast[0].name, 'RX')
        self.assertAlmostEqual(ast[0].angle, 3.14)

    def test_syntax_error(self):
        # Note: PLY's yacc.parse() usually returns None or prints to console on error
        # unless configured to raise an exception.
        code = "H q[0]" # Missing semicolon
        ast = self.parser.parse(code)
        self.assertIsNone(ast)

if __name__ == '__main__':
    unittest.main()
