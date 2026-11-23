---
myst:
  html_meta:
    "description": "The Pygments token type, and HTML class, that each Beancount element becomes."
    "keywords": "Beancount, Pygments, tokens, CSS classes, styles"
---

(reference-tokens)=

# Tokens

The lexer uses only the standard Pygments [token types](https://pygments.org/docs/tokens/), so every Pygments style, and every Sphinx theme, colours a ledger without custom CSS.
The CSS class is the one the HTML formatter writes on each `<span>`; a style that sets a colour for it colours that element.

## Mapping

| Beancount element | Example | Token type | CSS class |
| --- | --- | --- | --- |
| Comment | `; checked`{l=beancount} | `Comment.Single` | `c1` |
| Hashbang, on the first line | `#!/usr/bin/env bean-check` | `Comment.Hashbang` | `ch` |
| Org-mode heading: `*` in the first column | `* Accounts` | `Generic.Heading` | `gh` |
| Other ignored lines: `:`, `#`, `!`, `&`, `?` or `%` in the first column | `:PROPERTIES:` | `Comment.Special` | `cs` |
| Date | `2026-01-31`{l=beancount} | `Literal.Date` | `ld` |
| Directive keyword after a date, `txn`, the `*` flag | `balance`, `txn`, `*` | `Keyword` | `k` |
| Other flags: `!`, `&`, `#`, `?`, `%` or a capital letter | `!` | `Keyword.Pseudo` | `kp` |
| Directive without a date | `option`, `plugin`, `include`, `pushtag`, `poptag`, `pushmeta`, `popmeta` | `Keyword.Namespace` | `kn` |
| Boolean and null | `TRUE`{l=beancount}, `FALSE`{l=beancount}, `NULL`{l=beancount} | `Keyword.Constant` | `kc` |
| Account, as one token | `Assets:Bank:Checking`{l=beancount} | `Name.Namespace` | `nn` |
| Currency or commodity | `USD`{l=beancount}, `/ESM24`{l=beancount} | `Name.Constant` | `no` |
| Metadata key; the colon after it is punctuation | `receipt:`{l=beancount} | `Name.Attribute` | `na` |
| Tag | `#trip-2026`{l=beancount} | `Name.Tag` | `nt` |
| Link | `^invoice-42`{l=beancount} | `Name.Label` | `nl` |
| String, quotes included | `"Payee"`{l=beancount} | `Literal.String.Double` | `s2` |
| Escape in a string | `\"` | `Literal.String.Escape` | `se` |
| Number with a decimal point | `1,234.56`{l=beancount} | `Literal.Number.Float` | `mf` |
| Number without one | `42`{l=beancount} | `Literal.Number.Integer` | `mi` |
| Operators: price, tolerance, arithmetic, `#` in a cost | `@`, `@@`, `~`, `+`, `-`, `*`, `/`, `#` | `Operator` | `o` |
| Punctuation | `{`, `}`, `{{`, `}}`, `(`, `)`, `,`, `\|`, `:` | `Punctuation` | `p` |
| Spaces, tabs and newlines | | `Text.Whitespace` | `w` |
| Anything not recognized, such as `...` | `...` | `Text` | none |

## Choices worth knowing

The whole account is one token.
A style cannot colour `Assets` differently from `Bank:Checking`, but every account reads as one unit, and the lexer stays simple.

Flags other than `*` are `Keyword.Pseudo`, not `Keyword`.
Most styles colour the two differently, which sets pending entries (`!`) apart from cleared ones (`*`).

A single capital letter followed by a space is a flag where Beancount's grammar expects one, after a date or at the start of a posting, and a one-letter currency everywhere else.

```beancount
2026-01-09 P "Broker" "A transaction with the P flag"
  Assets:Broker   2 V {310.00 USD}
  Assets:Cash
```

## Every element in one ledger

The test suite uses this synthetic ledger to check that every element above is recognized.
Beancount's own parser accepts it.

```{literalinclude} ../../tests/examples/full.beancount
:language: beancount
```
