import ply.yacc as yacc
from scanner import tokens
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    )

parser = yacc.yacc()
