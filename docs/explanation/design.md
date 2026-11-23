---
myst:
  html_meta:
    "description": "How the Beancount lexer follows Beancount's scanner, where it is more permissive, and why it never reports an error."
    "keywords": "Beancount, Pygments, RegexLexer, lexer.l, grammar.y, design"
---

(explanation-design)=

# Design

## Follow Beancount's own scanner

Beancount reads a ledger in two steps.
A scanner written for [flex](https://github.com/westes/flex), [`lexer.l`](https://github.com/beancount/beancount/blob/master/beancount/parser/lexer.l), cuts the text into tokens, and a grammar, [`grammar.y`](https://github.com/beancount/beancount/blob/master/beancount/parser/grammar.y), decides where each token may appear.

The lexer's token patterns are the scanner's patterns, translated to Python regular expressions, with a comment in the source that names each one.
Where the scanner leaves a decision to the grammar, the lexer uses context.
A single capital letter is the clearest case: the scanner returns it as one token, and the grammar reads it as a flag after a date or at the start of a posting, and as a currency anywhere else.

Some consequences of following the scanner rather than the documentation:

- A metadata key has at least two characters, `[a-z][a-zA-Z0-9\-_]+`.
  A one-letter key is not a key.
- A date accepts any number of digits for the month and the day, and either `-` or `/` between them.
- A line that starts with `#` followed by tag characters is a tag, not an ignored line, because flex prefers the longer match.
  A line that starts with `#` and a space is ignored.
- `TRUE`, `FALSE` and `NULL` are constants only when no longer currency can be read: `TRUEUSD` is a currency.

## More permissive than Beancount

The lexer highlights; it does not validate.
It accepts some input that Beancount would reject after scanning:

- Any four-digit year, where the scanner limits years to 1700 to 2099.
- Any non-ASCII character in an account name.
  Beancount's scanner accepts them too, but its parser then requires each component to start with an uppercase letter or a digit, so `Ativos:日本` is highlighted but not valid.
- Dates such as `2026-13-45`, unbalanced transactions and unknown accounts.

## Never report an error

Pygments marks input that no rule matches with an `Error` token.
Sphinx, when a lexer returns one, gives up on the whole block and shows it without colours, with a warning.

Documentation is full of snippets that are not valid ledgers: `...` for omitted postings, `<amount>` for a value to fill in.
The lexer therefore ends its rules with a fallback that turns any run of unrecognized characters into plain `Text`.
The other rules cover every character the fallback leaves out, so every character of the input belongs to some token and no `Error` token is ever produced.

The test suite checks this on every example and every test input.
It also checks the opposite: a valid ledger produces no `Text` token, so the fallback cannot hide a gap in the rules.

## States

Beancount is line-oriented, so the lexer needs context in three places only.

`root`
:   The rules for the first column of a line: hashbang, org-mode headings, ignored lines, a date that opens a directive, directives without a date, and the flag at the start of a posting.
    Everything else falls through to `values`.

`directive`
:   The token right after a date: a directive keyword or a transaction flag.
    Every rule leaves the state, so it lasts for one token.

`values`
:   Every other token, in an order that matters, because the first rule that matches wins: dates before numbers, constants before currencies, accounts before currencies and metadata keys, the futures form of a currency before the division operator.

`string`
:   The inside of a string.
    Strings may span lines, and a state avoids the slow backtracking that one regular expression could suffer on an unterminated string.

The test suite includes pathological input, such as thousands of capital letters or backslashes in an unterminated string, and checks that each one lexes quickly.

## No dependency on Beancount

The lexer imports Pygments only.
Highlighting a ledger in documentation should not require installing Beancount, with its compiled parser, in the environment that builds the documentation.
The test suite uses Beancount, as a development dependency, to check that its example ledgers are valid.
