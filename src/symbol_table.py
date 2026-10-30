"""Symbol table for identifiers.

OWNER: Member 2 (Identifiers, Keywords & Symbol Table).

The symbol table records each user-defined identifier the first time it is
seen, together with where it appeared. Phase 3 (semantic analysis) will reuse
it, so keep the interface simple and clean.
"""
from __future__ import annotations

from .tokens import Token


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, Token] = {}

    def insert(self, token: Token) -> None:
        """Store an identifier token by its lexeme.

        Only the FIRST occurrence of a name is kept, so the stored token
        always points at the original definition.
        """
        if token.lexeme not in self._symbols:
            self._symbols[token.lexeme] = token

    def lookup(self, name: str) -> Token | None:
        """Return the stored token for ``name``, or None if not present."""
        return self._symbols.get(name)

    def __len__(self) -> int:
        return len(self._symbols)
