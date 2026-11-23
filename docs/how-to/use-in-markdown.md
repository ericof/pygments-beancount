---
myst:
  html_meta:
    "description": "Highlight Beancount ledgers in MkDocs, Pelican and other sites built with Python-Markdown."
    "keywords": "Beancount, MkDocs, Material for MkDocs, Pelican, Python-Markdown, codehilite, pymdownx"
---

(how-to-use-in-markdown)=

# Highlight ledgers in MkDocs and Python-Markdown

This guide shows how to highlight Beancount blocks in sites built with [Python-Markdown](https://python-markdown.github.io/), such as MkDocs and Pelican.

Python-Markdown highlights code through Pygments when its `codehilite` extension, or the `pymdownx.highlight` extension from [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/), is enabled.
Both look the lexer up by the fence's language name, so once pygments-beancount is installed, ```` ```beancount ```` and ```` ```bean ```` blocks highlight with no further configuration.

## Install the package next to the site generator

Install pygments-beancount in the same environment as MkDocs, Pelican or your own build script:

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

In a uv project, add it to the dependency group that builds the site:

```shell
uv add --group docs pygments-beancount
```

If you installed the site generator as a uv tool, reinstall it with the package alongside:

```shell
uv tool install mkdocs --with mkdocs-material --with pygments-beancount
```
````
`````

If you installed it with `pipx`, inject the package into its environment with `pipx inject mkdocs pygments-beancount`.

## Material for MkDocs

Material for MkDocs highlights code with `pymdownx.highlight` and `pymdownx.superfences`.
If `mkdocs.yml` already enables them, Beancount blocks highlight as soon as the package is installed:

```yaml
markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
```

The theme ships its own colours for Pygments tokens, in light and dark mode.

## MkDocs with the default theme

The default `mkdocs` theme highlights code in the browser with highlight.js, so Pygments is never called.
To use Pygments instead, turn highlight.js off and enable `codehilite`:

```yaml
theme:
  name: mkdocs
  highlightjs: false

markdown_extensions:
  - codehilite
```

`codehilite` writes CSS classes, not colours.
Generate a stylesheet for one of the Pygments styles, and add it with `extra_css`:

```shell
pygmentize -S default -f html -a .codehilite > docs/css/pygments.css
```

## Pelican

Pelican's default Markdown settings already enable `codehilite`, so Beancount blocks in Markdown articles highlight once the package is installed.
As with MkDocs, the theme must include a stylesheet for the Pygments classes.

## Python-Markdown in your own code

Pass the `fenced_code` and `codehilite` extensions:

```python
import markdown

html = markdown.markdown(
    "```beancount\n2026-01-01 open Assets:Cash USD\n```\n",
    extensions=["fenced_code", "codehilite"],
)
```

## Tools that do not use Pygments

Hugo and Zola highlight code with their own libraries, not with Pygments, so this package has no effect on them.
The same applies to sites that highlight in the browser, with highlight.js or Prism.
