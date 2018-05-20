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
    """program : instructions
    """
    p[0] = p[1]


def p_instructions(p):
    """instructions : instructions instruction
    """
    p[0] = entities.Instructions(p[1], p[2], p.lineno)


def p_instructions1(p):
    """instructions : instruction
    """
    p[0] = p[1]


def p_braced_instructions(p):
    """braced_instructions : '{' instructions '}'
    """
    p[0] = entities.BracedInstructions(p[2], p.lineno)


def p_braced_instructions1(p):
    """braced_instructions : instruction
    """
    p[0] = p[1]


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
    """assign : variable assign_op expression ';'
    """
    p[0] = entities.Assign(p[1], p[2], p[3], p.lineno)


def p_assign_op(p):
    """assign_op : '='
                 | ADDASSIGN
                 | SUBASSIGN
                 | MULASSIGN
                 | DIVASSIGN
    """
    p[0] = p[1]


def p_variable(p):
    """variable : ID    """
    p[0] = entities.Variable(p[1], p.lineno(1))


def p_variable_array_ref(p):
    """variable :  ID '[' array_ref ']'
    """
    p[0] = entities.ArrayRef(p[1], p[3], p.lineno(1))


def p_array_ref(p):
    """array_ref :  expression
    """
    p[0] = entities.MatrixIndexes(p[1], p.lineno(1))


def p_array_ref_rec(p):
    """array_ref : array_ref ',' array_ref
    """
    p[0] = entities.MatrixExactIndexes(p[1], p[3], p.lineno(1))


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


def p_unary_minus(p):
    """unary_expr : '-' expression
    """
    p[0] = entities.UnaryExpr(p[1], p[2], p.lineno(1))


def p_unary_transp(p):
    """unary_expr : expression TRANSP
    """
    p[0] = entities.UnaryExpr(p[2], p[1], p.lineno(1))


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
    p[0] = entities.BinaryExpr(p[1], p[2], p[3], p.lineno(2))


def p_matrix_zeros_square_init(p):
    """matrix_init : ZEROS '(' expression ')'
    """
    p[0] = entities.ZerosMatrixInit(p[3], p[3], p.lineno(1))


def p_matrix_zeros_init(p):
    """matrix_init :  ZEROS '(' expression ',' expression ')'
    """
    p[0] = entities.ZerosMatrixInit(p[3], p[5], p.lineno(1))


def p_matrix_ones_square_init(p):
    """matrix_init :  ONES '(' expression ')'
    """
    p[0] = entities.OnesMatrixInit(p[3], p[3], p.lineno(1))


def p_matrix_ones_init(p):
    """matrix_init :  ONES '(' expression ',' expression ')'
    """
    p[0] = entities.OnesMatrixInit(p[3], p[5], p.lineno(1))


def p_matrix_eye_init(p):
    """matrix_init : EYE '(' expression ')'"""
    p[0] = entities.EyeMatrixInit(p[3], p.lineno(1))


def p_matrix_rows_init(p):
    """matrix_init : '[' rows ']'
     """
    p[0] = entities.MatrixInit(p[2], p.lineno(1))


def p_rows(p):
    """rows : row ';' rows
    """
    p[0] = entities.MatrixVector(p[1], p[3], p.lineno(1))


def p_rows1(p):
    """rows :  row
    """
    p[0] = entities.MatrixVector(None, p[1], p.lineno(1))


def p_row(p):
    """row : row ',' expression
    """
    p[0] = entities.MatrixRow(p[1], p[3], p.lineno(1))


def p_row1(p):
    """row : expression
    """
    p[0] = entities.MatrixRow(None, p[1], p.lineno(1))


def p_break_instruction(p):
    """break_instruction : BREAK ';'
    """
    p[0] = entities.LoopControlInstruction(p[1])


def p_continue_instruction(p):
    """continue_instruction : CONTINUE ';'
    """
    p[0] = entities.LoopControlInstruction(p[1])


def p_return_instruction(p):
    """return_instruction : RETURN expression ';'
    """
    p[0] = entities.ReturnInstruction(p[2])


def p_print_instruction(p):
    """print_instruction : PRINT string_expressions ';'
    """
    p[0] = entities.PrintInstruction(p[2])


def p_string_expressions(p):
    """string_expressions : string_expressions ',' string_expression
    """
    p[0] = entities.StringExpressions(p[1], p[3])


def p_string_expressions_single(p):
    """string_expressions : string_expression
    """
    p[0] = entities.StringExpressions(None, p[1])


def p_string_expression(p):
    """string_expression : STRING
                         | expression
    """
    p[0] = entities.StringExpressions(None, p[1])


def p_if_instruction(p):
    """if_instruction : IF '(' expression ')' braced_instructions
    """
    p[0] = entities.IfInstruction(p[3], p[5], None)


def p_if_instruction_else(p):
    """if_instruction : IF '(' expression ')' braced_instructions ELSE braced_instructions
    """
    p[0] = entities.IfInstruction(p[3], p[5], p[7])


def p_iteration_instruction(p):
    """iteration_instruction : WHILE '(' expression ')' braced_instructions
    """
    p[0] = entities.WhileInstruction(p[3], p[5])


def p_iteration_instruction_for(p):
    """iteration_instruction : FOR range_expression braced_instructions
    """
    p[0] = entities.ForInstruction(p[2], p[3])


def p_range_expression(p):
    """range_expression : ID '=' expression ':' expression"""
    p[0] = entities.RangeExpression(p[1], p[3], p[5])


parser = yacc.yacc()
