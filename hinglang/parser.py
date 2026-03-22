from .ast_nodes import *
from .hing_token import Token
from .compiler_errors import ParseError


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else Token("EOF", None, 1)

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current.type == token_type:
            self.advance()
        else:
            raise ParseError(
                f"Expected {token_type} but got {self.current.type}",
                line=self.current.line,
                token=self.current
            )

    # -----------------------------------
    # program → START stmt_list END
    # -----------------------------------
    def parse_program(self):
        if self.current.type != "START":
            raise ParseError("Program must start with 'shuru'", line=self.current.line, token=self.current)

        self.eat("START")

        statements = []

        while self.current.type not in ("END", "EOF"):
            stmt = self.parse_statement()
            statements.append(stmt)

        if self.current.type == "EOF":
            raise ParseError("Program ended before 'khatam'", line=self.current.line, token=self.current)

        self.eat("END")

        if self.current.type != "EOF":
            raise ParseError("Unexpected tokens after program end", line=self.current.line, token=self.current)

        return ProgramNode(statements)

    # -----------------------------------
    # statement dispatcher
    # -----------------------------------
    def parse_statement(self):

        if self.current.type in ("INT_DECL", "STR_DECL"):
            return self.parse_declaration()

        elif self.current.type == "IDENTIFIER":
            return self.parse_assignment()

        elif self.current.type == "PRINT":
            return self.parse_print()

        elif self.current.type == "INPUT":
            return self.parse_input()

        elif self.current.type == "IF":
            return self.parse_if()

        elif self.current.type == "WHILE":
            return self.parse_while()

        else:
            raise ParseError(
                f"Unexpected token {self.current.type}",
                line=self.current.line,
                token=self.current
            )

    def parse_declaration(self):
        line = self.current.line

        dtype = self.current.type
        self.advance()

        name = self.current.value
        self.eat("IDENTIFIER")

        # optional initialization
        if self.current.type == "ASSIGN":

            self.eat("ASSIGN")
            expr = self.parse_expression()

        else:
            expr = None

        return DeclarationNode(dtype, name, expr, line=line)

    # -----------------------------------
    # assignment → ID = expr
    # -----------------------------------
    def parse_assignment(self):
        line = self.current.line

        name = self.current.value
        self.eat("IDENTIFIER")

        self.eat("ASSIGN")

        expr = self.parse_expression()

        return AssignmentNode(name, expr, line=line)

    # -----------------------------------
    # print → bol expr
    # -----------------------------------
    def parse_print(self):
        line = self.current.line

        self.eat("PRINT")

        expr = self.parse_expression()

        return PrintNode(expr, line=line)

   
    def parse_condition(self):
        line = self.current.line

        left = self.parse_expression()

        if self.current.type in ("LT", "GT", "LE", "GE", "EQ"):
            op = self.current.type
            self.advance()
        else:
            raise ParseError("Relational operator expected", line=self.current.line, token=self.current)

        right = self.parse_expression()

        return ConditionNode(left, op, right, line=line)
    
    # -----------------------------------
    # expression → term ((+ | -) term)*
    # -----------------------------------
    def parse_expression(self):

        node = self.parse_term()

        while self.current.type in ("PLUS", "MINUS"):
            op = self.current.type
            self.advance()

            right = self.parse_term()

            node = BinOpNode(node, op, right, line=getattr(node, "line", None))

        return node

    # -----------------------------------
    # term → factor ((* | /) factor)*
    # -----------------------------------
    def parse_term(self):

        node = self.parse_factor()

        while self.current.type in ("MUL", "DIV"):
            op = self.current.type
            self.advance()

            right = self.parse_factor()

            node = BinOpNode(node, op, right, line=getattr(node, "line", None))

        return node

    # -----------------------------------
    # factor → NUMBER | STRING | ID
    # -----------------------------------
    def parse_factor(self):

        token = self.current

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(token.value, line=token.line)

        elif token.type == "STRING":
            self.advance()
            return StringNode(token.value, line=token.line)

        elif token.type == "IDENTIFIER":
            self.advance()
            return IdentifierNode(token.value, line=token.line)
        elif self.current.type == "INPUT":
            return self.parse_input()

        elif token.type == "LPAREN":

            self.eat("LPAREN")

            node = self.parse_expression()

            self.eat("RPAREN")

            return node

        else:
            raise ParseError(
                f"Invalid expression near token {token.type}",
                line=token.line,
                token=token
            )

    def parse_if(self):
        line = self.current.line
        self.eat("IF")
        condition = self.parse_condition()
        true_block = []

        while self.current.type not in ("ELSE", "END", "EOF"):
            stmt = self.parse_statement()
            true_block.append(stmt)

        if self.current.type == "EOF":
            raise ParseError("Unterminated agar block", line=self.current.line, token=self.current)

        false_block = []

        if self.current.type == "ELSE":
            self.eat("ELSE")

            while self.current.type not in ("END", "EOF"):
                stmt = self.parse_statement()
                false_block.append(stmt)

            if self.current.type == "EOF":
                raise ParseError("Unterminated warna block", line=self.current.line, token=self.current)

        self.eat("END")

        return IfNode(condition, true_block, false_block, line=line)

    def parse_input(self):
        line = self.current.line

        self.eat("INPUT")

        name = self.current.value
        self.eat("IDENTIFIER")

        return InputNode(name, line=line)
    
    def parse_while(self):
        line = self.current.line

        self.eat("WHILE")

        condition = self.parse_condition()

        block = []

        while self.current.type not in ("END", "EOF"):
            stmt = self.parse_statement()
            block.append(stmt)

        if self.current.type == "EOF":
            raise ParseError("Unterminated jabtak block", line=self.current.line, token=self.current)

        self.eat("END")

        return WhileNode(condition, block, line=line)