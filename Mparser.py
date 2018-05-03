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
    ("left", "DOTMUL", "DOTDIV"),
    ("left", 'TRANSP')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(scanner.lexer.lexdata, p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""
    p[0] = p[1]


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = entities.Instructions(p[1], p[2])


def p_braced_instructions(p):
    """braced_instructions : '{' instructions '}'
                           | instruction ';'
    """
    if p[1] == '{':
        p[0] = entities.BracedInstructions(p[2])
    else:
        p[0] = entities.Instructions(None, p[1])


def p_instruction(p):
    """instruction : assign
                   | if_instruction
                   | iteration_instruction
                   | return_instruction
                   | break_instruction
                   | continue_instruction
                   | print_instruction
    """
    p[0] = p[1]


def p_assign(p):
    """assign : variable assign_op expression ';'"""
    p[0] = entities.Assign(p[1], p[2], p[3])


def p_assign_op(p):
    """assign_op : '='
                 | ADDASSIGN
                 | SUBASSIGN
                 | MULASSIGN
                 | DIVASSIGN
    """
    p[0] = p[1]


def p_variable(p):
    """variable : ID
                | ID '[' array_ref ']'
    """
    if len(p) == 2:
        p[0] = entities.Variable(p[1])
    else:
        p[0] = entities.ArrayRef(p[1], p[3])


def p_array_ref(p):
    """array_ref : expression
                 | array_ref ',' expression
                 | expression ':' expression
    """
    if len(p) > 2 and p[2] == ":":
        p[0] = entities.RangeExpression(None, p[1], p[3])
    elif len(p) > 2:
        p[0] = entities.MatrixIndexes(p[1], p[3])
    else:
        p[0] = p[1]


def p_expression(p):
    """expression : variable
                  | constant
                  | unary_expr
                  | binary_expr
                  | matrix_init
    """
    p[0] = p[1]


def p_constant(p):
    """constant : INT
                | FLOAT
    """
    p[0] = p[1]


def p_unary_expr(p):
    """unary_expr : '-' expression
                  | expression TRANSP
    """
    if p[1] == '-':
        p[0] = entities.UnaryExpr(p[1], p[2])
    else:
        p[0] = entities.UnaryExpr(p[2], p[1])


def p_binary_expr(p):
    """binary_expr : expression '+' expression
                   | expression '-' expression
                   | expression '*' expression
                   | expression '/' expression
                   | expression '>' expression
                   | expression '<' expression
                   | expression EQUAL expression
                   | expression NOTEQUAL expression
                   | expression LESSEQUAL expression
                   | expression GREATEREQUAL expression
                   | expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression
    """
    p[0] = entities.BinaryExpr(p[1], p[2], p[3])


def p_matrix_init(p):
    """matrix_init : ZEROS '(' expression ')'
                   | ZEROS '(' expression ',' expression ')'
                   | ONES '(' expression ')'
                   | ONES '(' expression ',' expression ')'
                   | EYE '(' expression ')'
                   | '[' rows ';' rows ']'
                   | '[' rows ']'
    """
    if p[1] == "zeros":
        if len(p) < 7:
            p[0] = entities.ZerosMatrixInit(p[3], None)
        else:
            p[0] = entities.ZerosMatrixInit(p[3], p[5])
    elif p[1] == "ones":
        if len(p) < 7:
            p[0] = entities.OnesMatrixInit(p[3], None)
        else:
            p[0] = entities.OnesMatrixInit(p[3], p[5])
    elif p[1] == "eye":
        p[0] = entities.EyeMatrixInit(p[3])
    else:
        if len(p) > 4:
            p[0] = entities.MatrixInit(p[2], p[4])
        else:
            p[0] = entities.MatrixInit(None, p[2])


def p_rows(p):
    """rows : row ';' rows
            | row
    """
    if len(p) > 2:
        p[0] = entities.MatrixVector(p[1], p[3])
    else:
        p[0] = entities.MatrixVector(None, p[1])


def p_row(p):
    """row : row ',' expression
           | expression
    """
    if len(p) > 2:
        p[0] = entities.MatrixRow(p[1], p[3])
    else:
        p[0] = entities.MatrixRow(None, p[1])


def p_break_instruction(p):
    """break_instruction : BREAK ';'"""
    p[0] = p[1]


def p_continue_instruction(p):
    """continue_instruction : CONTINUE ';'"""
    p[0] = p[1]


def p_return_instruction(p):
    """return_instruction : RETURN expression ';'"""
    p[0] = entities.ReturnInstruction(p[2])


def p_print_instruction(p):
    """print_instruction : PRINT string_expressions ';'"""
    p[0] = entities.PrintInstruction(p[2])


def p_string_expressions(p):
    """string_expressions : string_expressions ',' string_expression
                          | string_expression"""
    if len(p) >= 4:
        p[0] = entities.StringExpressions(p[1], p[3])
    else:
        p[0] = entities.StringExpressions(None, p[1])


def p_string_expression(p):
    """string_expression : STRING
                         | expression"""

    p[0] = entities.StringExpressions(None, p[1])


def p_if_instruction(p):
    """if_instruction : IF '(' expression ')' instructions
                      | IF '(' expression ')' instructions ELSE instructions
                      | IF '(' expression ')' instructions else_if_instruction
                      | IF '(' expression ')' instructions else_if_instruction ELSE instructions
    """
    if len(p) >= 9:
        p[0] = entities.IfInstruction(p[3], p[5], p[6], p[8])
    elif len(p) == 8:
        p[0] = entities.IfInstruction(p[3], p[5], p[7], None)
    elif len(p) == 7:
        p[0] = entities.IfInstruction(p[3], p[5], p[6], None)
    else:
        p[0] = entities.IfInstruction(p[3], p[5], None, None)


def p_else_if_instruction(p):
    """else_if_instruction : ELSE IF '(' expression ')' instructions
                           | ELSE IF '(' expression ')' instructions else_if_instruction
    """
    if len(p) >= 8:
        p[0] = entities.IfInstruction(p[4], p[6], p[7], None)
    else:
        p[0] = entities.IfInstruction(p[4], p[6], None, None)


def p_iteration_instruction(p):
    """iteration_instruction : WHILE '(' expression ')' braced_instructions
                             | FOR range_expression braced_instructions
    """
    if p[1] == "WHILE":
        p[0] = entities.WhileInstruction(p[3], p[5])
    else:
        p[0] = entities.ForInstruction(p[1], p[2])


def p_range_expression(p):
    """range_expression : ID '=' expression ':' expression"""
    p[0] = entities.RangeExpression(p[1], p[3], p[5])


parser = yacc.yacc()
