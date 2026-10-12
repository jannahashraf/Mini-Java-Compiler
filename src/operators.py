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

TODO(Member 4): implement this function.
"""
from __future__ import annotations


def scan_operator_or_delimiter(lexer) -> None:
    """README: see the module docstring for the rules.

    Helpers available on ``lexer``:
      lexer.current(), lexer.peek(), lexer.advance(), lexer.emit(...),
      lexer.reporter
    """
    raise NotImplementedError("Member 4: scan_operator_or_delimiter")
