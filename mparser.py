import ply.yacc as yacc
from scanner import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left','LT','GT', 'GTE', 'LTE', 'EQ', 'DIFF'),
    ('left','+','-'),
    ('left','*','/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', ':'),
    ('right', 'UMINUS'),
    ('nonassoc',    'IFX'),
    ('nonassoc',    'ELSE'),

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
                         | for
                         | statement_block """
    #     | for

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

# RETURN -----------------------------------------

def p_return_statement(p):
    """statement : RETURN
                 | RETURN expression"""

def p_break_continue_statement(p):
    """statement : BREAK
                 | CONTINUE """

# EXPRESSION -------------------------------------
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTDIV expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression"""

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
    """range : expression ':' expression"""
    print("range")

def p_index_ref(p):
    """index_ref : expression
                | range
                | index_ref ',' expression
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

# IF FOR WHILE -------------------------------------------------
def p_statement_block(p):
    """statement_block : '{' statements '}' """
    print("statement_block")

def p_if(p):
    """if : IF '(' logical ')' any_statement %prec IFX
            |  IF '(' logical ')' any_statement else_block
    """
    print("if")

def p_else(p):
    """else_block : ELSE any_statement
    """
    print("else")

def p_while(p):
    """while : WHILE '(' logical ')' any_statement
    """
    print("while")

def p_for(p):
    """for : FOR ID '=' range any_statement
    """
    print("for")

# ERROR -------------------------------------------------
def p_error(p):
    if p:
        print(f"--Syntax error: \n\t({p.lineno}), token: type {p.type}, '{p.value}'")
    else:
        print("--Syntax error: No more input")


parser = yacc.yacc()

