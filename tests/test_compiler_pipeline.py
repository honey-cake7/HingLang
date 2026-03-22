import io
import unittest
from unittest.mock import patch

from hinglang.compiler_errors import LexicalError, ParseError, SemanticError, RuntimeExecutionError
from hinglang.lexer import Lexer
from hinglang.parser import Parser
from hinglang.semantic_analyzer import SemanticAnalyzer
from hinglang.tac_generator import TACGenerator
from hinglang.tac_executor import TACExecutor


class CompilerPipelineTests(unittest.TestCase):

    def compile_program(self, source):
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse_program()
        SemanticAnalyzer().analyze(ast)
        tac = TACGenerator().generate(ast)
        return tokens, ast, tac

    def run_program(self, source, inputs=None):
        _, _, tac = self.compile_program(source)
        executor = TACExecutor(tac)

        with patch("builtins.input", side_effect=inputs or []), patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            executor.execute()
            return fake_out.getvalue().strip().splitlines() if fake_out.getvalue().strip() else []

    def test_happy_path_execution(self):
        src = """
shuru
num a = 2
num b = 3
num c = a + b
bol c
khatam
"""
        output = self.run_program(src)
        self.assertEqual(output, ["5"])

    def test_unterminated_string_raises_lexical_error(self):
        src = """
shuru
line a = "hello
khatam
"""
        with self.assertRaises(LexicalError):
            Lexer(src).tokenize()

    def test_undeclared_variable_raises_semantic_error(self):
        src = """
shuru
a = 5
khatam
"""
        with self.assertRaises(SemanticError):
            self.compile_program(src)

    def test_type_mismatch_raises_semantic_error(self):
        src = """
shuru
num a = 1
a = "x"
khatam
"""
        with self.assertRaises(SemanticError):
            self.compile_program(src)

    def test_divide_by_zero_raises_runtime_error(self):
        src = """
shuru
num a = 10
num b = 0
num c = a / b
bol c
khatam
"""
        with self.assertRaises(RuntimeExecutionError):
            self.run_program(src)

    def test_malformed_control_flow_raises_parse_error(self):
        src = """
shuru
num a = 1
jabtak a < 3
a = a + 1
"""
        with self.assertRaises(ParseError):
            tokens = Lexer(src).tokenize()
            Parser(tokens).parse_program()


if __name__ == "__main__":
    unittest.main()
