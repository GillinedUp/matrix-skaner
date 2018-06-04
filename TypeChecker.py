#!/usr/bin/python
import entities
from SymbolTable import SymbolTable, MatrixSymbol, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # simpler version of generic_visit, not so general
    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        # elif node is not None:
        #     for child in node.children:
        #         self.visit.py(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.type = ""
        self.function = ""
        self.varDict = {}
        self.rowsLengths = {}
        self.is_in_loop = False

    def visit_Instructions(self, node):
        self.visit(node.instructions)

    def visit_BracedInstructions(self, node):
        self.visit(node.instructions)

    def visit_Int(self, node):
        return node

    def visit_Float(self, node):
        return node

    def visit_String(self, node):
        return 'string'

    def visit_Assign(self, node):
        self.visit(node.assign_op)
        assignments = self.visit(node.expression)

        if assignments is not None:
            if isinstance(node.expression, entities.ZerosMatrixInit) \
                    or isinstance(node.expression, entities.OnesMatrixInit) \
                    or isinstance(node.expression, entities.EyeMatrixInit):
                self.table.put(str(node.variable.value),
                               MatrixSymbol(node.assign_op,
                                            node.expression,
                                            node.expression.columns.value,
                                            node.expression.rows.value))
            elif isinstance(assignments, entities.MatrixVector):
                self.table.put(str(node.variable.value),
                               MatrixSymbol(node.assign_op,
                                            node.expression,
                                            self.elements // self.rows,
                                            self.rows))
            elif not isinstance(node.variable, entities.ArrayRef):
                self.table.put(str(node.variable.value),
                               VariableSymbol(node.assign_op, node.expression))

    def visit_ZerosMatrixInit(self, node):
        return self.check_matrix(node)

    def visit_OnesMatrixInit(self, node):
        return self.check_matrix(node)

    def visit_EyeMatrixInit(self, node):
        return self.check_matrix(node)

    def check_matrix(self, node):
        columns = self.visit(node.columns)
        rows = self.visit(node.rows)

        if self.check_matrix_init(rows, node):
            return None

        if columns is None:
            return node

        if self.check_matrix_init(columns, node):
            return None

        return node

    def check_matrix_init(self, dim, node):

        if not isinstance(dim, entities.Int) and not isinstance(dim, entities.BinaryExpr):
            print("Error: Matrix size has incorrect type {}, line {}"
                  .format(dim, node.line))
            return True

        if isinstance(dim, entities.Int) and dim.value <= 0:
            print("Error: Matrix size is a non positive size of {}, line {}"
                  .format(dim, node.line))
            return True

    def visit_UnaryExpr(self, node):
        exp = node.expression
        if isinstance(node.expression, entities.Variable):
            exp = self.table.get(node.expression.value)
        if node.operator is '-':
            if isinstance(exp, entities.Int) or isinstance(exp, entities.Float):
                return (-1) * exp.value
            if isinstance(exp, VariableSymbol):
                return exp.value
            return 'NEGATIVE'

        else:
            if isinstance(exp, MatrixSymbol):
                transp = MatrixSymbol(node.operator, exp.value, exp.rows, exp.columns)
                # print("transp: " + str(node.expression.value) + " rows: " + str(transp.rows) + " columns: " + str(transp.columns))
                return transp
            return 'TRANSP'


    def visit_Variable(self, node):
        try:
            return self.visit((self.table.get(node.value)).value)
        except AttributeError:
            return None

    def visit_ArrayRef(self, node):
        matrix = self.table.get(node.matrix_name)

        if matrix is None or not isinstance(matrix, MatrixSymbol):
            print("Error: Variable {} is not a matrix, line {}"
                  .format(node.matrix_name, node.line))
            return None

        if isinstance(node.index, entities.MatrixIndexes):

            if matrix.columns > 1:
                print("Error: Cannot access 2D matrix {} with only one index, line {}"
                      .format(node.matrix_name, node.line))
                return None
            return node

        else:

            if matrix.columns == 1 and node.index.row is not None:
                print("Cannot access 1D matrix {} with two indexes, line {}"
                      .format(node.matrix_name, node.line))
                return None

        try:
            columns = self.visit(node.index.dim_index)

            if columns >= matrix.columns:
                print("Error: Index {} out of matrix bounds, line {}"
                      .format(columns, node.line))
                return None

            rows = self.visit(node.index.index)

            if rows >= matrix.rows:
                print("Error: Index {} out of matrix bounds, line {}"
                      .format(rows, node.line))
                return None

            return node
        except TypeError:
            print("Error: Invalid matrix index, line {}"
                  .format(node.line))
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
        left = node.left
        right = node.right

        if isinstance(node.left, entities.Variable):
            left = self.table.get(str(node.left.value))
        if isinstance(node.right, entities.Variable):
            right = self.table.get(str(node.right.value))

        matrix1_rows, matrix1_columns, matrix2_rows, matrix2_columns = 0, 0, 0, 0

        if left is None:
            left = self.visit(node.left)

            if isinstance(node.left, entities.MatrixInit):
                matrix1_rows = self.rows
                matrix1_columns = self.elements // self.rows

        if right is None:
            right = self.visit(node.right)

            if isinstance(node.right, entities.MatrixInit):
                matrix2_rows = self.rows
                matrix2_columns = self.elements // self.rows

        if right is None or left is None:
            print("Error: Undefined variable, line {}".format(node.line))
            return None
        if isinstance(right, entities.BinaryExpr) or isinstance(left, entities.BinaryExpr):
            return node

        if isinstance(left, VariableSymbol) \
                or isinstance(left, entities.Int) \
                or isinstance(left, entities.Float):

            if isinstance(right, VariableSymbol) \
                    or isinstance(right, entities.Int) \
                    or isinstance(right, entities.Float):

                if node.operator == ".*" \
                        or node.operator == "./" \
                        or node.operator == ".+" \
                        or node.operator == ".-":
                    print("Error: Invalid operation {} for numeric types, line {}"
                          .format(node.operator, node.line))
            else:

                if node.operator != "==" \
                        and node.operator != "!=" \
                        and node.operator != "*" \
                        and node.operator != "/":
                    print(node.left)
                    print(node.right)
                    print("Error: Invalid operation {} for numeric-matrix types, line {}"
                          .format(node.operator, node.line))
        elif not isinstance(left, str):

            if isinstance(left, entities.UnaryExpr):
                left = self.visit(left)
            if isinstance(right, entities.UnaryExpr):
                right = self.visit(right)
            if isinstance(right, str):
                return node

            if isinstance(right, VariableSymbol) \
                    or isinstance(right, entities.Int) \
                    or isinstance(right, entities.Float):

                if node.operator != "==" \
                        and node.operator != "!=":
                    print("Error: Invalid operation {} for matrix-numeric types, line {}"
                          .format(node.operator, node.line))
            else:
                if node.operator != "==" \
                        and node.operator != "!=" \
                        and node.operator != ".+" \
                        and node.operator != ".-" \
                        and node.operator != ".*" \
                        and node.operator != "./":
                    print("Error: Invalid operation {} for matrix types, line {}"
                          .format(node.operator, node.line))
                    return None


                if isinstance(left, entities.ZerosMatrixInit) \
                        or isinstance(left, entities.OnesMatrixInit) \
                        or isinstance(left, entities.EyeMatrixInit):

                    matrix1_columns = left.columns.value
                    matrix1_rows = left.rows.value

                elif matrix1_columns == 0 and matrix1_rows == 0:
                    matrix1_columns = left.columns
                    matrix1_rows = left.rows

                if isinstance(right, entities.ZerosMatrixInit) \
                        or isinstance(right, entities.OnesMatrixInit) \
                        or isinstance(right, entities.EyeMatrixInit):
                    matrix2_columns = right.columns.value
                    matrix2_rows = right.rows.value

                elif matrix2_columns == 0 and matrix2_rows == 0:
                    matrix2_columns = right.columns
                    matrix2_rows = right.rows

                if node.operator == ".+" \
                        or node.operator == ".-":

                    if matrix1_columns != matrix2_columns \
                            or matrix1_rows != matrix2_rows:
                        print("Error: Incompatible matrix sizes: {}x{} and  {}x{} for operation {}, line {}"
                              .format(matrix1_rows, matrix1_columns, matrix2_rows, matrix2_columns,
                                      node.operator, node.line))

                elif node.operator == ".*" or node.operator == "./":

                    if matrix1_columns != matrix2_rows:
                        print("Error: Incompatible matrix sizes: {}x{} and  {}x{} for operation {}, line {}"
                              .format(matrix1_rows, matrix1_columns, matrix2_rows, matrix2_columns,
                                      node.operator, node.line))

        return node

    def visit_RangeExpression(self, node):

        from_expr = self.visit(node.expression1)
        to_expr = self.visit(node.expression2)


        if isinstance(from_expr, entities.Int) \
                and isinstance(to_expr, entities.Int) \
                and from_expr.value > to_expr.value:
            print("Error: Range start limit {} cannot be larger than its end limit {}, line {}".
                  format(from_expr, to_expr, node.line))
            return None

        if not isinstance(from_expr, entities.Int) \
                and not isinstance(from_expr, entities.BinaryExpr):
            print("Error: Range start limit should not be a matrix, line {}"
                  .format(node.line))
            return None

        if not isinstance(to_expr, entities.Int) \
                and not isinstance(to_expr, entities.BinaryExpr)\
                and not isinstance(to_expr, int):
            print("Error: Range end limit should not be a matrix, line {}"
                  .format(node.line))
            return None

        if isinstance(from_expr, entities.BinaryExpr) \
                and from_expr.operator != "+" and from_expr.operator != "-" \
                and from_expr.operator != "*" and from_expr.operator != "/":
            print("Error: Wrong binary operation used in range expression, line {}"
                  .format(node.line))
            return None

        if isinstance(to_expr, entities.BinaryExpr) \
                and to_expr.operator != "+" and to_expr.operator != "-" \
                and to_expr.operator != "*" and to_expr.operator != "/":
            print("Error: Wrong binary operation used in range expression, line {}"
                  .format(node.line))
            return None

        return node

    def visit_ForInstruction(self, node):

        range_expression = self.visit(node.range_expression)

        if not isinstance(range_expression, entities.RangeExpression):
            print("Error: The for condition should be a range, line {}"
                  .format(node.line))
            return None

        self.table.put(str(range_expression.my_id),
                       VariableSymbol('=', range_expression.expression1))

        self.is_in_loop = True
        self.visit(node.braced_expression)
        self.is_in_loop = False

        return node

    def visit_WhileInstruction(self, node):

        self.visit(node.expression)

        self.is_in_loop = True
        self.visit(node.braced_expression)
        self.is_in_loop = False

        return node

    def visit_LoopControlInstruction(self, node):
        if not self.is_in_loop:
            print("Error: Loop Control instruction outside a loop, line {}"
                  .format(node.line))

    def visit_IfInstruction(self, node):
        expression = self.visit(node.expression)
        if isinstance(expression, entities.BinaryExpr) \
                and not (expression.operator == '=='
                         or expression.operator == '!='
                         or expression.operator == '<'
                         or expression.operator == '>'
                         or expression.operator == '<='
                         or expression.operator == '>='):
            print("Error: Invalid operation used in if instruction, line {}".format(node.line))
            return None

        self.visit(node.instructions)

        if node.else_if_instructions is not None:
            self.visit(node.else_if_instructions)

        return node
