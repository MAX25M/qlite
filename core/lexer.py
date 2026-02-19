import ply.lex as lex

# List of token names
tokens = (
    'QUBIT', 'REPEAT', 'PI',
    'GATE_FIXED', 'GATE_ROT',
    'ID', 'INTEGER', 'FLOAT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'ARROW', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
)

# Regular expression rules for simple tokens
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_SEMICOLON = r';'
t_COMMA     = r','
t_ARROW     = r'=>'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'

# Keywords and Special Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    keywords = {
        'qubit': 'QUBIT',
        'repeat': 'REPEAT',
        'PI': 'PI',
        # Fixed gates
        'H': 'GATE_FIXED', 'X': 'GATE_FIXED', 'Y': 'GATE_FIXED', 
        'Z': 'GATE_FIXED', 'CNOT': 'GATE_FIXED','CCNOT': 'GATE_FIXED', 'SWAP': 'GATE_FIXED',
        # Rotational gate  - Rotational/Parameterized gates
        'RX': 'GATE_ROT', 'RY': 'GATE_ROT', 'RZ': 'GATE_ROT', 'CP': 'GATE_ROT'
    }
    
    t.type = keywords.get(t.value, 'ID')
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (whitespace)
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out!
data = '''
qubit q[2];
RX(3.14159 / 2.0) q[0];
CNOT(q[0], q[1]);
q[0] => c0;
'''

lexer.input(data)

print(f"{'Token Type':<15} | {'Value':<15}")
print("-" * 35)
for tok in lexer:
    print(f"{tok.type:<15} | {tok.value:<15}")

  
