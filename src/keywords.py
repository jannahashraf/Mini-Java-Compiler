"""Keyword table for Mini Java.

OWNER: Member 2 (Identifiers, Keywords & Symbol Table).

Mini Java is case-sensitive, so the lookup must be exact ("class" is a
keyword, "Class" is an IDENTIFIER).

Note: ``true`` / ``false`` are BOOLEAN_LITERAL, not keywords. And ``main`` is
its own token MAIN (see the spec sample output).
"""
from __future__ import annotations

from .tokens import TokenType


KEYWORDS: dict[str, TokenType] = {
    "class": TokenType.CLASS,
    "public": TokenType.PUBLIC,
    "static": TokenType.STATIC,
    "void": TokenType.VOID,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "boolean": TokenType.BOOLEAN,
    "char": TokenType.CHAR,
    "String": TokenType.STRING_TYPE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
    "main": TokenType.MAIN,
    "true": TokenType.BOOLEAN_LITERAL,
    "false": TokenType.BOOLEAN_LITERAL,
}

# Reviewed against the Phase 1 spec: every reserved word is present.
# ``main`` and ``true``/``false`` are extras required by the shared token
# contract (MAIN and BOOLEAN_LITERAL respectively).
