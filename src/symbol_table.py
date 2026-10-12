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

        TODO(Member 2): insert only the FIRST occurrence of a name
        (do not overwrite the original definition).
        """
        raise NotImplementedError("Member 2: implement SymbolTable.insert")

    def lookup(self, name: str) -> Token | None:
        """Return the stored token for ``name``, or None if not present.

        TODO(Member 2): implement the lookup.
        """
        raise NotImplementedError("Member 2: implement SymbolTable.lookup")

    def __len__(self) -> int:
        return len(self._symbols)
