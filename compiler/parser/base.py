from compiler.errors import MiniJavaSyntaxError
from compiler.tokens import TokenType

SYNCHRONIZING_TYPES = {
    TokenType.SEMICOLON,
    TokenType.RCUR,
    TokenType.IF,
    TokenType.WHILE,
    TokenType.FOR,
    TokenType.RETURN,
    TokenType.CLASS,
    TokenType.PUBLIC,
    TokenType.PRIVATE,
    TokenType.PROTECTED,
    TokenType.STATIC,
    TokenType.VOID,
    TokenType.INT,
    TokenType.BOOLEAN_TYPE,
    TokenType.STRING_TYPE,
    TokenType.EOF,
}


class ParserBase:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.position = 0

    @property
    def current(self):
        return self.tokens[self.position]

    @property
    def previous(self):
        return self.tokens[max(0, self.position - 1)]

    def is_at_end(self):
        return self.current.type is TokenType.EOF

    def check(self, token_type):
        return self.current.type is token_type

    def advance(self):
        token = self.current
        if not self.is_at_end():
            self.position += 1
        return token

    def match(self, *token_types):
        if self.current.type in token_types:
            return self.advance()
        return None

    def expect(self, token_type, description=None):
        if self.check(token_type):
            return self.advance()
        expected = description or token_type.value
        raise MiniJavaSyntaxError(
            f"Expected '{expected}' but found '{self.current.lexeme}'",
            self.current.line,
            self.current.column,
        )

    def error(self, message):
        raise MiniJavaSyntaxError(message, self.current.line, self.current.column)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous.type in SYNCHRONIZING_TYPES:
                return
            if self.current.type in SYNCHRONIZING_TYPES:
                return
            self.advance()
