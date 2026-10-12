"""Error reporting for the Mini Java lexer.

OWNER: Member 5 (Comments, Errors, Testing & Report).

Every scan_* helper should report a lexical error by calling
``lexer.reporter.error(message, line, col)`` so the output format stays
consistent everywhere.
"""
from __future__ import annotations


class LexerErrorReporter:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, message: str, line: int, col: int) -> None:
        """Record and print one lexical error.

        Format required by the spec:
            Error: <message> at line <line>, column <col>.

        Examples:
            Error: invalid character '@' at line 1, column 12.
            Error: invalid identifier '1name' at line 1, column 1.
            Error: unclosed string literal starting at line 1, column 15.
            Error: unclosed comment starting at line 1, column 1.

        TODO(Member 5): keep this formatting but feel free to add a
        ``filename`` and to collect errors for the report.
        """
        text = f"Error: {message} at line {line}, column {col}."
        self.errors.append(text)
        print(text)

    def has_errors(self) -> bool:
        return len(self.errors) > 0
