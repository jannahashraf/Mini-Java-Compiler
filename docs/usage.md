# Usage

## Requirements

- Python 3.10 or newer.
- No third-party packages.

## Command line

```bash
python3 main.py [--tokens | --parse] <source-file>
```

`main.py` is the single entry point. The stages are:

| Stage | Command | Output |
|---|---|---|
| Lexer only | `python3 main.py --tokens <file>` | One line per token on stdout. |
| Through parse tree | `python3 main.py --parse <file>` | Token diagnostics, then the indented parse tree. |
| Full pipeline | `python3 main.py <file>` | Parse tree plus semantic diagnostics. |

With `--tokens`, each token line uses `Token.__str__` from
`compiler/tokens.py`, for example:

```text
Lexeme: class, Token: CLASS, line: 1, col: 1
Lexeme: , Token: EOF, line: 9, col: 1
```

Example:

```bash
python3 main.py --tokens tests/sample1.mj
```

The default pipeline currently reports the pending grammar stub on stderr and
exits 1 until the parser sections are implemented.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Selected stages completed with no errors. |
| `1` | Lexical, syntax, or semantic error reported; or a stub stage not implemented yet. |
| `2` | Wrong arguments or an unreadable source file. |

Error example:

```bash
python3 main.py --tokens tests/fixtures/errors/unclosed_comment.mj
```

stdout:

```text
Lexeme: , Token: EOF, line: 2, col: 1
```

stderr:

```text
Error: unclosed comment starting at line 1, column 1.
```

exit status: `1`.

## Programmatic use

```python
from compiler.lexer.scanner import Lexer
from compiler.tokens import TokenType

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

To parse programmatically, pass the non-`ERROR` tokens to
`compiler.parser.parser.Parser` and print the tree with
`compiler.ast.printer.print_tree`.

## Related reading

- [architecture.md](architecture.md) — how the stages work internally.
- [data-structures.md](data-structures.md) — `Token`, `Lexer`, `SymbolTable`, and reporter shapes.
- [token-reference.md](token-reference.md) — complete token vocabulary.
- [error-handling.md](error-handling.md) — diagnostics and recovery.
- [testing.md](testing.md) — how to run and extend the tests.
- [PROJECT.md](../PROJECT.md) — section assignments for the five members.
