# Architecture

The lexer is a single-pass, character-oriented scanner. `main.py` reads the
whole source file into a string, builds one `Lexer`, and asks it for a token
list. All scanning is done by the `Lexer` plus small helper functions that
receive the lexer as their context object. `compiler/cli.py` drives the later
stages when they are implemented.

## Pipeline

```text
source file
    |
    v
main.py  (read UTF-8 text)
    |
    v
Lexer.scan_tokens()                       compiler/lexer/
    |
    +--> whitespace .................. advance()
    +--> // or /* .................... comments.skip_comment()
    +--> letter or _ ................. identifiers.scan_identifier_or_keyword()
    +--> digit ....................... literals.scan_number()
    +--> ' or " ...................... literals.scan_string()
    +--> anything else ............... operators.scan_operator_or_delimiter()
    |
    v
tokens: list[Token]   +   symbol_table: SymbolTable   +   reporter.errors
    |
    v
Parser.parse_program()                    compiler/parser/
    |
    v
ParseTreeNode tree                        compiler/ast/
    |
    v
SemanticAnalyzer.analyze(tree)            compiler/semantic/
```

`--tokens` stops after lexing, `--parse` stops after tree printing, and the
default command runs all stages.

Every successful helper call consumes characters through `Lexer.advance()` and
usually calls `Lexer.emit(...)`. Comments and whitespace produce no token.
Errors are reported through `Lexer.reporter` and scanning continues.

## Module responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Single CLI entry point; delegates to `compiler/cli.py`. |
| `compiler/cli.py` | Parse CLI arguments, run the selected stages, map errors to an exit code. |
| `compiler/tokens.py` | Shared `TokenType` enum and `Token` dataclass. This is the contract between all sections. |
| `compiler/errors.py` | `LexerErrorReporter` plus syntax/semantic error types. |
| `compiler/lexer/scanner.py` | `Lexer` class: source text, cursor position, line/column tracking, token collection, main loop, and dispatch. |
| `compiler/lexer/keywords.py` | `KEYWORDS` dictionary mapping reserved words to token types. |
| `compiler/lexer/identifiers.py` | `scan_identifier_or_keyword()`: consume an identifier, classify it as keyword or `IDENTIFIER`, update the symbol table. |
| `compiler/lexer/symbol_table.py` | `SymbolTable`: first occurrence of each user-defined identifier, keyed by lexeme. |
| `compiler/lexer/literals.py` | `scan_number()` and `scan_string()`: numeric and quoted-string literals, including invalid forms. |
| `compiler/lexer/operators.py` | `scan_operator_or_delimiter()`: longest-match operators, delimiters, and unknown-character errors. |
| `compiler/lexer/comments.py` | `skip_comment()`: `//` line comments and non-nesting `/* ... */` block comments. |
| `compiler/parser/base.py` | Token navigation, `expect()`, and `synchronize()`. |
| `compiler/parser/parser.py` | `Parser`: combines the three grammar mixins with `ParserBase`. |
| `compiler/parser/declarations.py`, `statements.py`, `expressions.py` | Grammar sections (stubs until implemented). |
| `compiler/ast/nodes.py`, `printer.py` | `ParseTreeNode` and indented tree output. |
| `compiler/semantic/symbol_table.py`, `analyzer.py` | Scopes and semantic checks. |

## The `Lexer` as shared context

The helpers are plain functions rather than subclasses or separate scanners.
Each one receives the active `Lexer` and uses the same public surface:

- `lexer.current()` — current character, or `""` at end of input.
- `lexer.peek(offset=1)` — look ahead without consuming.
- `lexer.advance()` — consume one character and update line/column.
- `lexer.at_end()` — whether the cursor is past the last character.
- `lexer.emit(type, lexeme, line, col)` — append a token and return it.
- `lexer.reporter` — shared error reporter.
- `lexer.symbol_table` — shared symbol table.

Because every helper consumes text through `advance()`, source positions remain
consistent even when large comments or strings are skipped.

## Character reader

The reader is index-based:

| Member | Meaning |
|---|---|
| `source` | The complete input string. |
| `pos` | Index of the next character to consume. |
| `line` | 1-based current line. |
| `col` | 1-based current column. |

