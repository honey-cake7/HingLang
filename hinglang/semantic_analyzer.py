from .ast_nodes import *
from .compiler_errors import SemanticError


class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = {}

    # ----------------------------
    # ENTRY
    # ----------------------------
    def analyze(self, node):

        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.analyze(stmt)

        elif isinstance(node, DeclarationNode):
            self.handle_declaration(node)

        elif isinstance(node, AssignmentNode):
            self.handle_assignment(node)

        elif isinstance(node, PrintNode):
            self.evaluate_expr(node.expr)

        elif isinstance(node, IfNode):
            self.handle_if(node)

        elif isinstance(node, WhileNode):
            self.handle_while(node)
        elif isinstance(node, InputNode):
            self.handle_input(node)
    # ----------------------------
    # DECLARATION
    # ----------------------------
    def handle_input(self, node):
        if node.name not in self.symbol_table:
            raise SemanticError(
                f"'{node.name}' not declared before input",
                line=node.line
            )

    def handle_declaration(self, node):

        if node.name in self.symbol_table:
            raise SemanticError(
                f"'{node.name}' already declared",
                line=node.line
            )

        # declaration WITHOUT initialization
        if node.expr is None:

            self.symbol_table[node.name] = node.dtype
            return

        # declaration WITH initialization
        expr_type = self.evaluate_expr(node.expr)

        if node.dtype == "INT_DECL" and expr_type != "num":
            raise SemanticError(
                f"num variable '{node.name}' needs number",
                line=node.line
            )

        if node.dtype == "STR_DECL" and expr_type != "line":
            raise SemanticError(
                f"line variable '{node.name}' needs string",
                line=node.line
            )

        self.symbol_table[node.name] = node.dtype

    # ----------------------------
    # ASSIGNMENT
    # ----------------------------
    def handle_assignment(self, node):

        if node.name not in self.symbol_table:
            raise SemanticError(
                f"'{node.name}' not declared",
                line=node.line
            )

        expr_type = self.evaluate_expr(node.expr)

        declared_type = self.symbol_table[node.name]

        if declared_type == "INT_DECL" and expr_type != "num":
            raise SemanticError(
                f"assigning string to num '{node.name}'",
                line=node.line
            )

        if declared_type == "STR_DECL" and expr_type != "line":
            raise SemanticError(
                f"assigning number to line '{node.name}'",
                line=node.line
            )

    # ----------------------------
    # IF
    # ----------------------------
    def handle_if(self, node):

        self.evaluate_condition(node.condition)

        for stmt in node.true_block:
            self.analyze(stmt)

        for stmt in node.false_block:
            self.analyze(stmt)

    # ----------------------------
    # WHILE
    # ----------------------------
    def handle_while(self, node):

        self.evaluate_condition(node.condition)

        for stmt in node.block:
            self.analyze(stmt)

    # ----------------------------
    # CONDITION
    # ----------------------------
    def evaluate_condition(self, cond):

        left = self.evaluate_expr(cond.left)
        right = self.evaluate_expr(cond.right)

        if left != right:
            raise SemanticError("condition type mismatch", line=getattr(cond, "line", None))

    # ----------------------------
    # EXPRESSION TYPE INFERENCE
    # ----------------------------
    def evaluate_expr(self, node):

        if isinstance(node, NumberNode):
            return "num"

        if isinstance(node, StringNode):
            return "line"

        if isinstance(node, IdentifierNode):

            if node.name not in self.symbol_table:
                raise SemanticError(
                    f"'{node.name}' not declared",
                    line=node.line
                )

            return (
                "num"
                if self.symbol_table[node.name] == "INT_DECL"
                else "line"
            )

        if isinstance(node, BinOpNode):

            left = self.evaluate_expr(node.left)
            right = self.evaluate_expr(node.right)

            if left != right:
                raise SemanticError(
                    "type mismatch in expression",
                    line=node.line
                )

            if node.op in ("PLUS", "MINUS", "MUL", "DIV"):
                if left != "num":
                    raise SemanticError(
                        "arithmetic only on numbers",
                        line=node.line
                    )

            return left