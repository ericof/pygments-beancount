---
myst:
  html_meta:
    "description": "Add highlighted Beancount ledgers to a Sphinx project written in Markdown with MyST."
    "keywords": "Beancount, Sphinx, MyST, tutorial, syntax highlighting"
---

(tutorial-highlight-ledgers)=

# Highlight ledgers in Sphinx

In this tutorial you create a small Sphinx project written in Markdown, and highlight a Beancount ledger in it.
It takes about five minutes.

You need Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

## Create the project

Create a folder for the project, and add Sphinx, MyST-Parser and pygments-beancount to it:

```shell
mkdir ledger-docs
cd ledger-docs
uv init --bare
uv add sphinx myst-parser pygments-beancount
```

## Configure Sphinx

Create `conf.py` with the smallest configuration that reads Markdown:

```python
project = "Ledger docs"
extensions = ["myst_parser"]
```

Nothing in it mentions Beancount.
Installing pygments-beancount registers the lexer with Pygments, and Sphinx asks Pygments for it.

## Write a page

Create `index.md` with a fenced code block whose language is `beancount`:

````markdown
# My ledger

```beancount
2026-01-01 open Assets:Bank:Checking USD
2026-01-01 open Expenses:Groceries   USD

2026-01-06 * "Grocery store" "Weekly shopping"
  Expenses:Groceries     74.00 USD
  Assets:Bank:Checking
```
````

## Build it

Build the HTML with warnings as errors:

```shell
uv run sphinx-build -W -b html . _build/html
```

Open `_build/html/index.html` in a browser.
The ledger looks like this:

```beancount
2026-01-01 open Assets:Bank:Checking USD
2026-01-01 open Expenses:Groceries   USD

2026-01-06 * "Grocery store" "Weekly shopping"
  Expenses:Groceries     74.00 USD
  Assets:Bank:Checking
```

Dates, keywords, accounts, amounts and currencies each have their own colour, taken from the theme's Pygments style.

## What you learned

- Installing pygments-beancount is the whole integration: no Sphinx extension and no change to `conf.py`.
- `beancount` is the language name for code blocks; `bean` works too.
- Building with `-W` makes Sphinx fail if a block cannot be highlighted.

## Next steps

- {doc}`/how-to/use-in-sphinx` shows every other way to show a ledger: directives with options, included files, inline code and line numbers.
- {doc}`/reference/tokens` lists the token each Beancount element becomes.
