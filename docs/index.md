---
myst:
  html_meta:
    "description": "pygments-beancount is a Pygments lexer for Beancount ledgers, for highlighted ledgers in Sphinx and MyST documentation."
    "keywords": "Beancount, Pygments, lexer, syntax highlighting, Sphinx, MyST"
---

# pygments-beancount

pygments-beancount is a [Pygments](https://pygments.org/) lexer for [Beancount](https://beancount.github.io/) ledgers.

Install it, and ```` ```beancount ```` code blocks highlight in Sphinx and MyST documentation, in `pygmentize`, and anywhere else Pygments is used.
There is nothing to configure: Pygments finds the lexer through its plugin entry point.

```beancount
2026-01-05 * "Employer" "Salary for January" #payroll ^payslip-2026-01
  Assets:Bank:Checking     4,250.00 USD
  Income:Salary           -4,250.00 USD

2026-01-31 balance Assets:Bank:Checking  4,250.00 USD
```

Every Beancount block on these pages is highlighted by the lexer this documentation describes.

## Where to go next

`````{grid} 1 1 2 2
:gutter: 3

````{grid-item-card} Tutorial
:link: tutorials/highlight-ledgers-in-sphinx
:link-type: doc

New to the package?
Add highlighted ledgers to a Sphinx project in five minutes.
````

````{grid-item-card} How-to guides
:link: how-to/index
:link-type: doc

Use every MyST and Sphinx form, `pygmentize` and the Python API.
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
