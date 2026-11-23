"""A minimal Sphinx project: MyST, and nothing about Beancount.

The lexer is found through its entry point, so this file does not mention
it. Only ``attrs_inline`` is enabled, for the inline ``{l=beancount}`` span.
"""

project = "sphinx-myst"
extensions = ["myst_parser"]
myst_enable_extensions = ["attrs_inline"]
exclude_patterns = ["_build"]
