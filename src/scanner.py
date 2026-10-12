"""Mini Java lexical analyzer (scanner).

OWNER: Member 1 (Core & Integration).

This file contains the character reader, the main scan loop and the dispatch
to each team member's helper module. The helpers live in their own files so we
never edit the same file by accident:

  identifiers.scan_identifier_or_keyword  (Member 2)
  literals.scan_number / scan_string      (Member 3)
  operators.scan_operator_or_delimiter    (Member 4)
  comments.skip_comment                   (Member 5)
"""
from __future__ import annotations

from . import comments, identifiers, literals, operators
from .errors import LexerErrorReporter
from .symbol_table import SymbolTable
from .tokens import Token, TokenType

WHITESPACE = " \t\r\n"


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.reporter = LexerErrorReporter()
        self.symbol_table = SymbolTable()
        self.tokens: list[Token] = []

    # ---------- character reader (Member 1) ----------
    def current(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else ""

    def peek(self, offset: int = 1) -> str:
        i = self.pos + offset
        return self.source[i] if i < len(self.source) else ""

    def advance(self) -> str:
        ch = self.current()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def at_end(self) -> bool:
        return self.pos >= len(self.source)

    def emit(self, token_type: TokenType, lexeme: str, line: int, col: int) -> Token:
        token = Token(token_type, lexeme, line, col)
        self.tokens.append(token)
        return token

    # ---------- main loop (Member 1) ----------
    def scan_tokens(self) -> list[Token]:
        while not self.at_end():
            ch = self.current()

            if ch in WHITESPACE:
                self.advance()
            elif ch == "/" and self.peek() in ("/", "*"):
                comments.skip_comment(self)
            elif ch.isalpha() or ch == "_":
                identifiers.scan_identifier_or_keyword(self)
            elif ch.isdigit():
                literals.scan_number(self)
            elif ch in ("\"", "'"):
                literals.scan_string(self)
            else:
                operators.scan_operator_or_delimiter(self)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
