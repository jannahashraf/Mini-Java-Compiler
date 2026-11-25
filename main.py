"""Command-line entry point for the Mini Java compiler."""
from __future__ import annotations

import sys

from compiler.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
