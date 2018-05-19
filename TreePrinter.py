from __future__ import print_function
import entities

indent_symbol = '|  '


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(entities.Node)
    def printTree(self, indent=0):
        res = indent_symbol * indent
        res += self.instructions.printTree(indent)
        return res

    @addToClass(entities.Instructions)
    def printTree(self, indent=0):
        res = ""
        if issubclass(self.instructions.__class__, entities.Node):
            res += self.instructions.printTree(indent)
        elif issubclass(self.instructions.__class__, list):
            for el in self.instructions:
                res += indent_symbol * indent + el.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.instructions) + '\n'

        return res

    @addToClass(entities.BracedInstructions)
    def printTree(self, indent=0):
        res = indent_symbol * indent
        res += self.instructions.printTree(indent)
        return res

    @addToClass(entities.Assign)
    def printTree(self, indent=0):
        res = indent_symbol * indent + self.assign_op + '\n'
        res += self.variable.printTree(indent + 1)
        if issubclass(self.expression.__class__, entities.Node):
            res += self.expression.printTree(indent + 1)
        else:
            res += (indent_symbol * (indent + 1)) + str(self.expression) + '\n'
        return res

    @addToClass(entities.Variable)
    def printTree(self, indent=0):
        res = indent_symbol * indent + self.value + '\n'
        return res

    @addToClass(entities.ArrayRef)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'REF\n'
        if issubclass(self.matrix_name.__class__, entities.Node):
            res += self.matrix_name.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + self.matrix_name + '\n'

        res += self.index.printTree(indent + 1)

        return res

    # TODO chyba trzeba poprawić
    @addToClass(entities.MatrixExactIndexes)
    def printTree(self, indent=0):
        res = ""
        if issubclass(self.dim_index.__class__, entities.Node):
            res += self.dim_index.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.dim_index) + '\n'

        if issubclass(self.index.__class__, entities.Node):
            res += self.index.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.index) + '\n'

        return res

    @addToClass(entities.MatrixIndexes)
    def printTree(self, indent=0):
        res = ""
        if issubclass(self.index.__class__, entities.Node):
            res += self.index.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.index) + '\n'

        return res

    @addToClass(entities.UnaryExpr)
    def printTree(self, indent=0):
        res = indent_symbol * indent + self.operator + '\n'
        if issubclass(self.expr.__class__, entities.Node):
            res += self.expr.printTree(indent + 1)
        else:
            res += indent_symbol * indent + str(self.expr) + '\n'
        return res

    @addToClass(entities.BinaryExpr)
    def printTree(self, indent=0):
        res = indent_symbol * indent + self.operator + '\n'
        res += self.left.printTree(indent + 1)
        res += self.right.printTree(indent + 1)
        return res

    @addToClass(entities.ZerosMatrixInit)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'ZEROS\n'
        if issubclass(self.rows.__class__, entities.Node):
            res += self.rows.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.rows) + '\n'

        if self.columns is not None:
            if issubclass(self.columns.__class__, entities.Node):
                res += self.columns.printTree(indent + 1)
            else:
                res += indent_symbol * (indent + 1) + str(self.columns) + '\n'
        return res

    @addToClass(entities.OnesMatrixInit)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'ONES\n'
        if issubclass(self.rows.__class__, entities.Node):
            res += self.rows.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.rows) + '\n'

        if self.columns is not None:
            if issubclass(self.columns.__class__, entities.Node):
                res += self.columns.printTree(indent + 1)
            else:
                res += indent_symbol * (indent + 1) + str(self.columns) + '\n'
        return res

    @addToClass(entities.EyeMatrixInit)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'EYE\n'
        if issubclass(self.size.__class__, entities.Node):
            res += self.size.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.size) + '\n'
        return res

    @addToClass(entities.MatrixInit)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'MATRIX\n'
        if self.rows is not None:
            res += self.rows.printTree(indent + 1)

        res += self.row.printTree(indent + 1)
        return res

    @addToClass(entities.MatrixRow)
    def printTree(self, indent=0):
        res = ""
        if self.rows is not None:
            res += self.rows.printTree(indent)

        if issubclass(self.row.__class__, entities.Node):
            res += self.row.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.row) + '\n'

        return res

    @addToClass(entities.MatrixVector)
    def printTree(self, indent=0):
        res = indent_symbol * indent + 'VECTOR\n'
        if self.rows is not None:
            res += self.rows.printTree(indent)

        res += self.row.printTree(indent)
        return res


    @addToClass(entities.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body
