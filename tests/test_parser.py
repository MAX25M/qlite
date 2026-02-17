import unittest
from core.parser import Parser

class TestParser(unittest.TestCase):
    def test_simple_parse(self):
        parser = Parser()
        code = "qubit q[2]; H q[0];"
        ast = parser.parse(code)
        
        # Check if we have two main nodes: Declaration and Gate application
        self.assertEqual(len(ast), 2)
        self.assertEqual(ast[0]['type'], 'declaration')
        self.assertEqual(ast[1]['gate'], 'H')

    def test_syntax_error(self):
        parser = Parser()
        code = "H q[0]" # Missing semicolon
        with self.assertRaises(SyntaxError):
            parser.parse(code)

if __name__ == '__main__':
    unittest.main()
