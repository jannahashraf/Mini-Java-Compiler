# Mini Java Compiler - Phase 1: Lexical Analyzer

CSCI415 - Compiler Design (Fall 2026). Team project.

A lexical analyzer (scanner) for a simplified Java-like language ("Mini Java").
It reads source code character by character, groups characters into **tokens**,
classifies them, and builds a **symbol table**.

> Rule: no ready-made lexer/parser libraries. Everything is written by hand.

## Repo layout

```
main.py                  CLI entry point (Member 1)
REPORT.md                Phase 1 report
src/
  tokens.py              TokenType + Token  (Member 1 - shared contract)
  scanner.py             Lexer: reader + main loop + dispatch  (Member 1)
  keywords.py            Keyword table  (Member 2)
  identifiers.py         scan_identifier_or_keyword()  (Member 2)
  symbol_table.py        SymbolTable  (Member 2)
  literals.py            scan_number() / scan_string()  (Member 3)
  operators.py           scan_operator_or_delimiter()  (Member 4)
  comments.py            skip_comment()  (Member 5)
  errors.py              LexerErrorReporter  (Member 5)
tests/
  README.md              how to run the tests and what each fixture covers
  sample1.mj             sample Mini Java program
  expected_output.txt    expected token stream for sample1.mj
  sample_programs.mj     three Mini Java programs covering every token category
  comments_only.mj       comment-only smoke test
  sample_errors.mj       mixed-error example
  fixtures/errors/       one negative input per required error kind
  test_comments.py       comment and CLI tests
  test_errors.py         error-reporter tests
  integration/           whole-lexer acceptance tests
```

## Who owns what

| Member | Files | Task |
|---|---|---|
| 1 | `main.py`, `src/scanner.py`, `src/tokens.py` | Core reader, main loop, token/symbol-table contract, integration, merges |
| 2 | `src/keywords.py`, `src/identifiers.py`, `src/symbol_table.py` | Keywords, identifiers, `main`, `true`/`false`, symbol table |
| 3 | `src/literals.py` | `NUMBER` (int/float), `STRING`, unclosed-string error |
| 4 | `src/operators.py` | Longest-match operators, delimiters, unknown-symbol error |
| 5 | `src/comments.py`, `src/errors.py`, `tests/` | Comments + unterminated-comment error, error format, tests, report |

Only edit files you own. If you need a change in `src/tokens.py`, ask Member 1.

## Token contract

Shared token types live in `src/tokens.py`. Key names:

- Keywords: `CLASS PUBLIC STATIC VOID INT FLOAT BOOLEAN CHAR STRING_TYPE IF ELSE WHILE FOR RETURN MAIN`
- `IDENTIFIER`, `NUMBER`, `STRING`, `BOOLEAN_LITERAL` (`true`/`false`)
- Operators: `ASSIGN` (`=`), `MATHOP` (`+ - * / %`), `LOGOP` (`> < >= <= == != !`)
- Delimiters: `LPAR RPAR LCUR RCUR LSQU RSQU SEMICOLON COMMA DOT`
- `EOF`, `ERROR`

Helpers must emit tokens with `lexer.emit(type, lexeme, line, col)` and report
errors with `lexer.reporter.error(msg, line, col)`.

## Run

```bash
python3 main.py tests/sample1.mj
```

Run the test suites:

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tests/integration -v
```

## Deliverables checklist 

- [x] Source code (all modules implemented, sample passes)
- [x] `tests/` input file with several Mini Java programs
- [x] 1-2 page report: tokens implemented, error handling, challenges
