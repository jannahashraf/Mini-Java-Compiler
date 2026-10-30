"""Member 5 comment tests using the real shared character reader."""
from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from src.comments import skip_comment
from src.scanner import Lexer
from src.tokens import Token, TokenType


class CommentTests(unittest.TestCase):
    def test_line_comments_stop_before_newline_or_eof(self) -> None:
        cases = [
            ("//", "", 3),
            ("//abc", "", 6),
            ("//abc\nnext", "\nnext", 6),
            ("//abc\r\nnext", "\r\nnext", 6),
            ("//abc\rnext", "\rnext", 6),
        ]
        for source, remaining, column in cases:
            with self.subTest(source=source):
                lexer = Lexer(source)
                skip_comment(lexer)
                self.assertEqual(lexer.source[lexer.pos:], remaining)
                self.assertEqual((lexer.line, lexer.col), (1, column))
                self.assertEqual(lexer.tokens, [])
                self.assertEqual(lexer.reporter.errors, [])

    def test_closed_blocks_leave_the_next_character_unconsumed(self) -> None:
        cases = [
            ("/**/next", 1, 5),
            ("/* one */next", 1, 10),
            ("/*a\nb*/next", 2, 4),
            ("/*a\r\nb*/next", 2, 4),
            ("/* ***/next", 1, 8),
        ]
        for source, line, column in cases:
            with self.subTest(source=source):
                lexer = Lexer(source)
                skip_comment(lexer)
                self.assertEqual(lexer.source[lexer.pos:], "next")
                self.assertEqual((lexer.line, lexer.col), (line, column))
                self.assertEqual(lexer.tokens, [])
                self.assertEqual(lexer.reporter.errors, [])

    def test_blocks_close_at_the_first_terminator_without_nesting(self) -> None:
        lexer = Lexer("/* outer /* inner */next */")
        skip_comment(lexer)
        self.assertEqual(lexer.source[lexer.pos:], "next */")
        self.assertFalse(lexer.reporter.has_errors())

    def test_comment_contents_are_not_scanned_as_code(self) -> None:
        sources = [
            "// /* */ @ 1name ' \" class true",
            "/* // @ 1name ' \" class true */",
        ]
        for source in sources:
            with self.subTest(source=source):
                lexer = Lexer(source)
                tokens = lexer.scan_tokens()
                self.assertEqual([token.type for token in tokens], [TokenType.EOF])
                self.assertEqual(len(lexer.symbol_table), 0)
                self.assertFalse(lexer.reporter.has_errors())

    def test_adjacent_comments_are_all_consumed(self) -> None:
        lexer = Lexer("/**//**///end")
        self.assertEqual(lexer.scan_tokens(), [Token(TokenType.EOF, "", 1, 14)])
        self.assertEqual(lexer.pos, len(lexer.source))
        self.assertFalse(lexer.reporter.has_errors())

    def test_main_loop_consumes_line_comment_newlines(self) -> None:
        for source in ("//a\n/**/", "//a\r\n/**/"):
            with self.subTest(source=source):
                lexer = Lexer(source)
                self.assertEqual(
                    lexer.scan_tokens(), [Token(TokenType.EOF, "", 2, 5)]
                )
                self.assertFalse(lexer.reporter.has_errors())

    def test_closing_delimiter_at_eof_does_not_advance_past_eof(self) -> None:
        for source in ("/**/", "/* body */", "/*\n*/"):
            with self.subTest(source=source):
                lexer = Lexer(source)
                skip_comment(lexer)
                self.assertTrue(lexer.at_end())
                self.assertEqual(lexer.pos, len(source))
                self.assertEqual(lexer.tokens, [])
                self.assertFalse(lexer.reporter.has_errors())

    def test_unterminated_blocks_report_exactly_once(self) -> None:
        for source in ("/*", "/*/", "/**", "/* no end", "/*\n**"):
            with self.subTest(source=source):
                lexer = Lexer(source)
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    skip_comment(lexer)
                expected = "Error: unclosed comment starting at line 1, column 1."
                self.assertEqual(lexer.reporter.errors, [expected])
                self.assertEqual(stderr.getvalue(), expected + "\n")
                self.assertEqual(lexer.pos, len(source))
                self.assertTrue(lexer.at_end())
                self.assertEqual(lexer.tokens, [])

    def test_unterminated_block_reports_its_opening_not_eof(self) -> None:
        lexer = Lexer(" \n  /* unfinished\nlast")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            tokens = lexer.scan_tokens()
        self.assertEqual(tokens, [Token(TokenType.EOF, "", 3, 5)])
        self.assertEqual(
            lexer.reporter.errors,
            ["Error: unclosed comment starting at line 2, column 3."],
        )
        self.assertEqual(stderr.getvalue(), lexer.reporter.errors[0] + "\n")
        self.assertEqual(lexer.pos, len(lexer.source))

    def test_large_block_is_scanned_without_recursion(self) -> None:
        source = "/*" + "x\n" * 10_000 + "*/next"
        lexer = Lexer(source)
        skip_comment(lexer)
        self.assertEqual(lexer.source[lexer.pos:], "next")
        self.assertEqual((lexer.line, lexer.col), (10_001, 3))
        self.assertFalse(lexer.reporter.has_errors())

    def test_comment_fixture_emits_only_eof(self) -> None:
        path = Path(__file__).parent / "comments_only.mj"
        lexer = Lexer(path.read_text(encoding="utf-8"))
        tokens = lexer.scan_tokens()
        self.assertEqual([token.type for token in tokens], [TokenType.EOF])
        self.assertEqual(len(lexer.symbol_table), 0)
        self.assertFalse(lexer.reporter.has_errors())


if __name__ == "__main__":
    unittest.main()
