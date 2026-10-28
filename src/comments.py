"""Comment handling for Mini Java.

OWNER: Member 5 (Comments, Errors, Testing & Report).

Two comment styles, both skipped (no token emitted):
  //  single-line: ignore until end of line
  /* ... */  multi-line: ignore until the closing */

If a multi-line comment never closes before end of file, report:
    lexer.reporter.error("unclosed comment starting", start_line, start_col)

The main loop only calls this when the two current characters are "//" or "/*",
so you may assume lexer.current() == '/' at entry.
"""
from __future__ import annotations


def skip_comment(lexer) -> None:
    """Skip one comment, reporting an unclosed block at its opening position.

    Leave a line comment's newline for the main loop. Block comments do not
    nest: the first ``*/`` closes the comment, as in Java. All consumption goes
    through ``advance()`` to keep the shared reader's line/column accurate.
    """
    start_line, start_col = lexer.line, lexer.col
    style = lexer.peek()
    lexer.advance()
    lexer.advance()

    if style == "/":
        while not lexer.at_end() and lexer.current() not in ("\r", "\n"):
            lexer.advance()
        return

    while not lexer.at_end():
        if lexer.current() == "*" and lexer.peek() == "/":
            lexer.advance()
            lexer.advance()
            return
        lexer.advance()

    lexer.reporter.error("unclosed comment starting", start_line, start_col)
