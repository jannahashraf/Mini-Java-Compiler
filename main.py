"""Command-line entry point for the Mini Java lexer.

OWNER: Member 1 (Core & Integration).

Usage:
    python3 main.py tests/sample1.mj
"""
from __future__ import annotations

import sys

from src.scanner import Lexer


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 main.py <source-file>")
        return 2

    with open(argv[1], "r", encoding="utf-8") as handle:
        source = handle.read()

    lexer = Lexer(source)
    for token in lexer.scan_tokens():
        print(token)

    return 1 if lexer.reporter.has_errors() else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
