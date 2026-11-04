# Error Handling

Lexical errors are diagnostics, not exceptions. The scanner records the problem,
keeps going where possible, and still produces a token stream ending in `EOF`.

## The reporter

All helpers call the same method:

```python
lexer.reporter.error(message, line, col)
```

`LexerErrorReporter.error()`:

1. formats the message as
   `Error: <message> at line <line>, column <col>.`;
2. appends the formatted string to `reporter.errors` in encounter order;
3. prints the same string to **stderr** immediately.

So helpers pass only the bare message (for example `invalid character '@'`) and
the starting position. The prefix `Error:`, the location phrase, and the final
period are added centrally.

Streams are separated deliberately: tokens are printed to stdout by the CLI and
diagnostics go to stderr. `reporter.errors` is available for programmatic checks
and tests.

## Position conventions

- `line` and `col` are 1-based.
- Reported positions refer to the **start** of the offending construct, not the
  point where the error is detected. For example, an unclosed comment reports
  the opening `/*`, and an unclosed string reports the opening quote.
- `col` counts characters, not bytes. A `\n` resets the column; `\r` counts as a
  normal character.

## Diagnostic kinds

The scanner produces four required diagnostic forms.

| Situation | Message passed to the reporter | Typical output |
|---|---|---|
| Unknown character | `invalid character '@'` | `Error: invalid character '@' at line 1, column 12.` |
| Digit-started invalid name | `invalid identifier '1name'` | `Error: invalid identifier '1name' at line 1, column 1.` |
| EOF inside a string | `unclosed string literal starting` | `Error: unclosed string literal starting at line 1, column 15.` |
| EOF inside a block comment | `unclosed comment starting` | `Error: unclosed comment starting at line 1, column 1.` |
| Malformed number | `invalid number literal '5.'` | `Error: invalid number literal '5.' at line 1, column 1.` |

The first four are exercised by dedicated fixtures in `tests/fixtures/errors/`.
The malformed-number diagnostic has no separate fixture but is implemented in
`scan_number()` and can be triggered with input such as `5.` or `1.2.3`.

## Recovery behavior by helper

### Unknown character (`operators.py`)

The character is consumed, then the error is reported. Scanning resumes at the
next character, so later tokens are still produced. For example, in
`int x = 10 @ 5;` the error is recorded but `5` and `;` still scan normally.

### Malformed number / invalid identifier (`literals.py`)

`scan_number()` consumes the malformed run and reports one error, emitting no
token for it:

- trailing dot (`5.`) or second dot (`1.2.3`) → `invalid number literal`;
- letter/underscore after digits (`1name`, `2_name`) → `invalid identifier`.

Consuming the whole run avoids producing misleading partial tokens such as `1`
followed by `name`.

### Unclosed string (`literals.py`)

The helper consumes to EOF looking for the closing quote, reports once at the
opening quote, and emits no `STRING` token. Because the rest of the file is
treated as string contents, any comments or errors after the opening quote are
not scanned separately.

### Unclosed block comment (`comments.py`)

The helper consumes to EOF, reports once at the opening `/*`, and leaves the
cursor at EOF. The main loop then appends `EOF`. Block comments do not nest, so
the first `*/` always closes; an opener inside a comment is just text.

### Line comments

A `//` comment has no error condition: it ends at a line ending or EOF.

## Multiple errors

Reporting does not stop the scan, so several independent errors can be collected
in one run. Order in `reporter.errors` matches source order of detection. Some
constructs can swallow later input, however:

- an unclosed string consumes everything to EOF;
- an unclosed block comment consumes everything to EOF.

For that reason `tests/sample_errors.mj` (which mixes an invalid symbol, an
invalid identifier, an unclosed string, and an unclosed comment) is not used to
verify all four diagnostics together; the independent fixtures are. An unclosed
string before a block comment prevents the comment from being scanned as code.

## Reporter lifetime

A fresh `Lexer` creates a fresh `LexerErrorReporter`. Reporters do not share
state, so scanning one file cannot leak diagnostics into another. `has_errors()`
is simply `bool(self.errors)`.

## CLI exit status

`main.py` maps the scan result to an exit code:

| Code | Meaning |
|---|---|
| `0` | File scanned successfully; no lexical errors. |
| `1` | One or more lexical errors were reported. |
| `2` | Incorrect command-line usage (not exactly one source-file argument). |

Tokens (including `EOF`) are still printed to stdout when the exit code is `1`;
diagnostics are on stderr. Usage errors print the usage line to stdout and
return `2`.
