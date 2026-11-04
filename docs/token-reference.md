# Token Reference

This is the complete token vocabulary produced by the Phase 1 lexer. Token
names come from `TokenType` in `src/tokens.py`.

## Token categories

| Category | Token types | Lexemes |
|---|---|---|
| Keywords | `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`, `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`, `MAIN` | See keyword table below. |
| Identifier | `IDENTIFIER` | Names starting with a letter or `_`, continuing with letters, digits, or `_`. |
| Numeric literal | `NUMBER` | Integers such as `0`, `20`; floats such as `25.5`. |
| String literal | `STRING` | Values in single or double quotes, e.g. `"Ali"`, `'A'`, `""`. |
| Boolean literal | `BOOLEAN_LITERAL` | `true`, `false`. |
| Assignment | `ASSIGN` | `=`. |
| Arithmetic | `MATHOP` | `+`, `-`, `*`, `/`, `%`. |
| Comparison/logical | `LOGOP` | `>`, `<`, `>=`, `<=`, `==`, `!=`, `!`. |
| Delimiters | `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT` | `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `.`. |
| Bookkeeping | `EOF` | Empty lexeme `""`; always the final token. |
| Bookkeeping | `ERROR` | Reserved in the contract; not emitted by the current scanner. |

## Keywords

Mini Java is case-sensitive and keyword lookup is exact. The mapping lives in
`src/keywords.py`.

| Lexeme | Token type |
|---|---|
| `class` | `CLASS` |
| `public` | `PUBLIC` |
| `static` | `STATIC` |
| `void` | `VOID` |
| `int` | `INT` |
| `float` | `FLOAT` |
| `boolean` | `BOOLEAN` |
| `char` | `CHAR` |
| `String` | `STRING_TYPE` |
| `if` | `IF` |
| `else` | `ELSE` |
| `while` | `WHILE` |
| `for` | `FOR` |
| `return` | `RETURN` |
| `main` | `MAIN` |
| `true` | `BOOLEAN_LITERAL` |
| `false` | `BOOLEAN_LITERAL` |

Consequences of case sensitivity:

- `class` is `CLASS`, but `Class` is `IDENTIFIER`.
- `String` is `STRING_TYPE`, but `string` is `IDENTIFIER`.
- `main` is `MAIN`, but `Main` is `IDENTIFIER`.
- `true`/`false` are `BOOLEAN_LITERAL`, but `True`/`FALSE` are `IDENTIFIER`.
- The type keyword `boolean` (`BOOLEAN`) is distinct from the values
  `true`/`false` (`BOOLEAN_LITERAL`).

## Identifiers

An identifier:

- starts with a letter (`str.isalpha()`) or underscore `_`;
- continues with letters, digits (`str.isalnum()`), or `_`;
- is not a reserved word.

Examples: `age`, `studentName`, `x1`, `_count`, `total_marks`.

The implementation uses Python's Unicode-aware `isalpha`/`isalnum` predicates,
so non-ASCII letters are accepted even though the language is intended for
ASCII identifiers. Only lexemes classified as `IDENTIFIER` are added to the
symbol table.

## Numeric literals

`NUMBER` covers integers and simple decimal floats:

- `0`, `10`, `2026` — integers;
- `25.5`, `0.5` — floats with digits on both sides of the dot.

Not supported (and reported as lexical errors):

- a trailing dot such as `5.` → `invalid number literal`;
- more than one dot such as `1.2.3` → `invalid number literal`;
- a digit-run followed by a letter or `_` such as `1name` or `2_name` →
  `invalid identifier`.

The lexeme is the original source spelling; numbers are not converted to
`int`/`float` at this phase. A leading `-` or `+` is a separate operator token,
so `-5` is `MATHOP` followed by `NUMBER`. Exponents, hex, underscores in
numerals, and suffixes are not part of the language.

Note that `.5` begins with `.`, which dispatches to the delimiter helper, so it
becomes `DOT` followed by `NUMBER` rather than a single float.

## String literals

`STRING` accepts either delimiter style:

- double-quoted: `"Hello"`, `"Ali"`, `""`;
- single-quoted: `'A'`, `'//'`, `''`.

The lexeme includes the surrounding quotes. There is no escape processing: a
backslash is an ordinary character and cannot escape the closing quote. A string
may span lines. If EOF is reached before the matching quote, the scanner reports
`unclosed string literal starting` at the opening quote and emits no `STRING`
token.

Comment markers inside strings are literal text, e.g. `"http://host/*path*/"`
is one `STRING` token.

## Operators

Operators use longest match: two-character operators are tested before
one-character operators.

| Lexeme | Token type | Notes |
|---|---|---|
| `>=` | `LOGOP` | Two-character match. |
| `<=` | `LOGOP` | Two-character match. |
| `==` | `LOGOP` | Two-character match. |
| `!=` | `LOGOP` | Two-character match. |
| `>` | `LOGOP` | Single character. |
| `<` | `LOGOP` | Single character. |
| `!` | `LOGOP` | Single character. |
| `=` | `ASSIGN` | Assignment only; `==` is comparison. |
| `+` | `MATHOP` | |
| `-` | `MATHOP` | |
| `*` | `MATHOP` | |
| `/` | `MATHOP` | Division, unless followed by `/` or `*` for a comment. |
| `%` | `MATHOP` | |

Compound assignment (`+=`), increment/decrement (`++`, `--`), and bitwise
operators are not defined; they would scan as separate tokens or errors.

## Delimiters

| Lexeme | Token type |
|---|---|
| `(` | `LPAR` |
| `)` | `RPAR` |
| `{` | `LCUR` |
| `}` | `RCUR` |
| `[` | `LSQU` |
| `]` | `RSQU` |
| `;` | `SEMICOLON` |
| `,` | `COMMA` |
| `.` | `DOT` |

## Whitespace and comments

Whitespace (`space`, `\t`, `\r`, `\n`) is skipped and produces no token.

Comments produce no token:

- `// ...` until end of line or EOF;
- `/* ... */` until the first `*/`; block comments do not nest.

An unterminated block comment produces a diagnostic at its opening position, not
a token. See [error-handling.md](error-handling.md).

## End of file and errors

- `EOF` has lexeme `""` and is appended exactly once after scanning. Its
  `line`/`col` are the position after the last consumed character.
- `ERROR` is declared for the contract but unused. Lexical problems are reported
  through `LexerErrorReporter` and the scanner continues; the offending text
  generally produces no token.

## Example

For `tests/sample1.mj`, the first tokens are:

```text
Lexeme: class, Token: CLASS
Lexeme: Student, Token: IDENTIFIER
Lexeme: {, Token: LCUR
Lexeme: public, Token: PUBLIC
...
Lexeme: , Token: EOF
```

The full golden stream is in `tests/expected_output.txt`; the integration suite
compares it against the real scanner.
