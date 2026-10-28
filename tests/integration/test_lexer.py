"""Whole-lexer acceptance tests; require Members 2, 3 and 4's implementations.

Run explicitly with: python3 -m unittest discover -s tests/integration -v
"""
from __future__ import annotations

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from src.scanner import Lexer
from src.tokens import Token, TokenType


ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"


class LexerIntegrationTests(unittest.TestCase):
    def scan_valid(self, source: str) -> tuple[Lexer, list[Token]]:
        lexer = Lexer(source)
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            tokens = lexer.scan_tokens()
        self.assertEqual(lexer.reporter.errors, [])
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        self.assertEqual(sum(t.type == TokenType.EOF for t in tokens), 1)
        self.assertNotIn(TokenType.ERROR, [t.type for t in tokens])
        return lexer, tokens

    def test_spec_sample_matches_golden_output(self) -> None:
        source = (TESTS / "sample1.mj").read_text(encoding="utf-8")
        expected = (TESTS / "expected_output.txt").read_text(encoding="utf-8")
        _, tokens = self.scan_valid(source)
        self.assertEqual("\n".join(str(t) for t in tokens) + "\n", expected)

    def test_keywords_boolean_literals_and_case_sensitive_identifiers(self) -> None:
        cases = [
            ("class", TokenType.CLASS),
            ("public", TokenType.PUBLIC),
            ("static", TokenType.STATIC),
            ("void", TokenType.VOID),
            ("int", TokenType.INT),
            ("float", TokenType.FLOAT),
            ("boolean", TokenType.BOOLEAN),
            ("char", TokenType.CHAR),
            ("String", TokenType.STRING_TYPE),
            ("if", TokenType.IF),
            ("else", TokenType.ELSE),
            ("while", TokenType.WHILE),
            ("for", TokenType.FOR),
            ("return", TokenType.RETURN),
            ("main", TokenType.MAIN),
            ("true", TokenType.BOOLEAN_LITERAL),
            ("false", TokenType.BOOLEAN_LITERAL),
            ("Class", TokenType.IDENTIFIER),
            ("string", TokenType.IDENTIFIER),
            ("Main", TokenType.IDENTIFIER),
            ("True", TokenType.IDENTIFIER),
            ("FALSE", TokenType.IDENTIFIER),
            ("_count", TokenType.IDENTIFIER),
            ("x1", TokenType.IDENTIFIER),
            ("total_marks", TokenType.IDENTIFIER),
        ]
        _, tokens = self.scan_valid(" ".join(lexeme for lexeme, _ in cases))
        self.assertEqual([(t.lexeme, t.type) for t in tokens[:-1]], cases)

    def test_symbol_table_preserves_first_occurrence(self) -> None:
        lexer, tokens = self.scan_valid("age age\nother age")
        self.assertEqual(len(lexer.symbol_table), 2)
        self.assertEqual(lexer.symbol_table.lookup("age"), tokens[0])
        self.assertEqual(lexer.symbol_table.lookup("other"), tokens[2])
        self.assertIsNone(lexer.symbol_table.lookup("missing"))
        self.assertEqual((tokens[0].line, tokens[0].col), (1, 1))
        self.assertEqual((tokens[2].line, tokens[2].col), (2, 1))

    def test_numeric_and_single_or_double_quoted_literals(self) -> None:
        cases = [
            ("0", TokenType.NUMBER),
            ("10", TokenType.NUMBER),
            ("25.5", TokenType.NUMBER),
            ('"Hello"', TokenType.STRING),
            ("'A'", TokenType.STRING),
            ("''", TokenType.STRING),
            ('""', TokenType.STRING),
        ]
        _, tokens = self.scan_valid(" ".join(lexeme for lexeme, _ in cases))
        self.assertEqual([(t.lexeme, t.type) for t in tokens[:-1]], cases)

    def test_operators_use_longest_match(self) -> None:
        cases = [
            ("=", TokenType.ASSIGN),
            ("+", TokenType.MATHOP),
            ("-", TokenType.MATHOP),
            ("*", TokenType.MATHOP),
            ("/", TokenType.MATHOP),
            ("%", TokenType.MATHOP),
            (">", TokenType.LOGOP),
            ("<", TokenType.LOGOP),
            (">=", TokenType.LOGOP),
            ("<=", TokenType.LOGOP),
            ("==", TokenType.LOGOP),
            ("!=", TokenType.LOGOP),
        ]
        _, tokens = self.scan_valid(" ".join(lexeme for lexeme, _ in cases))
        self.assertEqual([(t.lexeme, t.type) for t in tokens[:-1]], cases)

    def test_all_delimiters(self) -> None:
        _, tokens = self.scan_valid("(){}[];,.")
        self.assertEqual(
            [t.type for t in tokens[:-1]],
            [
                TokenType.LPAR, TokenType.RPAR, TokenType.LCUR, TokenType.RCUR,
                TokenType.LSQU, TokenType.RSQU, TokenType.SEMICOLON,
                TokenType.COMMA, TokenType.DOT,
            ],
        )
        self.assertEqual([t.col for t in tokens[:-1]], list(range(1, 10)))

    def test_comments_separate_tokens_and_do_not_consume_division(self) -> None:
        source = "int/* gap */x=8/2;// tail\n/* next\nline */x=x+1;"
        _, tokens = self.scan_valid(source)
        self.assertEqual(
            [t.lexeme for t in tokens[:-1]],
            ["int", "x", "=", "8", "/", "2", ";", "x", "=", "x", "+", "1", ";"],
        )
        self.assertEqual(tokens[4].type, TokenType.MATHOP)
        self.assertEqual((tokens[1].line, tokens[1].col), (1, 13))
        self.assertEqual((tokens[7].line, tokens[7].col), (3, 8))

    def test_comment_markers_inside_strings_remain_literal_text(self) -> None:
        lexemes = ['"http://host/*path*/"', "'// literal'", '"/* literal */"']
        _, tokens = self.scan_valid(" ".join(lexemes))
        self.assertEqual([t.lexeme for t in tokens[:-1]], lexemes)
        self.assertEqual([t.type for t in tokens[:-1]], [TokenType.STRING] * 3)

    def test_multiple_programs_cover_the_shared_token_contract(self) -> None:
        source = (TESTS / "sample_programs.mj").read_text(encoding="utf-8")
        _, tokens = self.scan_valid(source)
        self.assertEqual({t.type for t in tokens}, set(TokenType) - {TokenType.ERROR})
        self.assertEqual(sum(t.type == TokenType.CLASS for t in tokens), 3)

    def test_spec_error_fixtures(self) -> None:
        cases = [
            (
                "invalid_symbol.mj",
                "Error: invalid character '@' at line 1, column 12.",
            ),
            (
                "invalid_identifier.mj",
                "Error: invalid identifier '1name' at line 1, column 1.",
            ),
            (
                "unclosed_string.mj",
                "Error: unclosed string literal starting at line 1, column 15.",
            ),
            (
                "unclosed_comment.mj",
                "Error: unclosed comment starting at line 1, column 1.",
            ),
        ]
        for filename, expected in cases:
            with self.subTest(filename=filename):
                source = (TESTS / "fixtures" / "errors" / filename).read_text(
                    encoding="utf-8"
                )
                lexer = Lexer(source)
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    tokens = lexer.scan_tokens()
                self.assertEqual(lexer.reporter.errors, [expected])
                self.assertEqual(stderr.getvalue(), expected + "\n")
                self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_digit_followed_by_underscore_is_an_invalid_identifier(self) -> None:
        lexer = Lexer("  2_name = 5;")
        with redirect_stderr(io.StringIO()):
            tokens = lexer.scan_tokens()
        self.assertEqual(
            lexer.reporter.errors,
            ["Error: invalid identifier '2_name' at line 1, column 3."],
        )
        self.assertFalse(any(t.lexeme in ("2", "_name") for t in tokens))
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_scanning_recovers_after_an_invalid_character(self) -> None:
        lexer = Lexer("int x = 10 @ 5;\nint recovered = 7;")
        with redirect_stderr(io.StringIO()):
            tokens = lexer.scan_tokens()
        self.assertEqual(
            lexer.reporter.errors,
            ["Error: invalid character '@' at line 1, column 12."],
        )
        self.assertIn(Token(TokenType.IDENTIFIER, "recovered", 2, 5), tokens)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_sample_cli_prints_the_golden_output(self) -> None:
        result = subprocess.run(
            [sys.executable, "main.py", "tests/sample1.mj"],
            cwd=ROOT, capture_output=True, text=True, timeout=5, check=False,
        )
        expected = (TESTS / "expected_output.txt").read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
