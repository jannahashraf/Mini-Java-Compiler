# Mini Java Compiler — Phase 1 Report

**Course:** CSCI415, Compiler Design — Fall 2026

**Team:** Jannah Ashraf, Yahia Hany, Ahmed AbdelMaboud, Omar Hesham, Abdelrahman Zaky



## Overview and implementation status

Phase 1 reads Mini Java source character by character, classifies lexemes and
prepares a token stream and identifier symbol table for later compiler phases.
The team uses separate helper modules with a shared `Lexer` reader and token
contract. All modules are implemented and integrated: keywords and identifiers,
numeric and string literals, longest-match operators and delimiters, comments,
error reporting and the symbol table. The specification sample matches its
golden output, and all 31 tests pass (18 unit/CLI tests and 13 integration
tests).

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
The identifier, literal and operator helpers report their own errors through
this same interface, including `1name`/`2_name` invalid identifiers.

## Testing, challenges and solutions

The unit/CLI suite contains 18 passing tests using Python's standard-library
`unittest`, the real character reader and the CLI. It covers empty/adjacent
comments, LF/CRLF input, incomplete delimiters, EOF boundaries, non-nested
blocks, opening-position diagnostics and a large multi-line block. Reporter
tests verify exact formatting and isolation between scans; CLI tests verify
stdout/stderr and exit statuses.

An additional 13 integration tests define full-lexer acceptance criteria:
sample output, case sensitivity, all token categories, symbol-table first
occurrences, longest-match operators, comment/string boundaries and recovery.
All 13 pass against the integrated lexer. `tests/sample_programs.mj` supplies
three programs in one file, and separate negative fixtures exercise the four
required diagnostic kinds.

The main challenges were preserving positions across skipped text, distinguishing
division from comments, and testing errors independently. Using only the shared
reader preserves positions; the scanner's two-character dispatch reserves `/`
for the operator helper unless it starts a comment. Separate negative files
prevent an unclosed string from swallowing an unterminated comment test.
Digit-started invalid identifiers such as `1name` and `2_name` are rejected in
`scan_number()` before any number token is emitted.

Run `python3 -m unittest discover -s tests -v` for the unit/CLI checks and
`python3 -m unittest discover -s tests/integration -v` for whole-lexer
acceptance. No ready-made lexer/parser library is used.
