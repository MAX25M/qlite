import ply.yacc as yacc
from .lexer import tokens
import math

# --- AST Node Classes ---
class Program:
    def __init__(self, statements):
        self.statements = statements

class GateNode:
    def __init__(self, name, target, angle=None):
        self.name = name
        self.target = target
        self.angle = angle

class MeasurementNode:
    def __init__(self, target, bit_name):
        self.target = target
        self.bit_name = bit_name

# --- Grammar Rules ---
def p_program(p):
    'program : statement_list'
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_declaration(p):
    'statement : QUBIT ID LBRACKET INTEGER RBRACKET SEMICOLON'
    p[0] = {'type': 'DECLARE', 'id': p[2], 'size': p[4]}

def p_statement_fixed_gate(p):
    'statement : GATE_FIXED qarg SEMICOLON'
    p[0] = GateNode(p[1], p[2])

def p_statement_rot_gate(p):
    'statement : GATE_ROT LPAREN expression RPAREN qarg SEMICOLON'
    p[0] = GateNode(p[1], p[5], angle=p[3])

def p_statement_measure(p):
    'statement : qarg ARROW ID SEMICOLON'
    p[0] = MeasurementNode(p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    '''expression : FLOAT
                  | INTEGER'''
    p[0] = p[1]

def p_expression_pi(p):
    'expression : PI'
    p[0] = math.pi

def p_qarg(p):
    'qarg : ID LBRACKET INTEGER RBRACKET'
    p[0] = f"{p[1]}[{p[3]}]"

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# --- Parser Entry Point ---
class Parser:
    def __init__(self):
        # Build the yacc parser using the global functions in this module
        self.parser = yacc.yacc()

    def parse(self, data):
        return self.parser.parse(data)


