"""CLI checks that run with the current shared scanner and Member 5 modules."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommentCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "main.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def test_comment_only_input_succeeds(self) -> None:
        result = self.run_cli("tests/comments_only.mj")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Lexeme: , Token: EOF\n")
        self.assertEqual(result.stderr, "")

    def test_unclosed_comment_fails_with_separate_diagnostic(self) -> None:
        result = self.run_cli("tests/fixtures/errors/unclosed_comment.mj")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "Lexeme: , Token: EOF\n")
        self.assertEqual(
            result.stderr,
            "Error: unclosed comment starting at line 1, column 1.\n",
        )

    def test_missing_argument_shows_usage(self) -> None:
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "Usage: python3 main.py <source-file>\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
