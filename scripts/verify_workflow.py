"""Run the local verification gates for the Agentic SDLC workflow."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(command: list[str]) -> int:
    """Run a verification command from the repository root and return its exit code."""
    print(f"$ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT, check=False)
    return result.returncode


def main() -> int:
    """Run tests, core coverage, dependency audit, and offline publication checks."""
    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "coverage", "run", "--source=app.budget_advisor", "-m", "pytest", "-q"],
        [sys.executable, "-m", "coverage", "report", "--fail-under=90"],
        [sys.executable, "-m", "pip_audit", "-r", "requirements-dev.txt"],
        [sys.executable, "scripts/publish_all_confluence.py", "--dry-run"],
    ]
    for command in commands:
        if run(command) != 0:
            return 1
    print("Verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
