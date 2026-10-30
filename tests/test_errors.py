"""Public error-reporting contract shared by all scanning helpers."""
from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from src.errors import LexerErrorReporter


class ErrorReporterTests(unittest.TestCase):
    def test_new_reporter_has_no_errors(self) -> None:
        reporter = LexerErrorReporter()
        self.assertEqual(reporter.errors, [])
        self.assertFalse(reporter.has_errors())

    def test_spec_diagnostics_are_recorded_and_written_only_to_stderr(self) -> None:
        cases = [
            (
                "invalid character '@'", 1, 12,
                "Error: invalid character '@' at line 1, column 12.",
            ),
            (
                "invalid identifier '1name'", 1, 1,
                "Error: invalid identifier '1name' at line 1, column 1.",
            ),
            (
                "unclosed string literal starting", 1, 15,
                "Error: unclosed string literal starting at line 1, column 15.",
            ),
            (
                "unclosed comment starting", 1, 1,
                "Error: unclosed comment starting at line 1, column 1.",
            ),
        ]
        for message, line, column, expected in cases:
            with self.subTest(message=message):
                reporter = LexerErrorReporter()
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    reporter.error(message, line, column)
                self.assertEqual(reporter.errors, [expected])
                self.assertTrue(reporter.has_errors())
                self.assertEqual(stderr.getvalue(), expected + "\n")
                self.assertEqual(stdout.getvalue(), "")

    def test_errors_keep_encounter_order_and_positions(self) -> None:
        reporter = LexerErrorReporter()
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            reporter.error("invalid character '@'", 2, 8)
            reporter.error("invalid identifier '2_name'", 4, 3)
        expected = [
            "Error: invalid character '@' at line 2, column 8.",
            "Error: invalid identifier '2_name' at line 4, column 3.",
        ]
        self.assertEqual(reporter.errors, expected)
        self.assertEqual(stderr.getvalue(), "\n".join(expected) + "\n")

    def test_reporters_do_not_share_errors(self) -> None:
        first, second = LexerErrorReporter(), LexerErrorReporter()
        with redirect_stderr(io.StringIO()):
            first.error("invalid character '@'", 1, 1)
        self.assertTrue(first.has_errors())
        self.assertFalse(second.has_errors())
        self.assertEqual(second.errors, [])


if __name__ == "__main__":
    unittest.main()
