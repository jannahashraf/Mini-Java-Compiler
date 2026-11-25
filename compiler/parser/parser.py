from compiler.parser.base import ParserBase
from compiler.parser.declarations import DeclarationParserMixin
from compiler.parser.expressions import ExpressionParserMixin
from compiler.parser.statements import StatementParserMixin


class Parser(DeclarationParserMixin, StatementParserMixin, ExpressionParserMixin, ParserBase):
    pass
