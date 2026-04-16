# HingLang Compiler Design Project

HingLang is a small educational compiler project. It reads HingLang source code, checks it, turns it into intermediate code, and executes it.

## What It Does

- Lexical analysis: converts source code into tokens
- Parsing: builds an AST from the tokens
- Semantic analysis: checks declarations, types, and program rules
- TAC generation: creates three-address code
- Execution: runs the generated code and prints output
- Error handling: reports lexical, parse, semantic, and runtime errors clearly

## Requirements

- Python 3.10 or newer
- Windows PowerShell

## Install

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install .
```

If you want to work on the project and reinstall changes quickly:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

## Run The Compiler

Use the HingLang command after installation:

```powershell
& .\.venv\Scripts\hinglang.exe --file examples/demo.hing --phase run
```

You can also stop after a specific compiler stage:

```powershell
& .\.venv\Scripts\hinglang.exe --file examples/demo.hing --phase tokens
& .\.venv\Scripts\hinglang.exe --file examples/demo.hing --phase ast
& .\.venv\Scripts\hinglang.exe --file examples/demo.hing --phase tac
```

## Run Demos

The project includes sample programs in `examples/demos`.

```powershell
& .\.venv\Scripts\hinglang-demos.exe --list
& .\.venv\Scripts\hinglang-demos.exe --category success --demo all --phase run
& .\.venv\Scripts\hinglang-demos.exe --category success --demo 03_if_else.hing --phase run
& .\.venv\Scripts\hinglang-demos.exe --category failing --demo all --phase run
```

## Run Tests

Run the full test suite with HingLang:

```powershell
& .\.venv\Scripts\hinglang.exe --test
```

## Example Program

The default example file is [examples/demo.hing](examples/demo.hing).

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
& .\.venv\Scripts\hinglang.exe --file examples/demo.hing --phase run
& .\.venv\Scripts\hinglang.exe --test
```

## Team Members

124cs0081 Aniket patil
524cs0008 Lakshya Patidar
