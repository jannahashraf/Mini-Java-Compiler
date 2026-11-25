"""Checks that every compiler section shares one token contract and CLI."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from compiler.lexer.scanner import Lexer
from compiler.tokens import TokenType

ROOT = Path(__file__).resolve().parents[1]


class SharedContractTests(unittest.TestCase):
    def test_token_names_from_the_parser_contract_are_aliases(self) -> None:
        self.assertIs(TokenType.BOOLEAN_TYPE, TokenType.BOOLEAN)
        self.assertIs(TokenType.TRUE, TokenType.BOOLEAN_LITERAL)
        self.assertIs(TokenType.FALSE, TokenType.BOOLEAN_LITERAL)

    def test_lexer_token_exposes_the_column_alias(self) -> None:
        lexer = Lexer("class")
        token = lexer.scan_tokens()[0]
        self.assertEqual((token.line, token.column, token.col), (1, 1, 1))
        self.assertEqual(token.type, TokenType.CLASS)


class CompilerCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "main.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def test_tokens_stage_prints_the_lexer_stream(self) -> None:
        result = self.run_cli("--tokens", "inputs/valid/example.minijava")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Lexeme: class, Token: CLASS", result.stdout)
        self.assertIn("Lexeme: , Token: EOF", result.stdout)

    def test_lexical_errors_are_reported_before_parsing(self) -> None:
        result = self.run_cli("--tokens", "tests/fixtures/errors/invalid_symbol.mj")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: invalid character '@'", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_full_pipeline_reports_the_pending_grammar_stub(self) -> None:
        result = self.run_cli("inputs/valid/example.minijava")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Parser not implemented yet:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_argument_shows_usage(self) -> None:
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr,
            "Usage: python3 main.py [--tokens | --parse] <source-file>\n",
        )


if __name__ == "__main__":
    unittest.main()
