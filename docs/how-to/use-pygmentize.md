---
myst:
  html_meta:
    "description": "Highlight Beancount ledgers on the command line with pygmentize, and from Python."
    "keywords": "Beancount, pygmentize, Pygments, Python, HTML, terminal"
---

(how-to-use-pygmentize)=

# Highlight ledgers outside Sphinx

This guide shows how to use the lexer with `pygmentize` and from Python code.

## Check that Pygments finds the lexer

```shell
pygmentize -L lexers | grep -A1 -i beancount
```

The output names the aliases and file patterns:

```text
* beancount, bean:
    Beancount (filenames *.beancount, *.bean)
```

## On the command line

`pygmentize` picks the lexer from the file name, so `-l` is only needed for other names or for standard input:

```shell
# In a terminal with 256 colours
pygmentize -f terminal256 main.beancount

# A standalone HTML page
pygmentize -f html -O full,style=friendly -o main.html main.beancount

# From standard input
bean-format main.beancount | pygmentize -l beancount
```

To see the token type of every piece of a ledger, which helps when choosing a style, use the `raw` formatter:

```shell
pygmentize -l beancount -f raw main.beancount
```

## From Python

Import the lexer class, or let Pygments look it up by alias or file name:

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_lexer_for_filename

from pygments_beancount import BeancountLexer

ledger = "2026-01-01 open Assets:Cash USD\n"

html = highlight(ledger, BeancountLexer(), HtmlFormatter())
same = highlight(ledger, get_lexer_by_name("beancount"), HtmlFormatter())
also = highlight(ledger, get_lexer_for_filename("main.beancount"), HtmlFormatter())
```

To work with the tokens themselves:

```python
for token_type, value in BeancountLexer().get_tokens(ledger):
    print(token_type, repr(value))
```

`guess_lexer` also recognizes ledgers, from lines such as a dated `open` or `balance`, a transaction whose flag is followed by a string, or an `option` line.
See {py:meth}`~pygments_beancount.BeancountLexer.analyse_text` for the score.
