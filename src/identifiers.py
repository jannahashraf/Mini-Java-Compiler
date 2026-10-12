"""Identifier and keyword scanning.

OWNER: Member 2 (Identifiers, Keywords & Symbol Table).
"""
from __future__ import annotations

from .keywords import KEYWORDS
from .tokens import TokenType


def scan_identifier_or_keyword(lexer) -> None:
    """Scan a full identifier and classify it.

    Steps:
      1. Consume the leading letter/_ and all following letters/digits/_.
         (The main loop already guarantees the first char is a letter or _.)
      2. If the lexeme is in KEYWORDS -> emit that keyword token.
         Otherwise emit IDENTIFIER and insert the token into the symbol table.

    Note: keywords include ``true``/``false`` (BOOLEAN_LITERAL) and ``main``
    (MAIN), so you get those for free by checking KEYWORDS first.

    Helpers available on ``lexer``:
      lexer.current(), lexer.peek(), lexer.advance(), lexer.emit(...),
      lexer.symbol_table, lexer.reporter

    TODO(Member 2): implement this function.
    """
    raise NotImplementedError("Member 2: scan_identifier_or_keyword")
