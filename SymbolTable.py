#!/usr/bin/python


class VariableSymbol:
    def __init__(self, var_type, value):
        self.type = var_type
        self.value = value


class MatrixSymbol:
    def __init__(self, m_type, value, columns, rows):
        self.value = value
        self.type = m_type
        self.columns = columns
        self.rows = rows


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.entries[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        try:
            symbol = self.entries[name]
            return symbol
        except:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        pass

    def popScope(self):
        pass
