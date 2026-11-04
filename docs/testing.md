# Testing

Tests use Python's standard-library `unittest` and exercise the real lexer,
reader, reporter, and CLI. No replacement implementations or optional skips are
used.

Run all commands from the repository root.

## Test suites

### Unit and CLI checks — 18 tests

```bash
python3 -m unittest discover -s tests -v
```

| File | Tests | Focus |
|---|---|---|
| `tests/test_comments.py` | 11 | Line and block comment boundaries, CRLF, nesting behavior, EOF handling, large blocks, comment-only fixtures. |
| `tests/test_errors.py` | 4 | Exact diagnostic format, encounter order, stderr-only output, reporter isolation. |
| `tests/test_cli.py` | 3 | Comment-only success, unclosed-comment failure, missing-argument usage error. |

Notable assertions:

- Line comments stop before `\n`, `\r`, or `\r\n`, leaving the line ending to
  the main loop; block comments close at the first `*/`.
- Comments emit no tokens, do not populate the symbol table, and do not scan
  code-like contents.
- Unterminated blocks report exactly once at the opening position and leave the
  cursor at EOF.
- A 10,000-line block comment scans without recursion.
- Diagnostics are identical in `reporter.errors` and stderr, and separate
  reporters do not share errors.
- CLI exit codes are `0` (success), `1` (lexical errors), and `2` (usage).

### Whole-lexer integration checks — 13 tests

```bash
python3 -m unittest discover -s tests/integration -v
```

`tests/integration/test_lexer.py` runs against the complete scanner and covers:

- The specification sample matches `tests/expected_output.txt` byte for byte.
- Every keyword and boolean literal, plus case-sensitive identifier fallbacks
  (`Class`, `string`, `Main`, `True`, `FALSE`).
- Symbol-table first-occurrence semantics and stored positions.
- Integer, float, single-quoted, double-quoted, and empty strings.
- Longest-match operators and all delimiters with correct columns.
- Comments as token separators while `/` remains division.
- Comment markers inside strings staying literal.
- Three programs in `sample_programs.mj` covering every `TokenType` except
  `ERROR`.
- All four error fixtures with exact messages and positions.
- Invalid identifiers such as `2_name` and recovery after an unknown character.
- End-to-end CLI output equal to the golden file.

`tests/integration/` is specified explicitly as a discovery directory, so it is
not included in the first command.

## Fixtures

| Input | Purpose |
|---|---|
| `tests/sample1.mj` | Specification example. |
| `tests/expected_output.txt` | Golden token stream for `sample1.mj`, including `EOF`. |
| `tests/sample_programs.mj` | Three programs covering all token categories except `ERROR`. |
| `tests/comments_only.mj` | Comment-only smoke test; only `EOF` is emitted. |
| `tests/sample_errors.mj` | Mixed-error example; useful for manual inspection but not for isolating all four diagnostics. |
| `tests/fixtures/errors/invalid_symbol.mj` | `@` at line 1, column 12. |
| `tests/fixtures/errors/invalid_identifier.mj` | `1name` at line 1, column 1. |
| `tests/fixtures/errors/unclosed_string.mj` | Opening quote at line 1, column 15. |
| `tests/fixtures/errors/unclosed_comment.mj` | Opening `/*` at line 1, column 1. |

The fixtures are intentionally separate because an unclosed string consumes the
rest of the file, which would hide a later unclosed-comment error.

## Manual checks

```bash
# Successful scan; tokens on stdout.
python3 main.py tests/sample1.mj

# Comment-only input; prints only the EOF token, exits 0.
python3 main.py tests/comments_only.mj

# Error input; prints EOF on stdout and one diagnostic on stderr, exits 1.
python3 main.py tests/fixtures/errors/unclosed_comment.mj

# Usage error; exits 2.
python3 main.py
```

## Adding tests

- Put unit tests at the top level of `tests/` so the first discovery command
  finds them. Put full-scanner tests under `tests/integration/`.
- Import from `src.*` (for example `from src.scanner import Lexer`) and run from
  the repository root.
- Redirect stderr with `contextlib.redirect_stderr(io.StringIO())` when a test
  intentionally triggers diagnostics, so test output stays clean.
- Assert `lexer.reporter.errors` for exact messages and `token.type`/`lexeme`
  for classification.
- Remember that every successful scan ends with exactly one `EOF` token; use
  `tokens[:-1]` when comparing token sequences.
