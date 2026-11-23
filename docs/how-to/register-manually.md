---
myst:
  html_meta:
    "description": "Register the Beancount lexer with Sphinx or Pygments by hand, where entry points are not available."
    "keywords": "Beancount, Sphinx, add_lexer, entry points, vendored"
---

(how-to-register-manually)=

# Register the lexer by hand

Pygments finds the lexer through the `pygments.lexers` entry point that the package declares.
Some environments have no entry points, for example a copy of the lexer vendored into a repository instead of installed.
This guide registers it by hand there.

## In Sphinx

Add a `setup()` function to `conf.py` that calls {py:meth}`sphinx.application.Sphinx.add_lexer`:

```python
from pygments_beancount import BeancountLexer


def setup(app):
    app.add_lexer("beancount", BeancountLexer)
```

Pass the class, not an instance: Sphinx 4.0 and later reject an instance.
Register each alias you use in the documentation, such as `bean`, the same way.

## In Pygments alone

Without Sphinx, skip the lookup functions and pass the lexer instance yourself:

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter

from pygments_beancount import BeancountLexer

html = highlight(source, BeancountLexer(), HtmlFormatter())
```

`pygmentize` can also load the lexer from a file with `-x`:

```shell
pygmentize -x -l path/to/lexer.py:BeancountLexer main.beancount
```
