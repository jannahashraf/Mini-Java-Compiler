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
    """
    line, col = lexer.line, lexer.col

    chars: list[str] = []
    while True:
        ch = lexer.current()
        if not (ch.isalnum() or ch == "_"):
            break
        chars.append(lexer.advance())

    lexeme = "".join(chars)
    token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
    token = lexer.emit(token_type, lexeme, line, col)

    # Only user-defined names belong in the symbol table; keywords,
    # ``main`` and ``true``/``false`` are not identifiers.
    if token_type is TokenType.IDENTIFIER:
        lexer.symbol_table.insert(token)
