# Mini Java Lexer — Documentation

This documentation covers Phase 1 of the Mini Java compiler: a hand-written
lexical analyzer (scanner) that turns Mini Java source text into a stream of
tokens and builds a symbol table of user-defined identifiers.

No third-party or ready-made lexer/parser libraries are used. The only runtime
dependency is the Python standard library (Python 3.10+).

## Quick start

```bash
# Scan a sample program; tokens go to stdout.
python3 main.py tests/sample1.mj

# Run the unit and CLI tests.
python3 -m unittest discover -s tests -v

# Run the whole-lexer integration tests.
python3 -m unittest discover -s tests/integration -v
```

## Documentation index

| Document | Contents |
|---|---|
| [architecture.md](architecture.md) | How the scanner works end to end: reader, main loop, dispatch, helper modules, and data flow. |
| [data-structures.md](data-structures.md) | `TokenType`, `Token`, `Lexer` state, `SymbolTable`, error reporter, and lookup tables. |
| [token-reference.md](token-reference.md) | Every token category, keyword, operator, delimiter, and literal form. |
| [error-handling.md](error-handling.md) | Diagnostic format, source positions, recovery behavior, and exit codes. |
| [testing.md](testing.md) | Test suites, fixtures, and what each test covers. |
| [usage.md](usage.md) | CLI and programmatic usage, output format, and examples. |

## Repository layout

```
main.py                  CLI entry point
src/
  tokens.py              TokenType + Token (shared contract)
  scanner.py             Lexer: character reader, main loop, dispatch
  keywords.py            Keyword lookup table
  identifiers.py         scan_identifier_or_keyword()
  symbol_table.py        SymbolTable for identifiers
  literals.py            scan_number() / scan_string()
  operators.py           scan_operator_or_delimiter()
  comments.py            skip_comment()
  errors.py              LexerErrorReporter
tests/                   Unit, CLI, and integration tests plus fixtures
docs/                    This documentation
REPORT.md                Phase 1 report
```

## One-paragraph summary

`main.py` reads a source file and constructs a `Lexer`. The lexer walks the
source one character at a time, tracking `pos`, `line`, and `col`. Its main loop
skips whitespace, delegates comments, identifiers/keywords, numbers, strings,
operators, and delimiters to small helper modules, and appends a `Token` for
each lexeme it recognizes. Identifiers are also inserted into a `SymbolTable`,
which keeps the first occurrence of each name. Lexical errors are recorded and
printed to stderr by a shared `LexerErrorReporter` without aborting the scan.
When the source is exhausted, the lexer appends a final `EOF` token and returns
the complete token list.
