# HingLang Compiler Design Project

A mini educational compiler pipeline for HingLang, covering lexical analysis, parsing, semantic checks, three-address code generation, and execution.

## Features

- Custom HingLang lexer with keyword/operator support
- Recursive-descent parser that builds an AST
- Semantic analyzer with type and declaration checks
- TAC (three-address code) generator for intermediate representation
- TAC executor for running compiled output
- Structured compiler errors by phase:
  - `LexicalError`
  - `ParseError`
  - `SemanticError`
  - `RuntimeExecutionError`
- Unit tests for happy-path and failure scenarios

## Project Structure

```text
.
|-- examples/
|   |-- demo.hing
|   `-- demos/
|       |-- 01_basics.hing
|       |-- 02_arithmetic.hing
|       |-- 03_if_else.hing
|       |-- 04_while_loop.hing
|       |-- 05_input_output.hing
|       |-- 06_nested_control.hing
|       `-- failing/
|           |-- 91_fail_lexical_invalid_char.hing
|           |-- 92_fail_parse_unterminated_if.hing
|           |-- 93_fail_semantic_undeclared_variable.hing
|           `-- 94_fail_runtime_division_by_zero.hing
|-- hinglang/
|   |-- __init__.py
|   |-- ast_nodes.py
|   |-- compiler_errors.py
|   |-- hing_token.py
|   |-- hinglang_spec.py
|   |-- lexer.py
|   |-- parser.py
|   |-- semantic_analyzer.py
|   |-- tac_executor.py
|   `-- tac_generator.py
|-- main.py
|-- run_demos.py
|-- tests/
|   `-- test_compiler_pipeline.py
|-- .gitignore
`-- README.md
```

## Requirements

- Python 3.10+ (tested with Python 3.13)

## Quick Start

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Run the compiler on the demo program.

```powershell
python main.py --file examples/demo.hing --phase run
```

## Install

To let your professor install and run the project with `pip`, use this flow from the repository root:

```powershell
python -m venv .venv
python -m pip install --upgrade pip
pip install .
```

After installation, the CLI commands are:

```powershell
hinglang --file examples/demo.hing --phase run
hinglang-demos --category success --demo all --phase run
```

If your professor wants to run it in editable mode during review, this also works:

```powershell
pip install -e .
```

## Compiler Phases (CLI)

Use the `--phase` flag to stop at any phase for debugging or learning:

```powershell
# Show tokens
python main.py --file examples/demo.hing --phase tokens

# Parse and validate AST structure
python main.py --file examples/demo.hing --phase ast

# Generate and print TAC
python main.py --file examples/demo.hing --phase tac

# Full pipeline and execute
python main.py --file examples/demo.hing --phase run
```

## Run Feature Demos With One File

You can run all feature demos from one Python file:

```powershell
python run_demos.py --category success --demo all --phase run
```

List all available demo files:

```powershell
python run_demos.py --category success --list
```

Run one specific demo:

```powershell
python run_demos.py --category success --demo 03_if_else.hing --phase run
```

The input demo (`05_input_output.hing`) uses scripted input by default when running through `run_demos.py`.
To enter input manually, use:

```powershell
python run_demos.py --category success --demo 05_input_output.hing --interactive-input
```

Run intentionally failing demos:

```powershell
python run_demos.py --category failing --demo all --phase run
```

Run both success and failing demos in one go:

```powershell
python run_demos.py --category all --demo all --phase run
```

## Running Tests

```powershell
python -m unittest discover -s tests -v
```

### Test Usage

Run all tests:

```powershell
python -m unittest discover -s tests -v
```

Run a single test file:

```powershell
python -m unittest tests.test_compiler_pipeline -v
```

Run one specific test method:

```powershell
python -m unittest tests.test_compiler_pipeline.CompilerPipelineTests.test_happy_path_execution -v
```

Expected result when everything passes:

- Tests print lines ending with `ok`
- Summary shows `Ran 6 tests`
- Final line shows `OK`

If virtual environment activation is blocked in PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Current test coverage includes:

- valid end-to-end execution
- unterminated string lexical failure
- undeclared variable semantic failure
- type mismatch semantic failure
- divide-by-zero runtime failure
- malformed control-flow parse failure

## HingLang Example

```hing
shuru
line a
bol "Line bata"
sun a
bol "Aapka Line hai"
bol a
khatam
```
## Team Members
124cs0081 Aniket patil
524cs0008 Lakshya Patidar