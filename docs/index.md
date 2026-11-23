---
myst:
  html_meta:
    "description": "pygments-beancount is a Pygments lexer for Beancount ledgers, for highlighted ledgers in Sphinx, MyST, MkDocs, Pelican and pygmentize."
    "keywords": "Beancount, Pygments, lexer, syntax highlighting, Sphinx, MyST, MkDocs"
---

# pygments-beancount

pygments-beancount is a [Pygments](https://pygments.org/) lexer for [Beancount](https://beancount.github.io/) ledgers.

Install it, and ```` ```beancount ```` code blocks highlight in every tool that highlights code with Pygments.
There is nothing to configure: Pygments finds the lexer through its plugin entry point.

`````{tab-set}
:sync-group: installer

````{tab-item} pip
:sync: pip

```shell
pip install pygments-beancount
```
````

````{tab-item} uv
:sync: uv

Add it to the dependency group that builds your documentation:

```shell
uv add --group docs pygments-beancount
```
````
`````

```beancount
option "operating_currency" "USD"

2026-01-01 open Assets:Bank:Checking  USD
2026-01-01 open Assets:Brokerage      ACME, USD
  institution: "Example Bank"
2026-01-01 open Income:Salary         USD

; Salary arrives on the fifth.
2026-01-05 * "Employer" "Salary for January" #payroll ^payslip-2026-01
  Assets:Bank:Checking     4,250.00 USD
  Income:Salary           -4,250.00 USD

2026-01-12 * "Buy shares"
  Assets:Brokerage            10 ACME {50.25 USD}
  Assets:Bank:Checking   -502.50 USD

2026-01-31 price ACME  51.10 USD
2026-01-31 balance Assets:Bank:Checking  3,747.50 USD
```

Every Beancount block on these pages is highlighted by the lexer this documentation describes.
The {ref}`token reference <reference-tokens>` shows the token each element becomes.

## Names it answers to

| Use | Value |
| --- | --- |
| Code block language | `beancount`, `bean` |
| File names | `*.beancount`, `*.bean` |
| MIME type | `text/x-beancount` |

## Where it works

Any tool that looks lexers up through Pygments:

- Sphinx and MyST, with no change to `conf.py`; see {doc}`how-to/use-in-sphinx`.
- MkDocs, Material for MkDocs, Pelican and other Python-Markdown sites; see {doc}`how-to/use-in-markdown`.
- `pygmentize` and Python code; see {doc}`how-to/use-pygmentize`.

Hugo, Zola and browser-side highlighters such as highlight.js do not use Pygments, so the package has no effect there.

## Where to go next

`````{grid} 1 1 2 2
:gutter: 3

````{grid-item-card} Tutorial
:link: tutorials/highlight-ledgers-in-sphinx
:link-type: doc

New to the package?
Build a small Sphinx site with a highlighted ledger in five minutes.
````

````{grid-item-card} How-to guides
:link: how-to/index
:link-type: doc

Use the lexer in Sphinx, MyST, MkDocs, Pelican, `pygmentize` and Python.
````

````{grid-item-card} Reference
:link: reference/index
:link-type: doc

The token each Beancount element becomes, and the lexer's API.
````

````{grid-item-card} Explanation
:link: explanation/index
:link-type: doc

How the lexer follows Beancount's scanner, and why it never reports an error.
````
`````

```{toctree}
:hidden:
:maxdepth: 2

tutorials/highlight-ledgers-in-sphinx
how-to/index
reference/index
explanation/index
changelog
```
