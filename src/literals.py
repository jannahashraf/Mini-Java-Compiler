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

    Rules (project spec, "Literals" / "Error Handling"):
            lexer.advance()
        lexeme = lexer.source[start_pos:lexer.pos]
        lexer.reporter.error(
            f"invalid identifier '{lexeme}'", start_line, start_col
        )
        return

    lexeme = lexer.source[start_pos:lexer.pos]
    lexer.emit(TokenType.NUMBER, lexeme, start_line, start_col)
=======
    The token is emitted with ``lexer.emit(TokenType.NUMBER, lexeme,
    line, col)`` and the start line/col are remembered BEFORE consuming
    characters, so the position points at the first digit.
    """
    start_line, start_col = lexer.line, lexer.col

    # 1) Integral part: consume digits.
    chars: list[str] = []
    while lexer.current().isdigit():
        chars.append(lexer.advance())

    # 2) Fractional part: at most one '.' that must be followed by digits.
    if lexer.current() == '.':
        if lexer.peek().isdigit():
            chars.append(lexer.advance())  # the '.'
            while lexer.current().isdigit():
                chars.append(lexer.advance())
            # A second '.' can never belong to a number (e.g. 85.5.3).
            if lexer.current() == '.':
                chars.append(lexer.advance())
                while lexer.current().isdigit():
                    chars.append(lexer.advance())
                lexer.reporter.error(
                    "invalid number '" + "".join(chars) + "'",
                    start_line, start_col)
                return
        else:
            # Trailing '.' with no digits (e.g. 85.) is a lexical error.
            chars.append(lexer.advance())
            lexer.reporter.error(
                "invalid number '" + "".join(chars) + "'",
                start_line, start_col)
            return

    # 3) Letters/underscores directly after digits (1name, 20abc):
    #    invalid identifier per the spec, reported by the scanner.
    if lexer.current().isalpha() or lexer.current() == '_':
        while lexer.current().isalnum() or lexer.current() == '_':
            chars.append(lexer.advance())
        lexer.reporter.error(
            "invalid identifier '" + "".join(chars) + "'",
            start_line, start_col)
        return

    lexer.emit(TokenType.NUMBER, "".join(chars), start_line, start_col)


def scan_string(lexer) -> None:
    """Scan a STRING literal (single or double quoted) and emit it.

    Rules (project spec, "Literals" / "Error Handling"):
      - The opening quote is lexer.current(); remember the start line/col.
      - Consume until the matching closing quote (same char as the opener,
        so "A" and 'A' both work, but "A' does not close).
      - The quotes are part of the lexeme (expected output:
            Lexeme: "Ali", Token: STRING).
      - If the source ends before the closing quote is found, report:
            lexer.reporter.error(
                "unclosed string literal starting", start_line, start_col)
        and do not emit a STRING token. The reported position is where the
        opening quote was found, exactly like the spec's example:
            Error: unclosed string literal starting at line 1, column 15.
    """
    start_line, start_col = lexer.line, lexer.col
    quote = lexer.current()

    # Opening quote is consumed first and is part of the lexeme.
    lexeme: list[str] = [lexer.advance()]

    while not lexer.at_end():
        ch = lexer.advance()
        lexeme.append(ch)
        if ch == quote:
            lexer.emit(TokenType.STRING, "".join(lexeme),
                       start_line, start_col)
            return

    # Reached end of source without the closing quote.
    lexer.reporter.error(
        "unclosed string literal starting", start_line, start_col)
