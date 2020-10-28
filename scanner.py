import ply.lex as lex
from ply import yacc

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}
literals = ['+', '-', '/', '*', '=', '(', ')', '[', ']', '{', '}', '\'', ':', ';', ',']
tokens = ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
          'EQ', 'LT', 'GT', 'LTE', 'GTE', 'DIFF',
          'STR', 'ID', 'INTNUM', 'FLOAT'] + list(reserved.values())

t_DOTADD = r'.\+'
t_DOTSUB = r'.-'
t_DOTMUL = r'.\*'
t_DOTDIV = r'./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_EQ = r'=='
t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_DIFF = r'!='
t_ignore = ' \t'


def t_COMMENT(t):
    r'\#[^\n]*'


def t_FLOAT(t):
    r'((\d*\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'"([^"]*)"'
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"line ({t.lineno}): Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



# Precedence rules for the arithmetic operators
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right', 'UMINUS'),
)

# dictionary of names (for storing variables)
names = { }

# statement
def p_statement_assign(p):
    """statement : ID '=' expression
       statement : ID '=' list"""
    names[p[1]] = p[3]

def p_statement_expr(p):
    """statement : expression
                | logical
                | if
    """
    print(p[1])

# basic expressions
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = -p[2]

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_number(p):
    """expression : INTNUM
                  | FLOAT"""
    p[0] = p[1]

def p_expression_name(p):
    """expression : ID"""
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_expression_group(p):
    """expression : '(' expression  ')' """
    p[0] = p[2]
    p[0] = p[2]

# list and matrix
def p_list(p):
    """list : '[' value_list ']' """
    p[0] = p[2]

def p_list_first(p):
    """value_list : expression
    """
    p[0] = [ p[1] ]


def p_list_extend(p):
    """value_list : value_list ','  expression
    """
    p[0] = p[1]
    p[0].append(p[3])


def p_logical(p):
    """logical : expression EQ expression
                | expression LT expression
                | expression GT expression
                | expression LTE expression
                | expression GTE expression
                | expression DIFF expression
    """
    if p[2] == t_EQ  : p[0] = p[1] == p[3]
    elif p[2] == t_LT  : p[0] = p[1] < p[3]
    elif p[2] == t_GT  : p[0] = p[1] > p[3]
    elif p[2] == t_LTE : p[0] = p[1] <= p[3]
    elif p[2] == t_GTE : p[0] = p[1] >= p[3]
    elif p[2] == t_DIFF: p[0] = p[1] != p[3]


def p_if(p):
    """if : IF '(' logical ')' expression
          | IF '(' logical ')' '{' expression '}'
    """
    if '{' in p:
        exp = p[6]
    else:
        exp = p[5]
    if p[3]:
        p[0] = exp


def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()
