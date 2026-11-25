"""Diagnostics shared by all compiler phases.

OWNER: Member 5 (diagnostics and testing).

Lexical errors are recorded and printed without raising. Syntax and semantic
errors carry a source position and are raised for the CLI to report.
"""
from __future__ import annotations

import sys


class LexerErrorReporter:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, message: str, line: int, col: int) -> None:
        """Format, record, and print one lexical diagnostic to stderr."""
        text = f"Error: {message} at line {line}, column {col}."
        self.errors.append(text)
        print(text, file=sys.stderr)

    def has_errors(self) -> bool:
        return bool(self.errors)


class MiniJavaError(Exception):
    def __init__(self, message, line, column):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.message} at line {self.line}, column {self.column}"


class MiniJavaSyntaxError(MiniJavaError):
    def __str__(self):
        return f"Syntax Error: {self.message} at line {self.line}, column {self.column}"


class SemanticError(MiniJavaError):
    def __str__(self):
        return f"Semantic Error: {self.message} at line {self.line}, column {self.column}"
