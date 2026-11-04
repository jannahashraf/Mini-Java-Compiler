# Usage

## Requirements

- Python 3.10 or newer.
- No third-party packages.

## Command line

```bash
python3 main.py <source-file>
```

`main.py` reads exactly one file as UTF-8, scans it, and prints one line per
token to stdout:

```text
Lexeme: <lexeme>, Token: <TOKEN_TYPE>
```

Lexical diagnostics are printed to stderr. The final token is always `EOF`, whose
lexeme is empty:

```text
Lexeme: , Token: EOF
```

Example:

```bash
python3 main.py tests/sample1.mj
```

Output begins:

```text
Lexeme: class, Token: CLASS
Lexeme: Student, Token: IDENTIFIER
Lexeme: {, Token: LCUR
Lexeme: public, Token: PUBLIC
Lexeme: static, Token: STATIC
Lexeme: void, Token: VOID
Lexeme: main, Token: MAIN
...
Lexeme: , Token: EOF
```

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Scan completed with no lexical errors. |
| `1` | At least one lexical error was reported. Tokens are still printed. |
| `2` | Wrong number of command-line arguments; a usage line is printed. |

Example of an error run:

```bash
python3 main.py tests/fixtures/errors/unclosed_comment.mj
```

stdout:

```text
Lexeme: , Token: EOF
```

stderr:

```text
Error: unclosed comment starting at line 1, column 1.
```

exit status: `1`.

## Programmatic use

```python
from src.scanner import Lexer
from src.tokens import TokenType

source = 'int age = 20;'
lexer = Lexer(source)
tokens = lexer.scan_tokens()

for token in tokens:
    print(token.type.name, repr(token.lexeme), token.line, token.col)

if lexer.reporter.has_errors():
    print("errors:", lexer.reporter.errors)

print("symbols:", len(lexer.symbol_table))
print("age at:", lexer.symbol_table.lookup("age"))
```

This prints the token stream, then reports the number of distinct identifiers and
the first `age` token. `scan_tokens()` is normally called once per lexer.

## What the scanner does not do

Phase 1 is lexical analysis only:

- It does not parse statements or expressions.
- It does not validate that tokens form a grammatical program.
- It does not assign types or check declarations.
- It does not evaluate literals; `NUMBER` lexemes remain strings.

The outputs intended for later phases are `lexer.tokens` (the stream) and
`lexer.symbol_table` (first occurrence of each user-defined identifier).

## Related reading

- [architecture.md](architecture.md) — how scanning works internally.
- [data-structures.md](data-structures.md) — `Token`, `Lexer`, `SymbolTable`, and reporter shapes.
- [token-reference.md](token-reference.md) — complete token vocabulary.
- [error-handling.md](error-handling.md) — diagnostics and recovery.
- [testing.md](testing.md) — how to run and extend the tests.
