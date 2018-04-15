class Instructions(object):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction


class BracedInstructions(object):
    def __init__(self, instructions):
        self.instructions = instructions


class Assign(object):
    def __init__(self, variable, assign_op, expression):
        self.variable = variable
        self.assign_op = assign_op
        self.expression = expression


class Variable(object):
    def __init__(self, value):
        self.value = value
        self.type = type(value)


class ArrayRef(object):
    def __init__(self, matrix_name, index):
        self.matrix_name = matrix_name
        self.index = index


class MatrixIndexes(object):
    def __init__(self, dim_index, index):
        self.dim_index = dim_index
        self.index = index


class UnaryExpr(object):
    def __init__(self, operator, expr):
        self.expr = expr
        self.operator = operator


class BinaryExpr(object):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class ZerosMatrixInit(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class OnesMatrixInit(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class EyeMatrixInit(object):
    def __init__(self, size):
        self.size = size


class MatrixInit(object):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row


class ReturnInstruction(object):
    def __init__(self, expression):
        self.expression = expression


class PrintInstruction(object):
    def __init__(self, string_expressions):
        self.string_expressions = string_expressions


class StringExpressions(object):
    def __init__(self, string_expressions, string_expression):
        self.string_expressions = string_expressions
        self.string_expression = string_expression


class IfInstruction(object):
    def __init__(self, expression, instructions, else_if_instructions, else_instructions):
        self.expression = expression
        self.instructions = instructions
        self.else_if_instructions = else_if_instructions
        self.else_instructions = else_instructions


class WhileInstruction(object):
    def __init__(self, expression, braced_expression):
        self.expression = expression
        self.braced_expression = braced_expression


class ForInstruction(object):
    def __init__(self, range_expression, braced_expression):
        self.range_expression = range_expression
        self.braced_expression = braced_expression


class RangeExpression(object):
    def __init__(self, my_id, expression1, expression2):
        self.my_id = my_id
        self.expression1 = expression1
        self.expression2 = expression2
