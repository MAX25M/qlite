import ply.yacc as yacc
from lexer import tokens  # Import tokens from our Lexer

def p_program(p):
    'program : statement_list'
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Handle Qubit Declaration: qubit q[2];
def p_statement_declaration(p):
    'statement : QUBIT ID LBRACKET INTEGER RBRACKET SEMICOLON'
    p[0] = ('DECLARE', p[2], p[4])

# Handle Fixed Gates: H q[0];
def p_statement_fixed_gate(p):
    'statement : GATE_FIXED qarg SEMICOLON'
    p[0] = GateNode(p[1], p[2])

# Handle Rotational Gates: RX(3.14) q[0];
def p_statement_rot_gate(p):
    'statement : GATE_ROT LPAREN expression RPAREN qarg SEMICOLON'
    p[0] = GateNode(p[1], p[5], angle=p[3])

# Handle Measurement: q[0] => c0;
def p_statement_measure(p):
    'statement : qarg ARROW ID SEMICOLON'
    p[0] = MeasurementNode(p[1], p[3])

# Simple Math Expressions for Angles
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
    import math
    p[0] = math.pi

def p_qarg(p):
    'qarg : ID LBRACKET INTEGER RBRACKET'
    p[0] = f"{p[1]}[{p[3]}]"

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()