`advance()` returns the current character, increments `pos`, and updates
position. A `\n` increments `line` and resets `col` to 1; every other character
(including `\r`) increments `col`. `current()` and `peek()` return `""` past the
end so callers can compare without bounds checks.

## Main loop and dispatch

`Lexer.scan_tokens()` repeatedly inspects `current()` and chooses a helper in a
fixed priority order:

1. **Whitespace** (`" \t\r\n"`): consumed one character at a time.
2. **Comments**: only when the current character is `/` and the next is `/` or
   `*`. This check happens before operators so `/` is reserved for division
   unless it starts a comment.
3. **Identifiers/keywords**: `ch.isalpha() or ch == "_"`.
4. **Numbers**: `ch.isdigit()`.
5. **Strings**: current character is `"` or `'`.
6. **Operators/delimiters/everything else**: delegated to the operator helper,
   which also reports unknown characters.

After the loop ends, the lexer appends `Token(TokenType.EOF, "", line, col)`.
`EOF` is always present exactly once, even when errors occurred.

## Scanning algorithms

### Identifiers and keywords

`scan_identifier_or_keyword()` records the start position, consumes a run of
`isalnum()` or `_` characters, then looks up the exact lexeme in `KEYWORDS`.
A hit emits the mapped token type; otherwise it emits `IDENTIFIER` and inserts
the token into the symbol table. Lookup is case-sensitive (`class` is a keyword,
`Class` is an identifier). `main`, `true`, and `false` are handled by the same
table (`MAIN` and `BOOLEAN_LITERAL`).

### Numbers

`scan_number()` consumes digits, then optionally a single decimal point followed
by at least one digit. It then detects invalid continuations:

- a trailing `.` with no following digit → `invalid number literal` error;
- a second `.` → consume the malformed run and report `invalid number literal`;
- a letter or `_` after the digits → consume the whole run and report
  `invalid identifier` (for example `1name` or `2_name`).

Signs are not part of a number: `-5` scans as `MATHOP` then `NUMBER`. Exponents
and hexadecimal forms are not supported.

### Strings

`scan_string()` remembers the opening quote, then consumes until the same quote
character. Single- and double-quoted strings are both accepted. There is no
escape processing; a backslash is ordinary text. If EOF is reached first, the
helper reports `unclosed string literal starting` at the opening position and
emits no token. Newlines inside an unfinished string are still consumed and
advance the line counter.

### Comments

The main loop calls `skip_comment()` only when `/` is followed by `/` or `*`.
The helper records the opening position and consumes the two-character opener.

- `//`: consume until `\r`, `\n`, or EOF. The line ending is left for the main
  loop's whitespace handling.
- `/* ... */`: consume until the first `*/`, including it. Block comments do
  not nest, matching Java. If EOF is reached, report
  `unclosed comment starting` once at the opening position; the cursor remains
  at EOF.

### Operators and delimiters

`scan_operator_or_delimiter()` builds the two-character candidate
`current() + peek()`. It checks the two-character operator table first
(`>=`, `<=`, `==`, `!=`), then the one-character operator table, then the
delimiter table. Anything unmatched is consumed and reported as
`invalid character '<ch>'`. This longest-match order is what makes `>=` one
`LOGOP` instead of `>` followed by `=`.

## Complexity

Scanning is one pass over the input. Each character is consumed at most once and
lookups use dictionaries, so time is O(n) in the source length. Auxiliary space
is O(t) for the token list, O(s) for the symbol table (distinct identifiers), and
O(e) for recorded errors. Helpers use loops, not recursion, so very large
comments and strings do not hit recursion limits.

## Phase boundaries

Phase 1 implements lexical analysis. The parser and semantic stages are
integrated alongside it: `main.py` passes the lexer's token stream to `Parser`,
prints the resulting `ParseTreeNode` tree, and runs `SemanticAnalyzer` over it.
The grammar and analysis methods are stubs to be completed by the team; until
then the CLI reports the pending stub instead of producing a tree. Section
ownership is recorded in [PROJECT.md](../PROJECT.md). See
[data-structures.md](data-structures.md) and
[token-reference.md](token-reference.md) for the shared token shapes.
