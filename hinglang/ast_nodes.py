class ProgramNode:
    def __init__(self, statements, line=None):
        self.statements = statements
        self.line = line


class DeclarationNode:
    def __init__(self, dtype, name, expr, line=None):
        self.dtype = dtype
        self.name = name
        self.expr = expr
        self.line = line


class AssignmentNode:
    def __init__(self, name, expr, line=None):
        self.name = name
        self.expr = expr
        self.line = line


class PrintNode:
    def __init__(self, expr, line=None):
        self.expr = expr
        self.line = line


class BinOpNode:
    def __init__(self, left, op, right, line=None):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class NumberNode:
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class StringNode:
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class IdentifierNode:
    def __init__(self, name, line=None):
        self.name = name
        self.line = line

class IfNode:
    def __init__(self, condition, true_block, false_block, line=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
        self.line = line


class WhileNode:
    def __init__(self, condition, block, line=None):
        self.condition = condition
        self.block = block
        self.line = line


class ConditionNode:
    def __init__(self, left, op, right, line=None):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class InputNode:
    def __init__(self, name, line=None):
        self.name = name
        self.line = line