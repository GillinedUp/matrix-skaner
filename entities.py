class Node(object):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction


class BracedInstructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Assign(Node):
    def __init__(self, variable, assign_op, expression):
        self.variable = variable
        self.assign_op = assign_op
        self.expression = expression


class Variable(Node):
    def __init__(self, value):
        self.value = value
        self.type = type(value)


class ArrayRef(Node):
    def __init__(self, matrix_name, index):
        self.matrix_name = matrix_name
        self.index = index


class MatrixIndexes(Node):
    def __init__(self, dim_index, index):
        self.dim_index = dim_index
        self.index = index


class UnaryExpr(Node):
    def __init__(self, operator, expr):
        self.expr = expr
        self.operator = operator


class BinaryExpr(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class ZerosMatrixInit(Node):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class OnesMatrixInit(Node):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns


class EyeMatrixInit(Node):
    def __init__(self, size):
        self.size = size


class MatrixInit(Node):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row


class MatrixRow(Node):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row


class MatrixVector(Node):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row


class LoopControlInstruction(Node):
    def __init__(self, loop_control):
        self.loop_control = loop_control


class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression


class PrintInstruction(Node):
    def __init__(self, string_expressions):
        self.string_expressions = string_expressions


class StringExpressions(Node):
    def __init__(self, string_expressions, string_expression):
        self.string_expressions = string_expressions
        self.string_expression = string_expression


class IfInstruction(Node):
    def __init__(self, expression, instruction, else_if_instructions, else_instructions):
        self.expression = expression
        self.instruction = instruction
        self.else_if_instructions = else_if_instructions
        self.else_instructions = else_instructions


class WhileInstruction(Node):
    def __init__(self, expression, braced_expression):
        self.expression = expression
        self.braced_expression = braced_expression


class ForInstruction(Node):
    def __init__(self, range_expression, braced_expression):
        self.range_expression = range_expression
        self.braced_expression = braced_expression


class RangeExpression(Node):
    def __init__(self, my_id, expression1, expression2):
        self.my_id = my_id
        self.expression1 = expression1
        self.expression2 = expression2


class Error(Node):
    def __init__(self):
        pass
