#!/usr/bin/python
import entities
from SymbolTable import SymbolTable, MatrixSymbol, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, entities.Node):
    #                         self.visit(item)
    #             elif isinstance(child, entities.Node):
    #                 self.visit(child)

    #simpler version of generic_visit, not so general
    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif node is not None:
            for child in node.children:
                self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.type = ""
        self.function = ""
        self.varDict = {}
        self.rowsLengths = {}

    def visit_Instructions(self, node):
        self.visit(node.instructions)

    # TODO
    def visit_BracedInstructions(self, node):
        print(node)

    def visit_Assign(self, node):
        self.visit(node.assign_op)
        assigments = self.visit(node.expression)

        if assigments is not None:
            if isinstance(node.expression, entities.ZerosMatrixInit) \
                    or isinstance(node.expression, entities.OnesMatrixInit) \
                    or isinstance(node.expression, entities.EyeMatrixInit):
                self.table.put(str(node.variable.value),
                               MatrixSymbol(node.assign_op, node.expression, node.expression.columns,
                                            node.expression.rows))
            elif isinstance(assigments, entities.MatrixVector):
                self.table.put(str(node.variable.value), MatrixSymbol(node.assign_op, node.expression, self.rows, self.elements / self.rows))
            else:
                self.table.put(str(node.variable.value), VariableSymbol(node.assign_op, node.expression))

    def visit_ZerosMatrixInit(self, node):
        columns = self.visit(node.columns)
        rows = self.visit(node.rows)

        if self.check_matrix_init(rows, node):
            return None
        if columns is None:
            return node
        if self.check_matrix_init(columns, node):
            return None;

        return node;

    def check_matrix_init(self, dim, node):
        if not isinstance(dim, int) and not isinstance(dim, entities.BinaryExpr):
            print("Error: Zeros Matrix size has incorrect type {}, line {}".format(dim, node.line))
            return True
        if isinstance(dim, int) and dim <= 0:
            print("Error: Zeros Matrix size is a non positive size of {}, line {}".format(dim, node.line))
            return True

    def visit_int(self, node):
        return node

    def visit_float(self, node):
        return node

    def visit_str(self, node):
        return 'string'

    def visit_UnaryExpr(self, node):
        if node.operator is '-':
            if isinstance(self.visit(node.expression), int):
                return -self.visit(node.expression)
            return 'negative'
        return 'transp'

    def visit_Variable(self, node):
        try:
            return self.visit((self.table.get(node.value)).value)
        except AttributeError:
            return None

    def visit_ArrayRef(self, node):
        matrix = self.table.get(node.matrix_name)

        if matrix is None or not isinstance(matrix, MatrixSymbol):
            print("Error: Variable {} is not a matrix, line {}".format(node.matrix_name, node.line))
            return None

        if isinstance(node.index, entities.MatrixIndexes):
            if matrix.columns > 1:
                print("Error: Cannot access 2D matrix {} with only one index, line {}".format(node.matrix_name, node.line))
                return None
            return node
        else:
            if matrix.columns == 1 and node.index.row is not None:
                print("Cannot access 1D matrix {} with two indexes, line {}".format(node.matrix_name, node.line))
                return None

        try:

            columns = self.visit(node.index.dim_index)
            if columns >= matrix.columns:
                print("Error: Index {} out of matrix bounds, line {}".format(columns, node.line))
                return None

            rows = self.visit(node.index.index)
            if rows >= matrix.rows:
                print("Error: Index {} out of matrix bounds, line {}".format(rows, node.line))
                return None
            return node
        except TypeError:
            print("Error: Invalid matrix index, line {}".format(node.line))
            return None

    def visit_MatrixInit(self, node):
        self.rows = 0
        self.elements = 0
        vector = self.visit(node.rows)
        return vector

    def visit_MatrixVector(self, node):
        self.rows += 1
        rowIndex = self.rows
        self.rowsLengths[rowIndex] = 0

        self.visit(node.rows)
        self.visit(node.row)

        if self.elements != (self.rowsLengths[rowIndex] * self.rows):
            print("Error: incorrect matrix dimensions, line {}".format(node.line))
            return None

        return node

    def visit_MatrixRow(self, node):
        self.visit(node.rows)
        self.visit(node.row)
        self.rowsLengths[self.rows] += 1
        self.elements += 1

    def visit_MatrixIndexes(self, node):
        return self.visit(node.index)

    def visit_BinaryExpr(self, node):
        left = self.table.get(str(node.left))
        right = self.table.get(str(node.right))

        matrix1_rows, matrix1_columns, matrix2_rows, maatrix2_columns = 0, 0, 0, 0

        if left is None:
            lfet = self.visit(node.left)
            if isinstance(node.left, entities.MatrixInit):
                matrix1_rows = self.rows
                matrix1_columns = self.elements / self.rows

        if right is None:
            right = self.visit(node.right)
            if isinstance(node.right, entities.MatrixInit):
                matrx2_rows = self.rows
                matrix2_columns  = self.elements / self.rows








