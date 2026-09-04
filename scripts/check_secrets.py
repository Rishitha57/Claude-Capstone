"""Scan staged Git changes for common credential patterns."""

from __future__ import annotations

import re
import subprocess
import sys


SECRET_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,}|"
    r"password\s*=\s*['\"][^'\"]+['\"]|"
    r"api[_-]?token\s*[:=]\s*['\"][^'\"]+['\"])",
    re.IGNORECASE,
)


def main() -> int:
    """Return a failure code when staged changes contain likely secrets."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--no-ext-diff", "--unified=0"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Secret scan could not read staged changes: {result.stderr.strip()}", file=sys.stderr)
        return 1
    matches = SECRET_PATTERN.findall(result.stdout)
    if matches:
        print("ERROR: Potential secret detected in staged changes!", file=sys.stderr)
        return 1
    print("Secret check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
