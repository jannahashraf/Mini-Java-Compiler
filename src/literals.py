"""Numeric and string literal scanning.

OWNER: Member 3 (Literals).

Literals in Mini Java:
  NUMBER  -> any integer or floating-point value (10, 0, 25.5)
  STRING  -> any value enclosed in single or double quotes ("Hello", 'A')
  BOOLEAN -> handled as BOOLEAN_LITERAL by the keyword table (Member 2)
"""
from __future__ import annotations

from .tokens import TokenType


def scan_number(lexer) -> None:
    """Scan a NUMBER literal and emit it.

    Rules:
      - Consume digits.
      - Allow at most ONE '.' to make it a float (e.g. 85.5 -> NUMBER).
      - A second '.' or a trailing '.' with no digits is a lexical error.

    Use ``lexer.emit(TokenType.NUMBER, lexeme, line, col)`` and remember the
    start line/col BEFORE consuming characters.

    TODO(Member 3): implement this function.
    """
    raise NotImplementedError("Member 3: scan_number")


def scan_string(lexer) -> None:
    """Scan a STRING literal (single or double quoted) and emit it.

    Rules:
      - The opening quote is lexer.current(); remember the start line/col.
      - Consume until the matching quote.
      - If the source ends first, report an error:
            lexer.reporter.error(
                "unclosed string literal starting", start_line, start_col)
        and do not emit a STRING token.

    TODO(Member 3): implement this function.
    """
    raise NotImplementedError("Member 3: scan_string")
