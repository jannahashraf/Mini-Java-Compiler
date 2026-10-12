"""Shared token definitions for the Mini Java lexer.

OWNER: Member 1 (Core & Integration).

This file is the contract between every module. Do NOT rename or remove a
token without telling the whole team, because every scan_* helper depends on it.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # ---- keywords (Member 2) ----
    CLASS = auto()
    PUBLIC = auto()
    STATIC = auto()
    VOID = auto()
    INT = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    CHAR = auto()
    STRING_TYPE = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    MAIN = auto()

    # ---- identifiers & literals (Members 2 & 3) ----
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN_LITERAL = auto()  # true / false

    # ---- operators (Member 4) ----
    ASSIGN = auto()  # =
    MATHOP = auto()  # + - * / % ...
    LOGOP = auto()   # > < >= <= == != ...

    # ---- delimiters (Member 4) ----
    LPAR = auto()      # (
    RPAR = auto()      # )
    LCUR = auto()      # {
    RCUR = auto()      # }
    LSQU = auto()      # [
    RSQU = auto()      # ]
    SEMICOLON = auto()  # ;
    COMMA = auto()     # ,
    DOT = auto()       # .

    # ---- bookkeeping ----
    EOF = auto()
    ERROR = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"Lexeme: {self.lexeme}, Token: {self.type.name}"
