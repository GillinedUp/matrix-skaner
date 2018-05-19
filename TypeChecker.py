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

    # simpler version of generic_visit, not so general
    def generic_visit(self, node):
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
        variable = self.table.get(node.variable)
        assign_op = self.visit(node.assign_op)
        assigments = self.visit(node.expression)

        if assigments is not None:
            if isinstance(node.expression, entities.ZerosMatrixInit) \
                    or isinstance(node.expression, entities.OnesMatrixInit) \
                    or isinstance(node.expression, entities.EyeMatrixInit):
                self.table.put(str(node.variable),
                               MatrixSymbol(node.assign_op, node.expression, node.expression.columns,
                                            node.expression.rows))
            elif isinstance(assigments, entities.MatrixVector):
                self.table.put(str(node.variable), MatrixSymbol(node.assign_op, node.expression, self.columns, self.elements / self.columns))
            else:
                self.table.put(str(node.variable), VariableSymbol(node.assign_op, node.expression))

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
        return self.visit((self.table.get(node.variable)).variable)
