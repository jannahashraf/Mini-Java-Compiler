# Phase 1 tests

Run commands from the repository root with Python 3.10 or newer. Only Python's
standard library is needed.

## Member 5 checks

```bash
python3 -m unittest discover -s tests -v
```

These 18 tests run against the real `Lexer` reader, comment handler, reporter
and CLI. They cover:

- Empty, adjacent, single-line and multi-line comments; EOF with no newline.
- LF/CRLF positions, first-terminator block closing, and code-like comment text.
- Unterminated blocks, including incomplete delimiters and non-default opening
  positions; no consumption beyond EOF and no comment tokens.
- A large block, to check that scanning does not depend on recursion depth.
- Exact diagnostic text, encounter order, independent reporter instances, and
  stderr output.
- CLI success, lexical-error and usage exit codes (`0`, `1`, `2`), with tokens on
  stdout and lexical diagnostics on stderr.

## Whole-lexer acceptance checks

```bash
python3 -m unittest discover -s tests/integration -v
```

The 13 integration tests exercise the specification's sample output, every
shared token category, case sensitivity, symbol-table first occurrences,
operators, literals, comment/token boundaries, error positions and recovery.
They use the real modules, without replacement implementations or automatic
skips. `integration/` is an explicit discovery directory, so the Member 5
command above can run independently while teammates implement their helpers.

**Current integration blocker:** `src/identifiers.py`, `src/literals.py`,
`src/operators.py` and the symbol-table methods still contain the original
`NotImplementedError` placeholders. Run this suite again after Members 2–4
complete those modules. A failure here is not a passing or skipped test.

Integration reminders:

- `scan_number()` receives digit-started input. It must reject `1name` and
  `2_name` as invalid identifiers rather than split them into valid tokens;
  Member 3 should coordinate this requirement with Members 1 and 2.
- `String` is `STRING_TYPE`; quoted values, including `'A'`, are `STRING`.
  `boolean` is `BOOLEAN`, while `true`/`false` are `BOOLEAN_LITERAL`.
- Helpers call `reporter.error(message, line, col)` with the starting position.
  Messages omit the `Error:` prefix and final location/punctuation, which the
  reporter supplies.

## Input fixtures

| Input | Purpose |
|---|---|
| `sample1.mj` | Specification example; compare the complete CLI stream with `expected_output.txt`, including the shared `EOF` token. |
| `sample_programs.mj` | Three Mini Java programs in one input file; together cover all declared token categories except `ERROR`. |
| `comments_only.mj` | Comment-only smoke test that works before the other helpers are implemented. |
| `fixtures/errors/invalid_symbol.mj` | `@` at line 1, column 12. |
| `fixtures/errors/invalid_identifier.mj` | `1name` at line 1, column 1. |
| `fixtures/errors/unclosed_string.mj` | Opening double quote at line 1, column 15. |
| `fixtures/errors/unclosed_comment.mj` | Opening `/*` at line 1, column 1. |
| `sample_errors.mj` | Mixed-error example; its unclosed string can consume the following comment, so use the independent fixtures to verify all four error kinds. |

For example, these commands already work:

```bash
python3 main.py tests/comments_only.mj
python3 main.py tests/fixtures/errors/unclosed_comment.mj
```

The second command intentionally exits with status `1` and prints one error to
stderr. Comments never emit tokens; an unterminated block consumes through EOF,
reports its opening position once, and lets the scanner append `EOF`.
