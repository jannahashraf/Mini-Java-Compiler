"""Operator and delimiter scanning.

OWNER: Member 4 (Operators & Delimiters).

Use LONGEST MATCH: check two-character operators before one-character ones
(e.g. >= before >, == before =, <= before <, != before !).

Token grouping (matches the spec sample output):
  '='                 -> ASSIGN
  arithmetic  + - * / %   -> MATHOP
  comparison / logical    -> LOGOP   (e.g. >=, ==, !=, <, >, <=)

Delimiters (one character each):
  LPAR (   RPAR )   LCUR {   RCUR }   LSQU [   RSQU ]
  SEMICOLON ;   COMMA ,   DOT .

Anything not matched is an error:
  lexer.reporter.error(f"invalid character '{ch}'", line, col)
"""
from __future__ import annotations

from .tokens import TokenType

TWO_CHAR_OPERATORS = {
    ">=": TokenType.LOGOP,
    "<=": TokenType.LOGOP,
    "==": TokenType.LOGOP,
    "!=": TokenType.LOGOP,
}

ONE_CHAR_OPERATORS = {
    "=": TokenType.ASSIGN,
    "+": TokenType.MATHOP,
    "-": TokenType.MATHOP,
    "*": TokenType.MATHOP,
    "/": TokenType.MATHOP,
    "%": TokenType.MATHOP,
    ">": TokenType.LOGOP,
    "<": TokenType.LOGOP,
    "!": TokenType.LOGOP,
}

DELIMITERS = {
    "(": TokenType.LPAR,
    ")": TokenType.RPAR,
    "{": TokenType.LCUR,
    "}": TokenType.RCUR,
    "[": TokenType.LSQU,
    "]": TokenType.RSQU,
    ";": TokenType.SEMICOLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
}


def scan_operator_or_delimiter(lexer) -> None:
    """Scan one operator or delimiter, using longest match.

    Helpers available on ``lexer``:
      lexer.current(), lexer.peek(), lexer.advance(), lexer.emit(...),
      lexer.reporter
    """
    line, col = lexer.line, lexer.col
    ch = lexer.current()
    two = ch + lexer.peek()

    if two in TWO_CHAR_OPERATORS:
        lexer.advance()
        lexer.advance()
        lexer.emit(TWO_CHAR_OPERATORS[two], two, line, col)
        return

    if ch in ONE_CHAR_OPERATORS:
        lexer.advance()
        lexer.emit(ONE_CHAR_OPERATORS[ch], ch, line, col)
        return

    if ch in DELIMITERS:
        lexer.advance()
        lexer.emit(DELIMITERS[ch], ch, line, col)
        return

    lexer.advance()
    lexer.reporter.error(f"invalid character '{ch}'", line, col)
