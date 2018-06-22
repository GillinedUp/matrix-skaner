import entities
import SymbolTable

import visitor
from Memory import *
from Exceptions import *
import sys
import numpy as np

sys.setrecursionlimit(10000)


class Indexes:
    def __init__(self):
        self.indexes = []
        self.dim = 0

    def add(self, index):
        self.indexes.append(index)
        self.dim += 1


def calculateNumeric(x):
    return {
        '+': lambda left, right: left + right,
        '-': lambda left, right: left - right,
        '*': lambda left, right: left * right,
        '/': lambda left, right: left / right,
        '==': lambda left, right: left == right,
        '!=': lambda left, right: left != right,
        '<': lambda left, right: left < right,
        '>': lambda left, right: left > right,
        '>=': lambda left, right: left >= right,
        '<=': lambda left, right: left <= right,
    }[x]


def calculateMatrices(x):
    return {
        '.+': lambda left, right: left + right,
        '.-': lambda left, right: left - right,
        '.*': lambda left, right: left * right,
        './': lambda left, right: left / right,
        '+': lambda left, right: np.add(left, right),
        '-': lambda left, right: np.subtract(left, right),
        '*': lambda left, right: np.matmul(left, right),
        '/': lambda left, right: np.divide(left, right),
        '==': lambda left, right: np.array_equal(left, right),
        '!=': lambda left, right: not np.array_equal(left, right),
    }[x]


def calculateNumericMatrix(x):
    return {
        '==': lambda left, right: left == right,
        '!=': lambda left, right: left != right,
        '.*': lambda left, right: left * right,
        './': lambda left, right: left / right,
        '.+': lambda left, right: left + right,
        '.-': lambda left, right: left - right,
    }[x]


def get_new_value(operator):
    return {
        '=': lambda old_value, value: value,
        '+=': lambda old_value, value: old_value + value,
        "-=": lambda old_value, value: old_value - value,
        "*=": lambda old_value, value: old_value * value,
        "/=": lambda old_value, value: old_value / value,

    }[operator]


class Interpreter(object):
    def __init__(self):
        self.stack = MemoryStack()
        self.stack.__init__(Memory('root'))
        self.level = 0

    def createMatrix(self, matrix_type, node):
        rows = node.rows.accept(self)
        columns = node.columns.accept(self)
        return {
            'zeros': np.zeros((rows, columns)),
            'ones': np.ones((rows, columns))
        }[matrix_type]

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
        for instruction in node.instructions:
            instruction.accept(self)

    @visitor.when(entities.Assign)
    def visit(self, node):
        value = node.expression.accept(self)

        if isinstance(node.variable, entities.ArrayRef):
            matrix = self.stack.get(node.variable.matrix_name)
            indexes = node.variable.index.accept(self)
            if isinstance(indexes, Indexes):
                dim = indexes.dim
                index = 0
                i = 0
                for ind in indexes.indexes:
                    elements = 1
                    for n in matrix.shape[dim - 1 + i:]:
                        elements *= n
                    index += elements * ind
                    i += 1

                old_value = np.take(matrix, [index])[0]
                new_value = get_new_value(node.assign_op)(old_value, value)
                np.put(matrix, [index], new_value)
                # print("Updated " + str(node.variable.matrix_name) + str(indexes.indexes) + " with value " + str(new_value))
            else:
                old_value = matrix[0, indexes]
                new_value = get_new_value(node.assign_op)(old_value, value)
                matrix[0, indexes] = new_value
                # print("Updated " + str(node.variable.matrix_name) + "[" + str(indexes) + "]" + " with value " + str(
                #     new_value))
        elif self.stack.get(str(node.variable.value)) is None:
            # print("Added variable " + str(node.variable.value) + " with value " + str(
            #     value))
            self.stack.insert(str(node.variable.value), value)
        else:
            old_value = self.stack.get(str(node.variable.value))
            new_value = get_new_value(node.assign_op)(old_value, value)
            self.stack.set(str(node.variable.value), new_value)
            # print("Updated " + str(node.variable.value) + " with value " + str(
            #     new_value))

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

    @visitor.when(entities.MatrixIndexes)
    def visit(self, node):
        return node.index.accept(self)

    @visitor.when(entities.MatrixExactIndexes)
    def visit(self, node):
        indexes = Indexes()
        indexes.add(node.dim_index.accept(self))
        indexes.add(node.index.accept(self))
        return indexes

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

        if type(left) is np.ndarray:
            return calculateNumericMatrix(node.operator)(left, right)

        return calculateNumeric(node.operator)(left, right)

    @visitor.when(entities.UnaryExpr)
    def visit(self, node):
        if node.operator == 'TRANSP':
            expression = self.stack.get(node.expression)
            if expression is None:
                expression = node.expression.accept(self)
            return np.transpose(expression)
        elif node.operator == '-':
            expression = self.stack.get(node.expression)
            if expression is None:
                expression = node.expression.accept(self)
            return (-1) * expression

    @visitor.when(entities.ZerosMatrixInit)
    def visit(self, node):
        return self.createMatrix('zeros', node)

    @visitor.when(entities.OnesMatrixInit)
    def visit(self, node):
        return self.createMatrix('ones', node)

    @visitor.when(entities.EyeMatrixInit)
    def visit(self, node):
        size = node.rows.accept(self)
        matrix = np.eye(size)
        return matrix

    @visitor.when(entities.MatrixInit)
    def visit(self, node):
        matrix_array = []
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
                matrix_array.append(cur_row)
                break

            if len(cur_row) > 0:
                matrix_array.append(cur_row[::-1])

        return np.array(matrix_array)

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
        string_expression = node.string_expression
        if isinstance(string_expression, str):
            return string_expression.replace('"', "")
        return string_expression.accept(self)

    @visitor.when(entities.StringExpressions)
    def visit(self, node):
        string = ""
        for s in node.string_expressions:
            string += str(s.accept(self)) + " "

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
            except:
                break

        self.stack.pop()
        return result

        # w bloku try ... except łapiemy wszystkie możliwe wyjątki, więc wykonanie
        # programu zawsze dojdzie do tego miejsca, i seft.stack.pop() zawsze się wykona.
        # Jeśli dodamy blok finally do pętli, to self.stack.pop() będzie wykonywał się tyle
        # razy ile pętla, co jest błędne. Jeśli dodamy pętle wewnątrz bloku try ... except,
        # to interpreter Pythona zgłosi błąd, że instrukcje continue i break są poza pętlą.

    @visitor.when(entities.RangeExpression)
    def visit(self, node):
        start = node.expression1.accept(self)
        end = node.expression2.accept(self)
        range_expression = range(start, end)
        return node.my_id, range_expression

    @visitor.when(entities.ForInstruction)
    def visit(self, node):
        self.stack.push(Memory("for"))
        my_id, range_expression = node.range_expression.accept(self)
        result = None
        for val in range_expression:
            try:
                if self.stack.get(str(my_id)) is None:
                    self.stack.insert(str(my_id), val)
                else:
                    self.stack.set(str(my_id), val)
                result = node.braced_expression.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            except:
                break

        self.stack.pop()
        return result

        # w bloku try ... except łapiemy wszystkie możliwe wyjątki, więc wykonanie
        # programu zawsze dojdzie do tego miejsca, i seft.stack.pop() zawsze się wykona.
        # Jeśli dodamy blok finally do pętli, to self.stack.pop() będzie wykonywał się tyle
        # razy ile pętla, co jest błędne. Jeśli dodamy pętle wewnątrz bloku try ... except,
        # to interpreter Pythona zgłosi błąd, że instrukcje continue i break są poza pętlą.
