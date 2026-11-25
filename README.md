# Mini Java Compiler

CSCI415 - Compiler Design (Fall 2026). Team project.

A hand-written lexer, recursive-descent parser, and semantic analyzer for a
simplified Java-like language ("Mini Java"). The code is organized as a normal
compiler pipeline — lexer, parser, AST, semantic — and each section is assigned
to one of five members. See [PROJECT.md](PROJECT.md) for the assignments.

> Rule: no ready-made lexer/parser libraries. Everything is written by hand.

## Repo layout

```
main.py                    Single CLI entry point
compiler/
  tokens.py                Shared Token / TokenType contract
  errors.py                Lexer reporter + syntax/semantic error types
  cli.py                   Stage driver: lex -> parse -> tree -> semantic
  lexer/                   Scanner, keywords, identifiers, literals,
                           operators, comments, identifier symbol table
  parser/                  Base navigation, Parser assembly, and grammar
                           sections: declarations, statements, expressions
  ast/                     Parse tree nodes and printer
  semantic/                Scope table and semantic analyzer
inputs/valid/              Valid Mini Java programs
inputs/invalid/            Programs with syntax errors
tests/                     Unit, integration, structure, and pipeline tests
docs/                      Design documentation
PROJECT.md                 Five-member section assignments and workflow
project-specs-phase-1.pdf  Phase 1 specification
Project Guidelines phase2.pdf  Phase 2/3 specification
```

## Sections and owners

| Member | Section |
|---|---|
| 1 | Core and integration: contracts, scanner, parser base/assembly, CLI |
| 2 | Identifiers, keyword table, lexer symbol table, declaration grammar |
| 3 | Literals and statement grammar |
| 4 | Operators and expression grammar |
| 5 | Diagnostics, comments, AST, semantic analysis, tests, report |

Only edit files in your own section. Ask Member 1 before changing shared files.

## Token contract

`compiler/tokens.py` is the single contract for every section. Lexer helpers emit
`lexer.emit(type, lexeme, line, col)`; grammar rules navigate with `self.current`,
`self.match(...)`, `self.expect(...)`, and `self.synchronize()`.

- Keywords: `CLASS PUBLIC PRIVATE PROTECTED STATIC VOID INT FLOAT BOOLEAN CHAR STRING_TYPE IF ELSE WHILE FOR RETURN MAIN`
- `IDENTIFIER`, `NUMBER`, `STRING`, `BOOLEAN_LITERAL` (`true`/`false`)
- Operators: `ASSIGN`, `MATHOP`, `LOGOP`; delimiters: `LPAR RPAR LCUR RCUR LSQU RSQU SEMICOLON COMMA DOT`
- `EOF`, `ERROR`

`BOOLEAN_TYPE` aliases `BOOLEAN`, and `TRUE`/`FALSE` alias `BOOLEAN_LITERAL`.
`Token.col` is canonical; `Token.column` is an alias.

`Parser` inherits the three grammar mixins plus `ParserBase`; mixin methods call
each other through `self`, so no section imports another member's grammar file.

## Phase 2/3 rules to keep

- Syntax errors read `Syntax Error: Expected ';' at line 5, column 12, but found '}'`.
- `ParserBase.synchronize()` stops at `;`, `}`, statement-start keywords, or `EOF`.
- `if/else` binds to the nearest unmatched `if`; expression rules must not be left-recursive.
- Semantic analysis consumes the `ParseTreeNode` tree built in `compiler/ast/`.
- Lexical errors are reported without crashing the parser.

## Run

```bash
python3 main.py --tokens tests/sample1.mj
python3 main.py --tokens inputs/valid/example.minijava
python3 main.py inputs/valid/example.minijava
```

`--tokens` runs the lexer only; `--parse` stops after printing the parse tree.
The default pipeline reports the pending grammar stub on stderr and exits 1
until Member 2 implements `parse_program()`. Usage/read errors exit 2, and
lexical/syntax/semantic errors exit 1.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tests/integration -v
python3 -m pytest -q tests
```

## Deliverables checklist

- [x] Phase 1 lexer complete
- [x] Compiler organized into stages with five member assignments
- [x] Single CLI wiring the full pipeline
- [ ] Grammar methods implemented
- [ ] Parse tree and semantic checks completed
- [ ] Phase 2/3 inputs and report finalized
