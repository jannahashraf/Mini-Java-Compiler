# Data Structures

The scanner uses a small set of types: one enum for token categories, one token
record, one central mutable lexer object, one symbol table, one error collector,
and several constant lookup dictionaries.

## `TokenType` (enum)

`compiler/tokens.py` defines `TokenType` with string values. The enum is the
shared contract for all compiler sections: every scanner helper and parser rule
refers to these names, so adding, renaming, or removing a member affects the
whole project.

Members grouped by purpose:

| Group | Members |
|---|---|
| Keywords | `CLASS`, `PUBLIC`, `PRIVATE`, `PROTECTED`, `STATIC`, `VOID`, `INT`, `FLOAT`, `BOOLEAN`, `BOOLEAN_TYPE`, `CHAR`, `STRING_TYPE`, `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`, `MAIN` |
| Identifiers and literals | `IDENTIFIER`, `NUMBER`, `STRING`, `BOOLEAN_LITERAL`, `TRUE`, `FALSE` |
| Operators | `ASSIGN`, `MATHOP`, `LOGOP` |
| Delimiters | `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT` |
| Bookkeeping | `EOF`, `ERROR` |

`PRIVATE`, `PROTECTED`, `BOOLEAN_TYPE`, `TRUE`, and `FALSE` are part of the
Phase 2/3 grammar contract. `BOOLEAN_TYPE` aliases `BOOLEAN`; `TRUE` and `FALSE`
alias `BOOLEAN_LITERAL`. The scanner does not emit `PRIVATE` or `PROTECTED`.

`ERROR` exists in the contract but the current scanner does not emit it: errors
are reported as diagnostics instead. `EOF` is always emitted as the final token.

## `Token` (dataclass)

```python
@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    col: int

    @property
    def column(self) -> int:
        return self.col
```

| Field | Type | Meaning |
|---|---|---|
| `type` | `TokenType` | Classified category. |
| `lexeme` | `str` | Exact source text that produced the token (for `EOF`, `""`). |
| `line` | `int` | 1-based line of the token's first character. |
| `col` | `int` | 1-based column of the token's first character. |

`column` is a read-only alias of `col` for Phase 2/3 code. Because this is a
regular dataclass, equality compares the four stored fields and the generated
`repr` is available for debugging. `str(token)` is the CLI output format; see
`Token.__str__` in `compiler/tokens.py` for its current shape.

For string tokens the lexeme retains the quotes (`"Ali"`, `'A'`). For numbers it
is the original spelling (`85.5`, not a parsed float).

## `Lexer` (central state)

Defined in `compiler/lexer/scanner.py`. One instance scans one source string.

| Attribute | Type | Purpose |
|---|---|---|
| `source` | `str` | Entire input text. |
| `pos` | `int` | Index of the next character to read. |
| `line` | `int` | Current 1-based line. Starts at 1. |
| `col` | `int` | Current 1-based column. Starts at 1. |
| `reporter` | `LexerErrorReporter` | Collects and prints diagnostics. |
| `symbol_table` | `SymbolTable` | First occurrences of user identifiers. |
| `tokens` | `list[Token]` | Tokens emitted during the scan. |

Key methods:

| Method | Description |
|---|---|
| `current() -> str` | Returns `source[pos]`, or `""` at/after end. |
| `peek(offset=1) -> str` | Returns `source[pos + offset]`, or `""` out of range. |
| `advance() -> str` | Consumes and returns the current character; updates `line`/`col`. |
| `at_end() -> bool` | `pos >= len(source)`. |
| `emit(type, lexeme, line, col) -> Token` | Constructs a `Token`, appends it to `tokens`, and returns it. |
| `scan_tokens() -> list[Token]` | Runs the main loop and appends `EOF`. |

Invariants and behavior:

- `0 <= pos <= len(source)`.
- `line` starts at 1; `col` starts at 1 for each line.
- `advance()` on `\n` increments `line` and resets `col = 1`; all other
  characters increment `col`. `\r` therefore does not start a new line itself.
- `scan_tokens()` appends exactly one `EOF` token at the end, directly to
  `tokens` rather than through `emit()`. Repeated calls would append additional
  `EOF` tokens because the cursor is already at the end; callers use it once.
- `tokens`, `reporter.errors`, and `symbol_table` are all readable after the
  scan for tests or later compiler phases.

## `SymbolTable`

Defined in `compiler/lexer/symbol_table.py`. It stores user-defined identifier names, not
keywords or `main`/`true`/`false`.

```python
class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, Token] = {}

    def insert(self, token: Token) -> None: ...
    def lookup(self, name: str) -> Token | None: ...
    def __len__(self) -> int: ...
```

| Member | Behavior |
|---|---|
| `_symbols` | Private `dict[str, Token]` keyed by lexeme. |
| `insert(token)` | Stores only the first token for each lexeme; later occurrences are ignored. |
| `lookup(name)` | Returns the stored first token, or `None`. |
| `len(table)` | Number of distinct names. |

Design notes:

- It is a flat, single-scope table. There is no nesting, shadowing, or type
  information yet; those belong to later phases.
- The stored `Token` includes the location of the first occurrence, which is why
  duplicates are deliberately not overwritten.
- Dictionary insertion order preserves first-seen order if later phases need to
  enumerate symbols.

## `LexerErrorReporter`

Defined in `compiler/errors.py`.

```python
class LexerErrorReporter:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, message: str, line: int, col: int) -> None: ...
    def has_errors(self) -> bool: ...
```

| Member | Behavior |
|---|---|
| `errors` | Formatted diagnostic strings in encounter order. |
| `error(...)` | Formats `Error: <message> at line <line>, column <col>.`, appends it, and prints it to stderr immediately. |
| `has_errors()` | `True` when `errors` is non-empty. |

The reporter does not raise exceptions. It is normally one instance per
`Lexer`, so separate scans do not share errors. See
[error-handling.md](error-handling.md) for the full contract.

## Lookup tables

All lookup tables are module-level constants, created once at import time.

### `KEYWORDS`

`dict[str, TokenType]` in `compiler/lexer/keywords.py`, keyed by exact, case-sensitive
lexeme. It also maps `main` to `MAIN` and `true`/`false` to
`BOOLEAN_LITERAL`. See [token-reference.md](token-reference.md) for the complete
list.

### Operator and delimiter tables

`compiler/lexer/operators.py` defines three dictionaries:

| Constant | Key type | Value | Checked |
|---|---|---|---|
| `TWO_CHAR_OPERATORS` | `str` (2 chars) | `LOGOP` for `>=`, `<=`, `==`, `!=` | First |
| `ONE_CHAR_OPERATORS` | `str` (1 char) | `ASSIGN` for `=`, `MATHOP` for `+ - * / %`, `LOGOP` for `> < !` | Second |
| `DELIMITERS` | `str` (1 char) | Parentheses, braces, brackets, `;`, `,`, `.` | Third |

Checking two-character operators first implements longest match.

## How the structures fit together

```text
Lexer.source ──(reader)──> current/peek/advance
                                |
                                v
                    helper consumes characters
                                |
                                v
                    Lexer.emit(type, lexeme, line, col)
                                |
                                +--> Lexer.tokens : list[Token]
                                |
                                +--> Lexer.symbol_table (identifiers only)

helper on bad input ──> Lexer.reporter.error(...)
                                |
                                +--> reporter.errors : list[str] -> stderr
```

The CLI prints each `Token` with `str(token)` and uses
`reporter.has_errors()` to choose the process exit status.
