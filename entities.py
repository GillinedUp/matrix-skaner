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
