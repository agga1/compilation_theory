import ply.yacc as yacc
from TreePrinter import *
from scanner import tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', '=', 'SUBASSIGN', 'ADDASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('left','LT','GT', 'GTE', 'LTE', 'EQ', 'DIFF'),
    ('left','+','-'),
    ('left','*','/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', ':'),
    ("right", 'ID', '['),
    ('right', 'UMINUS'),
    ('left','\''),
)
# Precedence rules for the arithmetic operators

# dictionary of names (for storing variables)
names = { }

# statement
def p_start(p):
    """start : statements
            | empty
             """
    p[0] = Program(p[1])

def p_statements(p):
    """statements : any_statement
                 | statements any_statement
                """
    if len(p) == 2:
        p[0] = Statements([p[1]])
    else:
        p[0] = Statements(p[1].statements+[p[2]])

def p_any_statements(p):
    """any_statement : no_semi_statement
                    | statement ';' """
    p[0] = Statement(p[1])

def p_no_semi_statements(p):
    """no_semi_statement : if
                         | while
                         | for
                         | statement_block """
    p[0] = p[1]

def p_statement_expr(p):
    """statement : expression
                """
    p[0] = p[1]

def p_statement_print(p):
    """statement : PRINT value_list"""
    p[0] = Print(p[2])

def p_statement_assign(p):
    """statement : id_whole_or_part '=' expression """
    p[0] = Assign(p[1], p[2], p[3])

def p_id_whole_or_part(p):
    """id_whole_or_part : ID """
    p[0] = Identifier(p[1])

def p_id_whole_or_part2(p):
    """id_whole_or_part : id_partial """
    p[0] = p[1]

def p_statement_update(p):
    """statement : id_whole_or_part ADDASSIGN expression
                | id_whole_or_part SUBASSIGN expression
                | id_whole_or_part DIVASSIGN expression
                | id_whole_or_part MULASSIGN expression"""
    p[0] = Assign(p[1], p[2], p[3])


# RETURN -----------------------------------------

def p_return_statement(p):
    """statement : RETURN
                 | RETURN expression"""
    p[0] = Return() if len(p) == 2 else Return(p[2])

def p_break_statement(p):
    """statement : BREAK"""
    p[0] = Break()

def p_continue_statement(p):
    """statement : CONTINUE """
    p[0] = Continue()

# EXPRESSION -------------------------------------
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UMinus(p[2])

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTDIV expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression"""
    p[0] = BinOp(*p[1:])

def p_expression_number(p):
    '''expression : number
                  | list
                  | logical
                  | id_partial
                  '''
    p[0] = Expression(p[1])

def p_expression_name(p):
    """expression : ID"""
    p[0] = Expression(Identifier(p[1]))

def p_expression_string(p):
    """expression : STR """
    p[0] = Expression(String(p[1]))

def p_expression_group(p):
    """expression : '(' expression  ')' """
    p[0] = Expression(p[1])

def p_create_matrix(p):
    """expression : ZEROS '(' INTNUM ')'
                  | ONES '(' INTNUM ')'
                  | EYE '(' INTNUM ')'
    """
    p[0] = MatrixCreator(p[1], IntNum(p[3]))

def p_expression_transpose(p):
    """expression : expression "\'" """
    p[0] = Expression(Transpose(p[1]))

# NUMERICAL ------------------------------------------------
def p_number(p):
    """number : INTNUM
              | FLOAT """
    if isinstance(p[1], int):
        p[0] = Number(IntNum(p[1]))
    else:
        p[0] = Number(FloatNum(p[1]))


# INDEX_REF ------------------------------------------------
def p_range(p):
    """range : expression ':' expression"""
    p[0] = Range(p[1], p[3])

def p_index_ref(p):
    """index_ref : expression
                | range
                | index_ref ',' expression
                | index_ref ',' range"""
    if len(p) == 2:
        p[0] = IndexRef([p[1]])
    else:
        p[0] = IndexRef(p[1].values+[p[3]])

def p_matrix_part(p):
    """id_partial : ID '[' index_ref ']' """
    p[0] = PartialId(Identifier(p[1]), p[3])

# # LIST -----------------------------------------------------
def p_list(p):
    """list : '[' value_list ']'
                | '[' ']' """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = ValueList([])


def p_num_list_extend(p):
    """value_list : expression
                  | value_list ','  expression
    """
    if len(p) == 2:
        p[0] = ValueList([p[1]])
    else:
        p[0] = ValueList(p[1].values+[p[3]])

# LOGICAL -------------------------------------------------
def p_logical(p):
    """logical : expression EQ expression
                | expression LT expression
                | expression GT expression
                | expression LTE expression
                | expression GTE expression
                | expression DIFF expression
    """
    p[0] = Logical(*p[1:])

# IF FOR WHILE -------------------------------------------------
def p_statement_block(p):
    """statement_block : '{' statements '}' """
    p[0] = p[2]

def p_if(p):
    """if : IF '(' logical ')' any_statement %prec IFX
            |  IF '(' logical ')' any_statement else_block
    """
    if len(p) == 6:
        p[0] = If(p[3], p[5])
    else:
        p[0] = If(p[3], p[5], p[6])

def p_else(p):
    """else_block : ELSE any_statement
    """
    p[0] = ElseBlock(p[2])

def p_while(p):
    """while : WHILE '(' logical ')' any_statement
    """
    p[0] = While(p[3], p[5])

def p_for(p):
    """for : FOR ID '=' range any_statement
    """
    p[0] = For(Identifier(p[2]), p[4], p[5])

def p_empty(p):
    """empty :"""
    p[0] = Empty()

# ERROR -------------------------------------------------
def p_error(p):
    if p:
        print(f"--Syntax error: \n\t({p.lineno}), token: type {p.type}, '{p.value}'")
    else:
        print("--Syntax error: No more input")


parser = yacc.yacc()

