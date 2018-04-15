#!/usr/bin/python
import entities
import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("nonassoc", '<', '>', 'EQUAL', 'NOTEQUAL', 'LESSEQUAL', 'GREATEREQUAL'),
    ("nonassoc", "IF"),
    ("nonassoc", "ELSE"),
    ("left", '+', '-'),
    ("left", "*", "/"),
    ("left", "DOTADD", "DOTSUB"),
    ("left", "DOTMUL", "DOTDIV")
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""
    p[0] = p[1]


def p_instructions(p):
    """instructions : instructions instruction | instruction """
    if len(p) == 2:
        p[0] = entities.Instructions(p[1], None)
    else:
        p[0] = entities.Instructions(p[1], p[2])


def end_of_the_line_instruction(p):
    """end_of_the_line_instruction : instruction ';'"""
    p[0] = entities.Instructions(None, p[1])


def p_braced_instructions(p):
    """braced_instructions : '{' instructions '}' | instruction ';'"""
    if p[1] == '{':
        p[0] = entities.BracedInstructions(p[2])
    else:
        p[0] = entities.Instructions(None, p[1])


def p_instruction(p):
    """instruction: assign |
                    if_instructions |
                    for_instruction |
                    while_instruction |
                    return_instruction |
                    break_instruction |
                    continue_instruction |
                    print_instruction
    """
    p[0] = p[1]


def p_assign(p):
    """assign : variable assign_op expression"""
    p[0] = entities.Assign(p[1], p[2], p[3])


def p_assign_op(p):
    """assign_op : '=' |
                    ADDASIGN |
                    SUBASSIGN |
                    MULASSIGN |
                    DIVASSIGN
    """
    p[0] = p[1]


def p_variable(p):
    """variable : ID |
                ID '[' array_ref ']'
                """
    if len(p) == 2:
        p[0] = entities.Variable(p[1])
    else:
        p[0] = entities.ArrayRef(p[1], p[3])


def p_array_ref(p):
    """array_ref : ID |
                   expression |
                   array_ref ',' array_ref
    """
    if len(p) > 2:
        p[0] = entities.MatrixIndexes(p[1], p[3])
    else:
        p[0] = entities.MatrixIndexes[None, p[1]]


def p_expression(p):
    """expression:  variable |
                    constant |
                    unary_expr |
                    binary_expr |
                    matrix_init
    """
    p[0] = p[1]


def p_constant(p):
    """constant: INT |
                 FLOAT
    """
    p[0] = p[1]


def p_unary_expr(p):
    """unary_expr : '-' expression |
                    expression TRANSP
    """
    if p[1] == '-':
        p[0] = entities.UnaryExpr(p[1], p[2])
    else:
        p[1] = entities.UnaryExpr(p[2], p[1])


def p_binary_expr(p):
    """binary_expr : expression '+' expression |
                     expression '-' expression |
                     expression '*' expression |
                     expression '/' expression |
                     expression '>' expression |
                     expression '<' expression |
                     expression EQUAL expression |
                     expression NOTEQUAL expression |
                     expression LESSEQUAL expression |
                     expression GREATEREQUAL expression |
                     expression DOTADD expression |
                     expression DOTSUB expression |
                     expression DOTMUL expression |
                     expression DOTDIV expression |
    """
    p[0] = entities.BinaryExpr(p[1], p[2], p[3])


def p_matrix_init(p):
    """matrix_init: ZEROS '( expression ')' |
                    ZEROS '(' expression ',' expression ')' |
                    ONES '(' expression ')' |
                    ONES '(' expression ',' expression ')' |
                    EYE '(' expression ')' |
                    '[' rows ';' row ']' |
                    '[' row ']'
    """
    if p[1] == "ZEROS":
        if len(p) < 7:
            p[0] = entities.ZerosMatrixInit(p[3], None)
        else:
            p[0] = entities.ZerosMatrixInit(p[3], p[5])
    elif p[1] == "ONES":
        if len(p) < 7:
            p[0] = entities.OnesMatrixInit(p[3], None)
        else:
            p[0] = entities.OnesMatrixInit(p[3], p[5])
    elif p[1] == "EYE":
        p[0] = entities.EyeMatrixInit(p[3])
    else:
        if len(p) > 4:
            p[0] = entities.MatrixInit(p[2], p[4])
        else:
            p[0] = entities.MatrixInit(None, p[2])


def p_rows(p):
    """rows : rows ';' row |
              row
     """
    if len(p) > 2:
        p[0] = entities.MatrixInit(p[1], p[3])
    else:
        p[0] = entities.MatrixInit(None, p[1])


def p_row(p):
    """row : row ',' expression |
            expression
    """
    if len(p) > 2:
        p[0] = entities.MatrixInit(p[1], p[3])  # not sure
    else:
        p[0] = entities.MatrixInit(None, p[1])


# if, if else,for, while, return, continue, break, print, string, range (?)
#  instructions to do

parser = yacc.yacc()
