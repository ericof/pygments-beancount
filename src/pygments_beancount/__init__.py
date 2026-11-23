"""A Pygments lexer for Beancount ledgers.

Installing the package registers :class:`BeancountLexer` with Pygments
through the ``pygments.lexers`` entry point, under the aliases ``beancount``
and ``bean``.
"""

from pygments_beancount.lexer import BeancountLexer

__version__ = "1.0.0a1.dev0"

__all__ = ["BeancountLexer", "__version__"]
