# pygments-beancount

A [Pygments](https://pygments.org/) lexer for [Beancount](https://beancount.github.io/) ledgers.

Install it, and ```` ```beancount ```` code blocks highlight in Sphinx and MyST, MkDocs and Pelican, `pygmentize`, and every other tool that highlights code with Pygments.
There is nothing to configure: Pygments finds the lexer through its plugin entry point.

[![CI](https://github.com/ericof/pygments-beancount/actions/workflows/ci.yml/badge.svg)](https://github.com/ericof/pygments-beancount/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://ericof.github.io/pygments-beancount/)
[![License: BSD-2-Clause](https://img.shields.io/badge/license-BSD--2--Clause-green)](https://github.com/ericof/pygments-beancount/blob/main/LICENSE)

## Features

- Covers the full Beancount v3 syntax: every directive, flags, postings, costs (`{}`, `{{}}`, `{502.12 # 9.95 USD}`), prices, tolerances, arithmetic, metadata, tags, links, `pushtag` and `pushmeta`, org-mode headings and ignored lines.
- Its token patterns follow Beancount's own scanner, `lexer.l`.
- Never emits an `Error` token: snippets with placeholders such as `...` still highlight, and Sphinx never drops a block's colours.
- Uses only standard token types, so every Pygments style colours it.
- Depends on Pygments only; it never imports Beancount.

## Installation

The package needs Python 3.11 or later and Pygments 2.13 or later.

```shell
pip install pygments-beancount
```

With uv, add it to the dependency group that builds your documentation:

```shell
uv add --group docs pygments-beancount
```

Do not install it together with the older, unmaintained `beancount-pygments-lexer`: both register the `beancount` alias, so which one Pygments uses depends on the order it finds their entry points.

## Usage

### In Sphinx with MyST

Install the package in the environment that builds the documentation, then use `beancount` (or `bean`) as the language of a code block.
No change to `conf.py` is needed.

````markdown
```beancount
2026-01-05 * "Employer" "Salary for January" #payroll
  Assets:Bank:Checking   4,250.00 USD
  Income:Salary
```
````

Directives work too, with all their options:

````markdown
```{literalinclude} ledger/main.beancount
:language: beancount
:lines: 1-20
```
````

### In MkDocs and other Python-Markdown sites

Python-Markdown highlights through Pygments with the `codehilite` or `pymdownx.highlight` extension.
Pelican enables `codehilite` by default, and Material for MkDocs highlights through `pymdownx.highlight`, so in both ```` ```beancount ```` blocks highlight once the package is installed.
The default `mkdocs` theme uses highlight.js instead; the [Markdown guide](https://ericof.github.io/pygments-beancount/how-to/use-in-markdown.html) shows how to switch it to Pygments.

Hugo, Zola and browser-side highlighters do not use Pygments, so the package has no effect there.

### On the command line

```shell
pygmentize -l beancount -f terminal256 main.beancount
pygmentize -f html -O full -o main.html main.beancount
```

### From Python

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter

from pygments_beancount import BeancountLexer

html = highlight('2026-01-01 open Assets:Cash USD\n', BeancountLexer(), HtmlFormatter())
```

## Documentation

The full documentation, including the token reference and how-to guides, is at <https://ericof.github.io/pygments-beancount/>.

## Development

The project uses [uv](https://docs.astral.sh/uv/) and a Makefile:

```shell
make install   # create the virtualenv
make check     # ruff, mypy --strict and pytest
make docs      # build the documentation; warnings are errors
```

See the [contributing guide](https://ericof.github.io/pygments-beancount/how-to/contribute.html) for the rest.

## License

BSD 2-Clause, the same licence as Pygments.
See [LICENSE](https://github.com/ericof/pygments-beancount/blob/main/LICENSE).
