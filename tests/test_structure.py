from compiler.ast.nodes import ParseTreeNode
from compiler.ast.printer import print_tree
from compiler.parser.base import ParserBase
from compiler.parser.parser import Parser
from compiler.tokens import Token, TokenType


def test_parser_combines_all_member_modules():
    parser = Parser([Token(TokenType.EOF, "", 1, 1)])
    assert isinstance(parser, ParserBase)
    for method in ("parse_program", "parse_block", "parse_expression"):
        assert callable(getattr(parser, method))


def test_parse_tree_node_and_printer(capsys):
    root = ParseTreeNode("Program")
    root.add(ParseTreeNode("ClassDecl", Token(TokenType.CLASS, "class", 1, 1)))
    print_tree(root)
    assert capsys.readouterr().out == "Program\n  ClassDecl 'class'\n"
