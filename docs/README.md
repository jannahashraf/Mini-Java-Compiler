# Mini Java Compiler — Documentation

This documentation covers the hand-written Mini Java compiler: a lexer, a
recursive-descent parser, a parse tree, and semantic analysis. The lexer sections
are described in detail here; see [PROJECT.md](../PROJECT.md) for section
assignments and the full pipeline.

No third-party or ready-made lexer/parser libraries are used. The only runtime
dependency is the Python standard library (Python 3.10+).

## Quick start

```bash
# Scan a sample program; tokens go to stdout.
python3 main.py --tokens tests/sample1.mj

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
main.py                  Single CLI entry point
compiler/
  tokens.py              TokenType + Token (shared contract)
  errors.py              Lexer reporter + syntax/semantic errors
  cli.py                 Stage driver
  lexer/                 scanner.py, keywords.py, identifiers.py,
                         symbol_table.py, literals.py, operators.py, comments.py
  parser/                base.py, parser.py, declarations.py,
                         statements.py, expressions.py
  ast/                   nodes.py, printer.py
  semantic/              symbol_table.py, analyzer.py
tests/                   Unit, CLI, structure, and pipeline tests
docs/                    This documentation
PROJECT.md               Section assignments for the five members
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
the complete token list. `compiler/cli.py` can then feed those tokens to the
parser, print the parse tree, and run semantic analysis.
