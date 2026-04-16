import argparse
import unittest
from pathlib import Path

from hinglang.lexer import Lexer
from hinglang.parser import Parser
from hinglang.tac_generator import TACGenerator
from hinglang.semantic_analyzer import SemanticAnalyzer
from hinglang.tac_executor import TACExecutor
from hinglang.compiler_errors import CompilerError


def resolve_source_file(file_path):
    candidate = Path(file_path)
    if candidate.is_file():
        return candidate

    project_root = Path(__file__).resolve().parent
    fallback = project_root / file_path
    if fallback.is_file():
        return fallback

    return candidate


def run_pipeline(file_path, phase):
    source_path = resolve_source_file(file_path)

    with open(source_path, encoding="utf-8") as f:
        text = f.read()

    tokens = Lexer(text).tokenize()

    if phase == "tokens":
        print("TOKENS:")
        for tok in tokens:
            print(tok)
        return

    parser = Parser(tokens)
    ast = parser.parse_program()

    print("Parsing Successful")

    if phase == "ast":
        print("AST parsed successfully. Phase stopped at AST.")
        return

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(ast)

    tac = TACGenerator().generate(ast)

    if phase == "tac":
        print("TAC:")
        for line in tac:
            print(line)
        return

    executor = TACExecutor(tac)
    print("\nPROGRAM OUTPUT:\n")
    executor.execute()


def run_tests():
    project_root = Path(__file__).resolve().parent
    tests_dir = project_root / "tests"

    if not tests_dir.exists():
        print("ERROR: tests directory not found")
        raise SystemExit(1)

    loader = unittest.defaultTestLoader
    suite = loader.discover(str(tests_dir), pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


def build_cli_args():
    cli = argparse.ArgumentParser(description="HingLang compiler pipeline")
    cli.add_argument("--file", default="examples/demo.hing", help="Input HingLang source file")
    cli.add_argument(
        "--test",
        action="store_true",
        help="Run the HingLang test suite"
    )
    cli.add_argument(
        "--phase",
        choices=["tokens", "ast", "tac", "run"],
        default="run",
        help="Stop after a specific phase or execute full pipeline"
    )
    return cli.parse_args()


def main():
    args = build_cli_args()
    try:
        if args.test:
            run_tests()
        run_pipeline(args.file, args.phase)
    except CompilerError as err:
        print(f"ERROR: {err}")
        raise SystemExit(1)
    except FileNotFoundError:
        print(f"ERROR: Source file not found: {args.file}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()