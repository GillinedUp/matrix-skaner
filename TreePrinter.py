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
        res += self.string_expressions.printTree(indent)
        return res

    @addToClass(entities.Instructions)
    def printTree(self, indent=0):
        res = ""
        if issubclass(self.instructions.__class__, entities.Node):
            res += self.instructions.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.instructions) + '\n'

        res += self.instruction.printTree(indent)
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

        if issubclass(self.index.__class__, entities.Node):
            res += self.index.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.index) + '\n'

        return res

    @addToClass(entities.MatrixIndexes)
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

        if issubclass(self.left.__class__, entities.Node):
            res += self.left.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.left) + '\n'

        if issubclass(self.right.__class__, entities.Node):
            res += self.right.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.right) + '\n'

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

    @addToClass(entities.ReturnInstruction)
    def printTree(self, indent=0):
        res = indent * indent_symbol + "RETURN\n"
        res += self.expression.printTree(indent + 1)
        return res

    @addToClass(entities.StringExpressions)
    def printTree(self, indent=0):
        res = ""

        if self.string_expressions is not None:
            res += self.string_expressions.printTree(indent)

        if issubclass(self.string_expression.__class__, entities.Node):
            res += self.string_expression.printTree(indent)
        else:
            res += indent * indent_symbol + str(self.string_expression) + '\n'

        return res

    @addToClass(entities.IfInstruction)
    def printTree(self, indent=0):
        res = indent * indent_symbol + "IF\n"
        res += self.expression.printTree(indent + 1)
        res += indent * indent_symbol + "THEN\n"
        res += self.instructions.printTree(indent + 1)

        if self.else_if_instructions is not None:
            res += indent * indent_symbol + "ELSE\n"
            res += self.else_if_instructions.printTree(indent + 1)

        if self.else_instructions is not None:
            res += indent * indent_symbol + "ELSE\n"
            res += self.else_instructions.printTree(indent + 1)
        return res

    @addToClass(entities.WhileInstruction)
    def printTree(self, indent=0):
        res = indent * indent_symbol + "WHILE\n"
        res += self.expression.printTree(indent + 1)
        res += self.braced_expression.printTree(indent)
        return res

    @addToClass(entities.ForInstruction)
    def printTree(self, indent=0):
        res = indent * indent_symbol + "FOR\n"

        if issubclass(self.range_expression.__class__, entities.Node):
            self.range_expression.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.range_expression) + '\n'

        if issubclass(self.braced_expression.__class__, entities.Node):
            self.braced_expression.printTree(indent)
        else:
            res += indent_symbol * indent + str(self.braced_expression) + '\n'

        return res

    @addToClass(entities.RangeExpression)
    def printTree(self, indent=0):
        res = ""
        if self.my_id is not None:
            if issubclass(self.my_id.__class__, entities.Node):
                res = self.my_id.printTree(indent)
            else:
                res += indent_symbol * indent + str(self.my_id) + '\n'
        res += indent * indent_symbol + "RANGE\n"

        if issubclass(self.expression1.__class__, entities.Node):
            res = self.expression1.printTree(indent + 1)
        else:
            res += indent_symbol * (indent + 1) + str(self.expression1) + '\n'

        if issubclass(self.expression2.__class__, entities.Node):
            res = self.expression2.printTree(indent)
        else:
            res += indent_symbol * (indent + 1) + str(self.expression2) + '\n'
        return res

    @addToClass(entities.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body
