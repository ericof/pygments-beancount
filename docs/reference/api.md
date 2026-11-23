---
myst:
  html_meta:
    "description": "API reference for the BeancountLexer class."
    "keywords": "Beancount, Pygments, BeancountLexer, API"
---

# API

The package exports one class, {py:class}`~pygments_beancount.BeancountLexer`, and its version, `pygments_beancount.__version__`.

| Attribute | Value |
| --- | --- |
| `name` | `Beancount` |
| `aliases` | `beancount`, `bean` |
| `filenames` | `*.beancount`, `*.bean` |
| `mimetypes` | `text/x-beancount` |
| Entry point | `beancount = pygments_beancount.lexer:BeancountLexer`, in the `pygments.lexers` group |

```{eval-rst}
.. autoclass:: pygments_beancount.BeancountLexer
   :members: analyse_text
   :exclude-members: tokens, flags
```

```{eval-rst}
.. automodule:: pygments_beancount.lexer
   :no-members:
```
