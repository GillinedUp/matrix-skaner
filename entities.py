class Node(object):
    def __init__(self, instructions, line):
        self.instructions = instructions
        self.line = line


class Instructions(Node):
    def __init__(self, instructions, instruction, line):
        self.instructions = []
        self.instructions.append(instructions)
        self.instructions.append(instruction)
        self.line = line


class BracedInstructions(Node):
    def __init__(self, instructions, line):
        self.instructions = []
        self.instructions.append(instructions)
        self.line = line


class Assign(Node):
    def __init__(self, variable, assign_op, expression, line):
        self.variable = variable
        self.assign_op = assign_op
        self.expression = expression
        self.line = line


class Variable(Node):
    def __init__(self, value, line):
        self.value = value
        self.type = type(value)
        self.line = line


class ArrayRef(Node):
    def __init__(self, matrix_name, index, line):
        self.matrix_name = matrix_name
        self.index = index
        self.line = line


class MatrixExactIndexes(Node):
    def __init__(self, dim_index, index, line):
        self.dim_index = dim_index
        self.index = index
        self.line = line


class MatrixIndexes(Node):
    def __init__(self, index, line):
        self.index = index
        self.line = line


class UnaryExpr(Node):
    def __init__(self, operator, expr, line):
        self.expression = expr
        self.operator = operator
        self.line = line


class BinaryExpr(Node):
    def __init__(self, left, operator, right, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line


class ZerosMatrixInit(Node):
    def __init__(self, rows, columns, line):
        self.rows = rows
        self.columns = columns
        self.line = line


class OnesMatrixInit(Node):
    def __init__(self, rows, columns, line):
        self.rows = rows
        self.columns = columns
        self.line = line


class EyeMatrixInit(Node):
    def __init__(self, size, line):
        self.rows = size
        self.columns = size
        self.line = line


class MatrixInit(Node):
    def __init__(self, rows, line):
        self.rows = rows
        self.line = line


class MatrixRow(Node):
    def __init__(self, rows, row, line):
        self.rows = rows
        self.row = row
        self.line = line


class MatrixVector(Node):
    def __init__(self, rows, row, line):
        self.rows = rows
        self.row = row
        self.line = line;


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
    def __init__(self, expression, instruction, else_if_instructions):
        self.expression = expression
        self.instruction = instruction
        self.else_if_instructions = else_if_instructions


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
