import ply.lex as lex
from ply import yacc
import numpy as np

from expression import expression_factory, ExpressionList

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

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
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
    r'((\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
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
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
)

# dictionary of names (for storing variables)
names = { }

# statement
def p_statement_assign(p):
    """statement : ID '=' expression"""
    names[p[1]] = p[3]

def p_statement_expr(p):
    """statement : expression
                | logical
                | if
    """
    print(p[1])

def p_expression_print(p):
    'statement : PRINT expression'
    print(p[2])

# basic expressions
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = -p[2]

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTDIV expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression"""
    # print("p1", p[2])
    p1 = expression_factory(p[1])
    # print("p2", p[2])
    p2 = expression_factory(p[3])
    p[0] = p1.eval(p[2], p2)
    # print("result", p[0], p[2] )

def p_number(p):
    """number : INTNUM
                | FLOAT """
    p[0] = p[1]

def p_expression_number(p):
    '''expression : number
                  | row
                  | matrix
                  | id_partial '''
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

# MATRIX ops ------------------------------------------------
def p_statement_update(p):
    """statement :  ID '[' index_ref ']' '=' expression
                 | ID '[' index_ref_pair ']' '=' expression"""
    try:
        M = names[p[1]]
        if isinstance(p[3], tuple):
            M[p[3][0], p[3][1]] = p[6]
        else:
            M[p[3]] = p[6]
    except LookupError:
        print(f"Undefined name {p[1]!r}")

def p_range(p):
    """range : INTNUM ':' INTNUM"""
    p[0] = [i for i in range(p[1], p[3])]

def p_index_ref(p):
    """index_ref : INTNUM
                | range """
    p[0] = p[1]

def p_index_ref_pair(p):
    """index_ref_pair : index_ref ',' index_ref """
    p[0] = ( p[1], p[3] )

def p_matrix_part(p):
    """id_partial : ID '[' index_ref ']'
                    |  ID '[' index_ref_pair ']'"""
    try:
        M = names[p[1]]
        if isinstance(p[3], tuple):
            p[0] = M[p[3][0], p[3][1]]
        else:
            p[0] = M[p[3]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_matrix(p):
    """matrix : '[' row_list ']' """
    p[0] = np.array(p[2])

def p_matrix_extend(p):
    """row_list : row_list ','  row
    """
    p[0] = p[1]
    p[0].append(p[3])

def p_matrix_first(p):
    """row_list : row
    """
    p[0] = [ p[1] ]

def p_row(p):
    """row : '[' value_list ']' """
    p[0] = np.array(p[2])

def p_num_list_extend(p):
    """value_list : value_list ','  number
    """
    p[0] = p[1]
    p[0].append(p[3])

def p_num_list_first(p):
    """value_list : number
    """
    p[0] = [ p[1] ]

def p_zeros(p):
    """expression : ZEROS '(' INTNUM ')'"""
    p[0] = np.zeros((p[3], p[3]))


def p_ones(p):
    """expression : ONES '(' INTNUM ')'"""
    p[0] = np.ones((p[3], p[3]))


def p_eye(p):
    """expression : EYE '(' INTNUM ')'"""
    p[0] = np.eye(p[3])


def p_expression_transpose(p):
    """expression : expression "\'" """
    p1 = ExpressionList(p[1])
    p[0] = p1.transpose()


# LOGICAL ops -------------------------------------------------
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
    exp = p[6] if p[5] == '{' else p[5]
    if p[3]:
        p[0] = exp


def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()
