import ply.yacc as yacc
from src.astt.tree_printer import *
from src.scanner.scanner import tokens
tokens  # added to force scanner.tokens dependency

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
    p[0] = Program(p.lexer.lineno, p[1])

def p_empty(p):
    """empty :"""
    p[0] = Empty(p.lexer.lineno)

def p_statements(p):
    """statements : any_statement
                 | statements any_statement
                """
    if len(p) == 2:
        p[0] = Statements(p.lexer.lineno, [p[1]])
    else:
        p[0] = Statements(p.lexer.lineno, p[1].children+[p[2]])

def p_any_statements(p):
    """any_statement : no_semi_statement
                    | statement ';' """
    p[0] = Statement(p.lexer.lineno, p[1])

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
    p[0] = Print(p.lexer.lineno, p[2])

def p_statement_assign(p):
    """statement : id_whole_or_part '=' expression """
    p[0] = Assign(p.lexer.lineno, p[1], p[2], p[3])

def p_id_whole_or_part(p):
    """id_whole_or_part : ID """
    p[0] = Identifier(p.lexer.lineno, p[1])

def p_id_whole_or_part2(p):
    """id_whole_or_part : id_partial """
    p[0] = p[1]

def p_statement_update(p):
    """statement : id_whole_or_part ADDASSIGN expression
                | id_whole_or_part SUBASSIGN expression
                | id_whole_or_part DIVASSIGN expression
                | id_whole_or_part MULASSIGN expression"""
    p[0] = Assign(p.lexer.lineno, p[1], p[2], p[3])


# RETURN -----------------------------------------

def p_return_statement(p):
    """statement : RETURN
                 | RETURN expression"""
    p[0] = Return(p.lexer.lineno) if len(p) == 2 else Return(p[2])

def p_break_statement(p):
    """statement : BREAK"""
    p[0] = Break(p.lexer.lineno)

def p_continue_statement(p):
    """statement : CONTINUE """
    p[0] = Continue(p.lexer.lineno)

# EXPRESSION -------------------------------------
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UMinus(p.lexer.lineno, p[2])

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTDIV expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression"""
    p[0] = BinOp(p.lexer.lineno, *p[1:])

def p_expression_number(p):
    '''expression : number
                  | list
                  | logical
                  | id_partial
                  '''
    p[0] = Expression(p.lexer.lineno, p[1])

def p_expression_name(p):
    """expression : ID"""
    p[0] = Expression(p.lexer.lineno, Identifier(p.lexer.lineno, p[1]))

def p_expression_string(p):
    """expression : STR """
    p[0] = Expression(p.lexer.lineno, StringM(p.lexer.lineno, p[1]))

def p_expression_group(p):
    """expression : '(' expression  ')' """
    p[0] = Expression(p.lexer.lineno, p[2])

def p_create_matrix(p):
    """expression : ZEROS '(' value_list ')'
                  | ONES '(' value_list ')'
                  | EYE '(' value_list ')'
    """
    p[0] = MatrixCreator(p.lexer.lineno, p[1], p[3])

def p_expression_transpose(p):
    """expression : expression "\'" """
    p[0] = Expression(p.lexer.lineno, Transpose(p.lexer.lineno, p[1]))

# NUMERICAL ------------------------------------------------
def p_number_float(p):
    """number : FLOAT """
    p[0] = Number(p.lexer.lineno, FloatNum(p.lexer.lineno, p[1]))

def p_number_int(p):
    """number : INTNUM """
    p[0] = Number(p.lexer.lineno, IntNum(p.lexer.lineno, p[1]))


# INDEX_REF ------------------------------------------------
def p_range(p):
    """range : expression ':' expression"""
    p[0] = Range(p.lexer.lineno, p[1], p[3])

def p_index_ref(p):
    """index_ref : expression
                | range
                | index_ref ',' expression
                | index_ref ',' range"""
    if len(p) == 2:
        p[0] = IndexRef(p.lexer.lineno, [p[1]])
    else:
        p[0] = IndexRef(p.lexer.lineno, p[1].children+[p[3]])

def p_matrix_part(p):
    """id_partial : ID '[' index_ref ']' """
    p[0] = PartialId(p.lexer.lineno, Identifier(p.lexer.lineno, p[1]), p[3])

# # LIST -----------------------------------------------------
def p_list(p):
    """list : '[' value_list ']'
                | '[' ']' """
    if len(p) == 4:
        p[0] = List(p.lexer.lineno, p[2])
    else:
        p[0] = List(p.lexer.lineno, None)


def p_num_list_extend(p):
    """value_list : expression
                  | value_list ','  expression
    """
    if len(p) == 2:
        p[0] = ValueList(p.lexer.lineno, [p[1]])
    else:
        p[0] = ValueList(p.lexer.lineno, p[1].children+[p[3]])

# LOGICAL -------------------------------------------------
def p_logical(p):
    """logical : expression EQ expression
                | expression LT expression
                | expression GT expression
                | expression LTE expression
                | expression GTE expression
                | expression DIFF expression
    """
    p[0] = Logical(p.lexer.lineno, *p[1:])

# IF FOR WHILE -------------------------------------------------
def p_statement_block(p):
    """statement_block : '{' statements '}' """
    p[0] = p[2]

def p_if(p):
    """if : IF '(' logical ')' any_statement %prec IFX
            |  IF '(' logical ')' any_statement else_block
    """
    if len(p) == 6:
        p[0] = If(p.lexer.lineno, p[3], p[5])
    else:
        p[0] = If(p.lexer.lineno, p[3], p[5], p[6])

def p_else(p):
    """else_block : ELSE any_statement
    """
    p[0] = ElseBlock(p.lexer.lineno, p[2])

def p_while(p):
    """while : WHILE '(' logical ')' any_statement
    """
    p[0] = While(p.lexer.lineno, p[3], p[5])

def p_for(p):
    """for : FOR ID '=' range any_statement
    """
    p[0] = For(p.lexer.lineno, Identifier(p.lexer.lineno, p[2]), p[4], p[5])



# ERROR -------------------------------------------------
def p_error(p):
    if p:
        print(f"--Syntax error: \n\t({p.lexer.lineno}), token: type {p.type}, '{p.value}'")
    else:
        print("--Syntax error: No more input")


parser = yacc.yacc()

