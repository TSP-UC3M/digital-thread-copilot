"""Single entry command of the development tasks. Works on Windows and Linux.

    python scripts/dev.py all          install, then lint and all tests (fresh clone)
    python scripts/dev.py install      install the pinned tools and the package
    python scripts/dev.py lint         static checks and formatting check
    python scripts/dev.py unit         unit tests with the coverage threshold
    python scripts/dev.py functional   functional tests
    python scripts/dev.py check        lint, unit and functional tests

Run it from the repository root, inside the virtual environment.
"""

import subprocess
import sys

PYTHON = [sys.executable, "-m"]

TASKS = {
    "install": [
        [*PYTHON, "pip", "install", "-r", "requirements-dev.txt"],
        [*PYTHON, "pip", "install", "--no-deps", "-e", "."],
    ],
    "lint": [
        [*PYTHON, "ruff", "check", "src", "tests", "scripts"],
        [*PYTHON, "ruff", "format", "--check", "src", "tests", "scripts/dev.py"],
    ],
    "unit": [
        [*PYTHON, "pytest", "tests/unit", "--cov", "--cov-report=term-missing", "--cov-report=xml"],
    ],
    "functional": [
        [*PYTHON, "pytest", "tests/functional", "-m", "functional"],
    ],
}
TASKS["check"] = [*TASKS["lint"], *TASKS["unit"], *TASKS["functional"]]
TASKS["all"] = [*TASKS["install"], *TASKS["check"]]


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in TASKS:
        print(__doc__)
        return 2
    for command in TASKS[argv[0]]:
        print("+ " + " ".join(command[2:]), flush=True)
        code = subprocess.run(command, check=False).returncode
        if code != 0:
            print(f"FAILED ({code}): {' '.join(command[2:])}")
            return code
    print(f"OK: {argv[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
