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
        for instruction in node.instructions:
            instruction.accept(self)

    @visitor.when(entities.BracedInstructions)
    def visit(self, node):
        node.instructions.accept(self)

    @visitor.when(entities.Assign)
    def visit(self, node):
        print("Variable assignment:  " + str(node.variable.value) + " with value: ")
        print(node.expression.accept(self))
        if self.stack.get(str(node.variable.value)) is None:
            self.stack.insert(str(node.variable.value), node.expression.accept(self))
        else:
            self.stack.set(str(node.variable.value), node.expression.accept(self))

    @visitor.when(entities.Int)
    def visit(self, node):
        return node.value

    @visitor.when(entities.Float)
    def visit(self, node):
        return node.value

    @visitor.when(entities.String)
    def visit(self, node):
        return node.value

    @visitor.when(entities.Variable)
    def visit(self, node):
        if self.stack.get(node) is not None:
            return self.stack.get(node)
        else:
            return None

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
        rows = node.rows

        while True:
            cur_row = []

            row = rows.rows

            while row is not None and row.row is not None:
                res = row.row.accept(self)
                cur_row.append(res)
                row = row.rows
                if row is None:
                    break

            rows = rows.row

            if not hasattr(rows, "rows"):
                res = rows.accept(self)
                cur_row = cur_row[::-1]
                cur_row.append(res)
                matrixArray.append(cur_row)
                break

            if len(cur_row) > 0:
                matrixArray.append(cur_row[::-1])

        return np.array(matrixArray)

    @visitor.when(entities.LoopControlInstruction)
    def visit(self, node):
        if node.loop_control == "break":
            raise BreakException()
        elif node.loop_control == "continue":
            raise ContinueException()

    @visitor.when(entities.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(node.expression.accept(self))

    @visitor.when(entities.StringExpression)
    def visit(self, node):
        string_expression = node.string_expression.accept(self)
        if isinstance(string_expression, str):
            return string_expression.replace('"', "")
        return string_expression

    @visitor.when(entities.StringExpressions)
    def visit(self, node):
        string = ""
        for s in node.string_expressions:
            string += str(s.accept(self))

        return string

    @visitor.when(entities.PrintInstruction)
    def visit(self, node):
        string_expressions = node.string_expressions.accept(self)
        print(string_expressions)
        return string_expressions

    @visitor.when(entities.IfInstruction)
    def visit(self, node):
        self.stack.push(Memory("if"))
        if node.expression.accept(self):
            node.instructions.accept(self)
        elif node.else_if_instructions is not None:
            node.else_if_instructions.accept(self)
        self.stack.pop()

    @visitor.when(entities.WhileInstruction)
    def visit(self, node):
        result = None
        self.stack.push(Memory("while"))
        while node.expression.accept(self):
            try:
                result = node.braced_expression.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break

        self.stack.pop()
        return result

    @visitor.when(entities.RangeExpression)
    def visit(self, node):
        start = node.expression1.accept(self)
        end = node.expression2.accept(self)
        range_expression = range(start, end)

        if self.stack.get(str(node.my_id)) is None:
            self.stack.insert(str(node.my_id), range_expression)
        else:
            self.stack.set(str(node.my_id), range_expression)

        return range_expression

    @visitor.when(entities.ForInstruction)
    def visit(self, node):
        self.stack.push(Memory("for"))
        for _ in node.range_expression.accept(self):
            try:
                node.braced_expression.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break

        self.stack.pop()
