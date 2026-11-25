"""Shared token definitions for the Mini Java compiler.

OWNER: Member 1 (Core & Integration).

This file is the contract between every module in every phase. Do NOT rename or
remove a token without telling the whole team, because the lexer helpers and the
parser grammar rules both depend on it. Phase 2/3 names that differ from the
Phase 1 names are exposed here as enum aliases.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    # ---- keywords (Member 2) ----
    CLASS = "CLASS"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    PROTECTED = "PROTECTED"
    STATIC = "STATIC"
    VOID = "VOID"
    INT = "INT"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    BOOLEAN_TYPE = "BOOLEAN"
    CHAR = "CHAR"
    STRING_TYPE = "STRING_TYPE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"
    MAIN = "MAIN"

    # ---- identifiers & literals (Members 2 & 3) ----
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL"  # true / false
    TRUE = "BOOLEAN_LITERAL"
    FALSE = "BOOLEAN_LITERAL"

    # ---- operators (Member 4) ----
    ASSIGN = "ASSIGN"
    MATHOP = "MATHOP"
    LOGOP = "LOGOP"

    # ---- delimiters (Member 4) ----
    LPAR = "LPAR"
    RPAR = "RPAR"
    LCUR = "LCUR"
    RCUR = "RCUR"
    LSQU = "LSQU"
    RSQU = "RSQU"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"

    # ---- bookkeeping ----
    EOF = "EOF"
    ERROR = "ERROR"


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    col: int

    @property
    def column(self) -> int:
        return self.col

    def __str__(self) -> str:
        return f"Lexeme: {self.lexeme}, Token: {self.type.name}, line: {self.line}, col: {self.col}"
