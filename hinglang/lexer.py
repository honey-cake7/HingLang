from .hinglang_spec import HingLangSpec
from .hing_token import Token
from .compiler_errors import LexicalError


class Lexer:

    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):

        i = 0
        line_no = 1
        text = self.text

        while i < len(text):

            ch = text[i]

            # newline
            if ch == '\n':
                line_no += 1
                i += 1
                continue

            # skip spaces
            if ch.isspace():
                i += 1
                continue

            # number
            if ch.isdigit():
                num = ch
                i += 1
                while i < len(text) and text[i].isdigit():
                    num += text[i]
                    i += 1

                self.tokens.append(Token("NUMBER", int(num), line_no))
                continue

            # identifier / keyword
            if ch.isalpha():
                word = ch
                i += 1
                while i < len(text) and text[i].isalnum():
                    word += text[i]
                    i += 1

                if word in HingLangSpec.KEYWORDS:
                    self.tokens.append(
                        Token(HingLangSpec.KEYWORDS[word], word, line_no)
                    )
                else:
                    self.tokens.append(Token("IDENTIFIER", word, line_no))

                continue

            # string
            if ch == '"':
                i += 1
                s = ""
                while i < len(text) and text[i] != '"':
                    if text[i] == "\\":
                        i += 1
                        if i >= len(text):
                            raise LexicalError("Unterminated escape sequence", line=line_no)
                        s += text[i]
                        i += 1
                        continue
                    s += text[i]
                    i += 1

                if i >= len(text):
                    raise LexicalError("Unterminated string literal", line=line_no)

                i += 1
                self.tokens.append(Token("STRING", s, line_no))
                continue

            # operators
            if ch in "+-*/":
                self.tokens.append(
                    Token(HingLangSpec.ARITHMETIC_OPERATORS[ch], ch, line_no)
                )
                i += 1
                continue

            # parentheses
            if ch == "(":
                self.tokens.append(Token("LPAREN", ch, line_no))
                i += 1
                continue

            if ch == ")":
                self.tokens.append(Token("RPAREN", ch, line_no))
                i += 1
                continue

            # relational
            if ch in "<>=":
                op = ch
                i += 1
                if i < len(text) and text[i] == "=":
                    op += "="
                    i += 1

                token_type = HingLangSpec.RELATIONAL_OPERATORS.get(op)

                if token_type:
                    self.tokens.append(Token(token_type, op, line_no))
                else:
                    self.tokens.append(Token("ASSIGN", op, line_no))

                continue

            raise LexicalError(f"Lexical Galti ho gayi '{ch}'", line=line_no)

        self.tokens.append(Token("EOF", None, line_no))
        return self.tokens