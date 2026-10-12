"""Comment handling for Mini Java.

OWNER: Member 5 (Comments, Errors, Testing & Report).

Two comment styles, both skipped (no token emitted):
  //  single-line: ignore until end of line
  /* ... */  multi-line: ignore until the closing */

If a multi-line comment never closes before end of file, report:
    lexer.reporter.error("unclosed comment starting", start_line, start_col)

The main loop only calls this when the two current characters are "//" or "/*",
so you may assume lexer.current() == '/' at entry.

TODO(Member 5): implement this function.
"""
from __future__ import annotations


def skip_comment(lexer) -> None:
    """Skip a single-line or multi-line comment."""
    raise NotImplementedError("Member 5: skip_comment")
