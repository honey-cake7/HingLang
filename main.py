import argparse

from hinglang.lexer import Lexer
from hinglang.parser import Parser
from hinglang.tac_generator import TACGenerator
from hinglang.semantic_analyzer import SemanticAnalyzer
from hinglang.tac_executor import TACExecutor
from hinglang.compiler_errors import CompilerError


def run_pipeline(file_path, phase):
    with open(file_path, encoding="utf-8") as f:
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


def build_cli_args():
    cli = argparse.ArgumentParser(description="HingLang compiler pipeline")
    cli.add_argument("--file", default="examples/demo.hing", help="Input HingLang source file")
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
        run_pipeline(args.file, args.phase)
    except CompilerError as err:
        print(f"ERROR: {err}")
        raise SystemExit(1)
    except FileNotFoundError:
        print(f"ERROR: Source file not found: {args.file}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()