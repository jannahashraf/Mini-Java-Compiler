"""Compiler driver: source -> tokens -> parse tree -> semantic analysis."""
from __future__ import annotations

import sys

from compiler.ast.printer import print_tree
from compiler.errors import MiniJavaError
from compiler.lexer.scanner import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.tokens import TokenType

USAGE = "Usage: python3 main.py [--tokens | --parse] <source-file>"


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    stage = "all"
    if args and args[0] in ("--tokens", "--parse"):
        stage = args[0][2:]
        args.pop(0)

    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    path = args[0]
    try:
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
    except OSError as exc:
        print(f"Error: cannot read '{path}': {exc}", file=sys.stderr)
        return 2

    lexer = Lexer(source)
    tokens = [token for token in lexer.scan_tokens() if token.type is not TokenType.ERROR]

    if stage == "tokens":
        for token in tokens:
            print(token)
        return 1 if lexer.reporter.has_errors() else 0
    if lexer.reporter.has_errors():
        return 1

    parser = Parser(tokens)
    try:
        tree = parser.parse_program()
    except MiniJavaError as exc:
        print(exc, file=sys.stderr)
        return 1
    except NotImplementedError as exc:
        print(f"Parser not implemented yet: {exc}", file=sys.stderr)
        return 1

    print_tree(tree)
    if stage == "parse":
        return 0

    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(tree)
    except MiniJavaError as exc:
        print(exc, file=sys.stderr)
        return 1
    except NotImplementedError as exc:
        print(f"Semantic analysis not implemented yet: {exc}", file=sys.stderr)
        return 1
    return 0
