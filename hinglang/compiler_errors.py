class CompilerError(Exception):
    def __init__(self, message, *, line=None, token=None, phase=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.token = token
        self.phase = phase

    def __str__(self):
        parts = []
        if self.phase:
            parts.append(f"{self.phase}")
        parts.append(self.message)
        if self.line is not None:
            parts.append(f"line={self.line}")
        if self.token is not None:
            parts.append(f"token={self.token}")
        return " | ".join(parts)


class LexicalError(CompilerError):
    def __init__(self, message, *, line=None, token=None):
        super().__init__(message, line=line, token=token, phase="LexicalError")


class ParseError(CompilerError):
    def __init__(self, message, *, line=None, token=None):
        super().__init__(message, line=line, token=token, phase="ParseError")


class SemanticError(CompilerError):
    def __init__(self, message, *, line=None, token=None):
        super().__init__(message, line=line, token=token, phase="SemanticError")


class RuntimeExecutionError(CompilerError):
    def __init__(self, message, *, line=None, token=None):
        super().__init__(message, line=line, token=token, phase="RuntimeExecutionError")
