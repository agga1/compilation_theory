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
    ('left','LT','GT', 'GTE', 'LTE', 'EQ', 'DIFF'),
    ('left','+','-'),
    ('left','*','/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
)

# dictionary of names (for storing variables)
names = { }

# statement
def p_start(p):
    """start : statements
             """
def p_statements(p):
    """statements : any_statement
                 | statements any_statement
                """

def p_any_statements(p):
    """any_statement : no_semi_statement
                    | statement ';' """

def p_no_semi_statements(p):
    """no_semi_statement : if
                         | while
                         | for"""

def p_statement_expr(p):
    """statement : expression
                """
def p_statement_print(p):
    """statement : PRINT expression"""

def p_statement_assign(p):
    """statement : id_whole_or_part '=' expression """

def p_id_whole_or_part(p):
    """id_whole_or_part : ID
                        | id_partial """

def p_statement_update(p):
    """statement : id_whole_or_part ADDASSIGN expression
                | id_whole_or_part SUBASSIGN expression
                | id_whole_or_part DIVASSIGN expression
                | id_whole_or_part MULASSIGN expression"""

# EXPRESSION -------------------------------------
def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTDIV expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression"""


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""

def p_expression_number(p):
    '''expression : number
                  | id_partial
                  | list
                  | STR
                  | logical
                  '''

def p_expression_name(p):
    """expression : ID"""


def p_expression_group(p):
    """expression : '(' expression  ')' """

def p_zeros(p):
    """expression : ZEROS '(' INTNUM ')'"""


def p_ones(p):
    """expression : ONES '(' INTNUM ')'"""


def p_eye(p):
    """expression : EYE '(' INTNUM ')'"""


def p_expression_transpose(p):
    """expression : expression "\'" """

# NUMERICAL ------------------------------------------------
def p_number(p):
    """number : INTNUM
              | FLOAT """

# INDEX_REF ------------------------------------------------
def p_range(p):
    """range : INTNUM ':' INTNUM"""

def p_index_ref(p):
    """index_ref : INTNUM
                | range
                | index_ref ',' INTNUM
                | index_ref ',' range"""

def p_matrix_part(p):
    """id_partial : ID '[' index_ref ']' """

# # LIST -----------------------------------------------------
def p_list(p):
    """list : '[' value_list ']' """

def p_num_list_extend(p):
    """value_list : expression
                  | value_list ','  expression
    """
# LOGICAL -------------------------------------------------
def p_logical(p):
    """logical : expression EQ expression
                | expression LT expression
                | expression GT expression
                | expression LTE expression
                | expression GTE expression
                | expression DIFF expression
    """

# IF  -------------------------------------------------
def p_if(p):
    """if : IF '(' logical ')' any_statement else_block
          | IF '(' logical ')' '{' statements '}' else_block
    """
    print("got if")

def p_else(p):
    """else_block : ELSE any_statement
                  | ELSE '{' statements '}'
    """
    print("got else")

def p_while(p):
    """while : WHILE '(' logical ')' any_statement
          | WHILE '(' logical ')' '{' statements '}'
    """

def p_for(p):
    """for : FOR ID '=' range any_statement
          | FOR ID '=' range '{' statements '}'
    """

# ERROR -------------------------------------------------
def p_error(p):
    print("Syntax error in input!")

# def p_empty(p):
#     'empty :'

parser = yacc.yacc()
