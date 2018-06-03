import entities
import SymbolTable

import visitor
from Memory import *
from Exceptions import *
import sys
import numpy as np

sys.setrecursionlimit(10000)


def calculateNumeric(x):
    return {
        '+': lambda left, right: left + right,
        '-': lambda left, right: left - right,
        '*': lambda left, right: left * right,
        '/': lambda left, right: left / right,
        '==': lambda left, right: left == right,
        '!=': lambda left, right: left != right,
    }[x]


def calculateMatrices(x):
    return {
        '.+': lambda left, right: np.add(left, right),
        '.-': lambda left, right: np.subtract(left, right),
        '.*': lambda left, right: np.matmul(left, right),
        './': lambda left, right: np.divide(left, right),
        '==': lambda left, right: np.array_equal(left, right),
        '!=': lambda left, right: not np.array_equal(left, right),
    }[x]


def calculateNumericMatrix(x):
    return {
        '*': lambda left, right: left * right,
        '/': lambda left, right: left / right,
        '==': lambda left, right: left == right,
        '!=': lambda left, right: left != right,
    }[x]


class Interpreter(object):
    def __init__(self):
        self.stack = MemoryStack()
        self.stack.__init__(Memory('root'))
        self.level = 0

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(entities.Node)
    def visit(self, node):
        print("Unrecognized node")

    @visitor.when(entities.Instructions)
    def visit(self, node):
        print(node)

        for instruction in node.instructions:
            instruction.accept(self)

    @visitor.when(entities.BracedInstructions)
    def visit(self, node):
        print(node)

        node.instructions.accept(self)

    @visitor.when(entities.Int)
    def visit(self, node):
        return node.value

    @visitor.when(entities.String)
    def visit(self, node):
        return node.value

    @visitor.when(entities.Float)
    def visit(self, node):
        return node.value

    @visitor.when(entities.Assign)
    def visit(self, node):
        print("Variable assignment:  " + str(node.variable.value) + " with value: " + str(node.expression))
        if self.stack.get(str(node.variable.value)) is None:
            self.stack.insert(str(node.variable.value), node.expression.accept(self))
        else:
            self.stack.set(str(node.variable.value), node.expression.accept(self))

    @visitor.when(entities.BinaryExpr)
    def visit(self, node):

        left = self.stack.get(node.left)
        right = self.stack.get(node.right)

        if left is None:
            try:
                left = node.left.accept(self)
            except AttributeError:
                raise AttributeError("Variable " + str(node.left) + " does not exist, line: " + str(node.line))

        if right is None:
            try:
                right = node.right.accept(self)
            except AttributeError:
                raise AttributeError("Variable " + str(node.left) + "does not exist, line: " + str(node.line))

        if type(right) is np.ndarray:
            if type(left) is np.ndarray:
                return calculateMatrices(node.operator)(left, right)
            return calculateNumericMatrix(node.operator)(left, right)

        return calculateNumeric(node.operator)(left, right)

    @visitor.when(entities.UnaryExpr)
    def visit(self, node):
        if node.operator == 'TRANSP':
            expression = self.stack.get(node.expression)
            if expression is None:
                expression = node.expression.accept(self)
            return np.transpose(expression)
        else:
            expression = self.stack.get(node.expression)
            if expression is None:
                expression = node.expression.accept(self)
                return (-1) * expression
            return (-1) * expression

    @visitor.when(entities.ZerosMatrixInit)
    def visit(self, node):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        matrix = np.zeros((rows, columns))
        return matrix

    @visitor.when(entities.OnesMatrixInit)
    def visit(self, node):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        matrix = np.ones((rows, columns))
        return matrix

    @visitor.when(entities.EyeMatrixInit)
    def visit(self, node):
        size = node.rows.accept(self)
        matrix = np.eye(size)
        return matrix

    @visitor.when(entities.MatrixInit)
    def visit(self, node):
        matrixArray = []
        mat = node.rows

        while True:

            rows = mat.rows
            if rows is None:
                rows = mat.row
            row = []

            while rows.row is not None:
                row.append(rows.row.accept(self))
                rows = rows.rows
                if rows is None:
                    break

            mat = mat.row
            matrixArray.append(row[::-1])

            if mat is None:
                break

            if not hasattr(mat, 'rows'):
                break

        print(matrixArray)
        return np.array(matrixArray)
