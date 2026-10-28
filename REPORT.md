# Mini Java Compiler — Phase 1 Report

**Course:** CSCI415, Compiler Design — Fall 2026

**Contribution:** Member 5 — comments, error reporting, testing and report

## Overview and implementation status

Phase 1 reads Mini Java source character by character, classifies lexemes and
prepares a token stream and identifier symbol table for later compiler phases.
The team uses separate helper modules with a shared `Lexer` reader and token
contract. Member 5's comment handling and error-reporting implementation are
complete, with executable tests and example programs. Full-program validation
depends on the remaining identifier, literal, operator and symbol-table helpers,
which are still placeholders on the current base branch.

## Token categories

The shared contract defines the following categories for the integrated lexer:

| Category | Token names / examples |
|---|---|
| Keywords | `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`, `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`, `MAIN` |
| Identifiers | `IDENTIFIER`: names such as `age`, `_count`, `studentName` |
| Literals | `NUMBER` for integers/floats; `STRING` for single- or double-quoted values; `BOOLEAN_LITERAL` for `true`/`false` |
| Operators | `ASSIGN` (`=`), `MATHOP` (`+ - * / %`), `LOGOP` (`> < >= <= == !=`) |
| Delimiters | `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT` |
| Bookkeeping | `EOF` terminates the stream; `ERROR` is available in the contract |

Mini Java is case-sensitive: `class` and `Class` differ, as do `String` and
`string`. The shared names distinguish the type keyword `BOOLEAN` from boolean
values (`BOOLEAN_LITERAL`). Comments and whitespace contribute no tokens. An
unterminated comment produces a diagnostic rather than an `ERROR` token.

## Comment handling and errors

`skip_comment()` consumes the two-character opening delimiter. For `//`, it
advances until a line ending or EOF, leaving the line ending to the scanner.
For `/*`, it advances until the first `*/`, including that closing delimiter.
Block comments do not nest, matching Java behavior. Quotes, invalid symbols and
other code-like text inside comments are ignored. Scanning uses loops and the
shared `advance()` method: it takes linear time in the comment length and
constant auxiliary space, while preserving line/column tracking.

If a block reaches EOF without closing, the helper reports its saved opening
position once. It leaves the cursor at EOF so the main scanner can finish
normally. All helpers share `LexerErrorReporter.error(message, line, col)`:

```text
Error: invalid character '@' at line 1, column 12.
Error: invalid identifier '1name' at line 1, column 1.
Error: unclosed string literal starting at line 1, column 15.
Error: unclosed comment starting at line 1, column 1.
```

The reporter records formatted messages in encounter order and writes them to
stderr, preserving stdout for tokens. Reporting does not throw an exception;
each helper controls recovery. The CLI checks `has_errors()` and returns status
`1` for lexical errors, `0` for successful scans, or `2` for incorrect usage.
Members 2–4 supply the other error detections through this same interface.

## Testing, challenges and solutions

The Member 5 suite contains 18 passing tests using Python's standard-library
`unittest`, the real character reader and the CLI. It covers empty/adjacent
comments, LF/CRLF input, incomplete delimiters, EOF boundaries, non-nested
blocks, opening-position diagnostics and a large multi-line block. Reporter
tests verify exact formatting and isolation between scans; CLI tests verify
stdout/stderr and exit statuses.

An additional 13 integration tests define full-lexer acceptance criteria:
sample output, case sensitivity, all token categories, symbol-table first
occurrences, longest-match operators, comment/string boundaries and recovery.
These checks currently expose the existing teammate placeholders; they do not
substitute mocked implementations or count unavailable behavior as passing.
`tests/sample_programs.mj` supplies three programs in one file, and separate
negative fixtures exercise the four required diagnostic kinds.

The main challenges were preserving positions across skipped text, distinguishing
division from comments, and testing errors independently. Using only the shared
reader preserves positions; the scanner's two-character dispatch reserves `/`
for the operator helper unless it starts a comment. Separate negative files
prevent an unclosed string from swallowing an unterminated comment test.
Another integration requirement is that digit-started invalid identifiers reach
`scan_number()`, so that helper must reject sequences such as `1name`.

Run `python3 -m unittest discover -s tests -v` for Member 5 checks and
`python3 -m unittest discover -s tests/integration -v` after the remaining
helpers are implemented. No ready-made lexer/parser library is used.
