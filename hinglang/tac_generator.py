from .ast_nodes import *


class TACGenerator:

    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    # ----------------------------
    # Entry point
    # ----------------------------
    def generate(self, node):

        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.generate(stmt)

        elif isinstance(node, DeclarationNode):
            if node.expr is not None:
                value = self.generate_expr(node.expr)
                self.code.append(f"{node.name} = {value}")

        elif isinstance(node, AssignmentNode):
            value = self.generate_expr(node.expr)
            self.code.append(f"{node.name} = {value}")

        elif isinstance(node, PrintNode):
            value = self.generate_expr(node.expr)
            self.code.append(f"print {value}")

        elif isinstance(node, IfNode):
            self.generate_if(node)

        elif isinstance(node, WhileNode):
            self.generate_while(node)
        elif isinstance(node, InputNode):
            self.code.append(f"input {node.name}")

        return self.code

    # ----------------------------
    # Expression TAC
    # ----------------------------
    def generate_expr(self, node):

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return f'"{node.value}"'

        if isinstance(node, IdentifierNode):
            return node.name

        if isinstance(node, BinOpNode):
            left = self.generate_expr(node.left)
            right = self.generate_expr(node.right)

            temp = self.new_temp()
            op = self.map_op(node.op)

            self.code.append(f"{temp} = {left} {op} {right}")

            return temp

    # ----------------------------
    # Condition TAC
    # ----------------------------
    def generate_condition(self, cond):

        left = self.generate_expr(cond.left)
        right = self.generate_expr(cond.right)
        op = self.map_op(cond.op)

        return f"{left} {op} {right}"

    # ----------------------------
    # IF TAC
    # ----------------------------
    def generate_if(self, node):

        label_else = self.new_label()
        label_end = self.new_label()

        cond = self.generate_condition(node.condition)

        self.code.append(f"ifFalse {cond} goto {label_else}")

        for stmt in node.true_block:
            self.generate(stmt)

        self.code.append(f"goto {label_end}")

        self.code.append(f"{label_else}:")

        for stmt in node.false_block:
            self.generate(stmt)

        self.code.append(f"{label_end}:")

    # ----------------------------
    # WHILE TAC
    # ----------------------------
    def generate_while(self, node):

        label_start = self.new_label()
        label_end = self.new_label()

        self.code.append(f"{label_start}:")

        cond = self.generate_condition(node.condition)

        self.code.append(f"ifFalse {cond} goto {label_end}")

        for stmt in node.block:
            self.generate(stmt)

        self.code.append(f"goto {label_start}")
        self.code.append(f"{label_end}:")

    # ----------------------------
    # Helpers
    # ----------------------------
    def new_label(self):
        self.temp_count += 1
        return f"L{self.temp_count}"

    def map_op(self, op):

        mapping = {
            "PLUS": "+",
            "MINUS": "-",
            "MUL": "*",
            "DIV": "/",
            "LT": "<",
            "GT": ">",
            "LE": "<=",
            "GE": ">=",
            "EQ": "=="
        }

        return mapping[op]