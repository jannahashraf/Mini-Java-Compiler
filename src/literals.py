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

    """
    start_pos = lexer.pos
    start_line = lexer.line
    start_col = lexer.col

    while lexer.current().isdigit():
        lexer.advance()

    if lexer.current() == ".":
        lexer.advance()
        digits_after_decimal = 0
        while lexer.current().isdigit():
            lexer.advance()
            digits_after_decimal += 1

        if digits_after_decimal == 0:
            lexeme = lexer.source[start_pos:lexer.pos]
            lexer.reporter.error(
                f"invalid number literal '{lexeme}'", start_line, start_col
            )
            return

    if lexer.current() == ".":
        while lexer.current().isdigit() or lexer.current() == ".":
            lexer.advance()
        lexeme = lexer.source[start_pos:lexer.pos]
        lexer.reporter.error(
            f"invalid number literal '{lexeme}'", start_line, start_col
        )
        return

    if lexer.current().isalpha() or lexer.current() == "_":
        while lexer.current().isalnum() or lexer.current() == "_":
            lexer.advance()
        lexeme = lexer.source[start_pos:lexer.pos]
        lexer.reporter.error(
            f"invalid identifier '{lexeme}'", start_line, start_col
        )
        return

    lexeme = lexer.source[start_pos:lexer.pos]
    lexer.emit(TokenType.NUMBER, lexeme, start_line, start_col)


def scan_string(lexer) -> None:
    """Scan a STRING literal (single or double quoted) and emit it.

    Rules:
      - The opening quote is lexer.current(); remember the start line/col.
      - Consume until the matching quote.
      - If the source ends first, report an error:
            lexer.reporter.error(
                "unclosed string literal starting", start_line, start_col)
        and do not emit a STRING token.

    """
    start_pos = lexer.pos
    start_line = lexer.line
    start_col = lexer.col
    quote = lexer.current()
    lexer.advance()

    while not lexer.at_end() and lexer.current() != quote:
        lexer.advance()

    if lexer.at_end():
        lexer.reporter.error(
            "unclosed string literal starting", start_line, start_col
        )
        return

    lexer.advance()
    lexeme = lexer.source[start_pos:lexer.pos]
    lexer.emit(TokenType.STRING, lexeme, start_line, start_col)
