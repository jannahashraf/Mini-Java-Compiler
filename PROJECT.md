# Project organization

The code is organized by compiler stage, not by owner. Each stage is a section
of the project; each section has exactly one owner. Only the owner edits the
files listed for that section, so five people can work in parallel without
colliding.

```
source file
    |
    v
compiler/lexer/     tokens + identifier table      lexer symbol table
    |
    v
compiler/parser/    parse tree (ParseTreeNode)
    |
    v
compiler/ast/       tree printing
    |
    v
compiler/semantic/  scope checks
```

`compiler/tokens.py`, `compiler/errors.py` and `compiler/cli.py` are the shared
spine: every section imports them, so changes there need sign-off from Member 1
and a note to the whole team.

## Section assignments

| Member | Section | Files owned | Responsibility |
|---|---|---|---|
| 1 | Core and integration | `main.py`, `compiler/cli.py`, `compiler/tokens.py`, `compiler/lexer/scanner.py`, `compiler/parser/base.py`, `compiler/parser/parser.py` | Token/error contracts, character reader, token navigation, parser assembly, CLI, merges |
| 2 | Identifiers and declarations | `compiler/lexer/keywords.py`, `compiler/lexer/identifiers.py`, `compiler/lexer/symbol_table.py`, `compiler/parser/declarations.py` | Keywords, identifier classification, first-occurrence table, program/class/field/method/type grammar |
| 3 | Literals and statements | `compiler/lexer/literals.py`, `compiler/parser/statements.py` | Numbers, strings, blocks, control flow, returns, local declarations, assignments |
| 4 | Operators and expressions | `compiler/lexer/operators.py`, `compiler/parser/expressions.py` | Longest-match operators/delimiters, precedence chain, calls, arrays, argument lists |
| 5 | Diagnostics, AST and semantics | `compiler/errors.py`, `compiler/lexer/comments.py`, `compiler/ast/*`, `compiler/semantic/*`, `tests/*`, `docs/*`, `REPORT.md` | Comment skipping, diagnostics, parse tree nodes and printing, scopes, semantic checks, tests, report |

## Section boundaries

- The lexer emits `Token` values in source order and ends with `TokenType.EOF`.
  Lexical errors are recorded by `LexerErrorReporter` and never raise.
- The parser receives only non-`ERROR` tokens. Grammar mixins call each other
  through `self`; no section imports another member's grammar file.
- `Parser` combines the three grammar mixins plus `ParserBase`. Error recovery
  uses `ParserBase.synchronize()`.
- Member 5's `compiler/semantic/analyzer.py` consumes the `ParseTreeNode` tree
  produced during parsing; `Token.col` and `Token.column` are the same value.

## Workflow

1. Work on your own section only; every grammar rule is a stub in your own file.
2. Branch from `main`, implement your section, add tests under `tests/`, open a PR.
3. Keep `python3 -m pytest -q tests` green before merging.
4. Run the whole pipeline with `python3 main.py inputs/valid/example.minijava`.
   Use `--tokens` to stop after lexing and `--parse` to stop after tree printing.

## Shared CLI stages

| Command | Stages run |
|---|---|
| `python3 main.py --tokens <file>` | lexer only |
| `python3 main.py --parse <file>` | lexer + parser + tree print |
| `python3 main.py <file>` | lexer + parser + tree print + semantic analysis |

Exit codes: `2` for usage/read errors, `1` for lexical/syntax/semantic errors,
`0` on success.
