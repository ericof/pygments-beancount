---
myst:
  html_meta:
    "description": "Every way to show a highlighted Beancount ledger in Sphinx and MyST."
    "keywords": "Beancount, Sphinx, MyST, code-block, literalinclude, inline code"
---

(how-to-use-in-sphinx)=

# Use the lexer in Sphinx and MyST

This guide shows each way to put a highlighted ledger on a Sphinx page written with [MyST](https://myst-parser.readthedocs.io/en/latest/syntax/code_and_apis.html).

Install pygments-beancount in the environment that builds the documentation first.
With uv, add it to the dependency group that builds the docs, and pin it, because the languages Sphinx knows depend on what that environment has installed:

```shell
uv add --group docs pygments-beancount
```

## Fenced code blocks

Use `beancount`, or its short alias `bean`, as the language:

````markdown
```beancount
2026-01-01 open Assets:Cash USD
```
````

```beancount
2026-01-01 open Assets:Cash USD
```

## Code blocks with options

The `code-block` directive takes the options Sphinx defines for [showing code examples](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block), such as a caption, line numbers and emphasized lines:

````markdown
```{code-block} beancount
:caption: A transaction with a pending posting
:linenos:
:emphasize-lines: 3

2026-01-06 * "Grocery store" "Weekly shopping"
  Expenses:Groceries     74.00 USD
  ! Assets:Cash
```
````

```{code-block} beancount
:caption: A transaction with a pending posting
:linenos:
:emphasize-lines: 3

2026-01-06 * "Grocery store" "Weekly shopping"
  Expenses:Groceries     74.00 USD
  ! Assets:Cash
```

## Include a ledger file

`literalinclude` shows a file from the documentation source tree.
Give it the language explicitly, with its usual options to show part of the file:

````markdown
```{literalinclude} ../../tests/examples/orgmode.beancount
:language: beancount
:lines: 9-15
```
````

```{literalinclude} ../../tests/examples/orgmode.beancount
:language: beancount
:lines: 9-15
```

## Inline code

With the `attrs_inline` MyST extension enabled in `conf.py`, set the language of an inline code span with `l`:

```python
myst_enable_extensions = ["attrs_inline"]
```

```markdown
Move the money to `Assets:Bank:Savings`{l=beancount} before the `balance`{l=beancount} check.
```

Move the money to `Assets:Bank:Savings`{l=beancount} before the `balance`{l=beancount} check.

## Number the lines of every Beancount block

`myst_number_code_blocks` adds line numbers to every fenced block in the languages it lists.
This documentation uses it, which is why the blocks on these pages are numbered:

```python
myst_number_code_blocks = ["beancount"]
```

## Make Beancount the default language

If most blocks in a project are ledgers, make Beancount the language of every block that does not name one:

```python
highlight_language = "beancount"
```

## Placeholders and invalid snippets

Documentation often shortens a ledger with `...` or a placeholder such as `<amount>`.
The lexer highlights such snippets anyway: it shows what it does not recognize as plain text instead of reporting an error, so Sphinx keeps the colours of the rest of the block.

```beancount
2026-01-02 * "Payee" "Narration"
  Assets:Investments:Cash   <amount> USD
  ...
```

You do not need the `:force:` option of `code-block`, which tells Sphinx to ignore errors from a lexer.
See {doc}`/explanation/design` for why the lexer never reports one.

## Fail the build on a block that cannot be highlighted

Build with warnings as errors, so a block in a language Pygments does not know fails the build instead of losing its colours:

```shell
sphinx-build -W -b html docs docs/_build/html
```
