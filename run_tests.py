import argparse
import unittest
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run HingLang tests")
    parser.parse_args()

    tests_dir = Path(__file__).resolve().parent / "tests"
    if not tests_dir.exists():
        print("No tests directory found.")
        raise SystemExit(1)

    loader = unittest.defaultTestLoader
    suite = loader.discover(str(tests_dir), pattern="test*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()