---
myst:
  html_meta:
    "description": "The older Beancount lexer for Pygments, and why pygments-beancount does not build on it."
    "keywords": "Beancount, Pygments, beancount-pygments-lexer, prior art"
---

(explanation-prior-art)=

# Prior art

## Pygments itself

Pygments has no Beancount lexer.
As of Pygments 2.21, `pygmentize -L lexers` lists none.

## beancount-pygments-lexer

[beancount-pygments-lexer](https://pypi.org/project/beancount-pygments-lexer/) is an older lexer for the same purpose, under the MIT licence.
Its last release, 0.1.2, dates from February 2016 and declares support for Python 3.3 to 3.5.

It predates Beancount v3 and has no tests, so this package does not port its rules: they are written from Beancount's scanner and grammar instead.

It registers the aliases `beancount` and `ledger`, and the file patterns `*.beancount`, `*.ledger` and `*.bean`.
Pygments aliases must be unique, so do not install both packages in one environment: which lexer answers to `beancount` would depend on the order Pygments finds their entry points.
This package does not claim `ledger`, which belongs to the [Ledger](https://ledger-cli.org/) file format.
