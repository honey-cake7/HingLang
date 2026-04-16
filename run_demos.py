import argparse
from pathlib import Path
from unittest.mock import patch

from hinglang.compiler_errors import CompilerError
from main import run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent
DEMO_DIR = PROJECT_ROOT / "examples" / "demos"
FAILING_DIR = DEMO_DIR / "failing"
SCRIPTED_INPUTS = {
    "05_input_output.hing": ["Aniket"],
}


def get_demo_files(category):
    if category == "success":
        if not DEMO_DIR.exists():
            return []
        # Keep top-level demos as successful feature walkthrough demos.
        return sorted(DEMO_DIR.glob("*.hing"))

    if category == "failing":
        if not FAILING_DIR.exists():
            return []
        return sorted(FAILING_DIR.glob("*.hing"))

    # category == "all"
    demos = []
    if DEMO_DIR.exists():
        demos.extend(sorted(DEMO_DIR.glob("*.hing")))
    if FAILING_DIR.exists():
        demos.extend(sorted(FAILING_DIR.glob("*.hing")))
    return demos


def run_single_demo(file_path, phase, interactive_input):
    print(f"\n===== Running {file_path.name} =====")

    if phase == "run" and not interactive_input and file_path.name in SCRIPTED_INPUTS:
        with patch("builtins.input", side_effect=SCRIPTED_INPUTS[file_path.name]):
            run_pipeline(str(file_path), phase)
    else:
        run_pipeline(str(file_path), phase)


def parse_args():
    cli = argparse.ArgumentParser(description="Run HingLang feature demos")
    cli.add_argument(
        "--category",
        choices=["success", "failing", "all"],
        default="success",
        help="Which demo set to run"
    )
    cli.add_argument(
        "--demo",
        default="all",
        help="Demo filename (e.g. 03_if_else.hing) or 'all'"
    )
    cli.add_argument(
        "--phase",
        choices=["tokens", "ast", "tac", "run"],
        default="run",
        help="Stop at a specific phase"
    )
    cli.add_argument(
        "--list",
        action="store_true",
        help="List available demos"
    )
    cli.add_argument(
        "--interactive-input",
        action="store_true",
        help="Use interactive input instead of scripted values"
    )
    return cli.parse_args()


def main():
    args = parse_args()
    demos = get_demo_files(args.category)

    if not demos:
        print(f"No demo files found for category: {args.category}")
        raise SystemExit(1)

    if args.list:
        print(f"Available demos ({args.category}):")
        for demo in demos:
            print(f"- {demo.name}")
        return

    failures = []

    if args.demo == "all":
        selected = demos
    else:
        selected = [d for d in demos if d.name == args.demo]
        if not selected:
            print(f"Demo not found: {args.demo}")
            print("Use --list to see available demos.")
            raise SystemExit(1)

    for demo in selected:
        try:
            run_single_demo(demo, args.phase, args.interactive_input)
        except CompilerError as err:
            print(f"ERROR in {demo.name}: {err}")
            failures.append(demo.name)
        except FileNotFoundError:
            print(f"ERROR: file not found: {demo}")
            failures.append(demo.name)

    if failures:
        print("\nCompleted with failures:")
        for name in failures:
            print(f"- {name}")
        raise SystemExit(1)

    print("\nAll selected demos executed successfully.")


if __name__ == "__main__":
    main()
