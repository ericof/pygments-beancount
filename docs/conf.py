"""Sphinx configuration for the pygments-beancount documentation.

Set up like the Plone Python packages: Sphinx, MyST, plone-sphinx-theme,
Diátaxis sections, Vale. Nothing here registers the lexer: the docs
environment installs the package, and its entry point does the rest, which
is the point of the package. Every ``beancount`` block on these pages is
therefore a test of the lexer.
"""

from datetime import datetime

from pygments_beancount import __version__

project = "pygments-beancount"
author = "Érico Andrei"
copyright = str(datetime.now().year)
release = __version__
version = release

templates_path: list[str] = []

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxext.opengraph",
]

# _styles holds the Vale configuration and the styles `vale sync` downloads,
# whose README files are not pages.
exclude_patterns = ["_build", "_styles"]

# -- MyST -------------------------------------------------------------------

myst_enable_extensions = [
    "attrs_inline",
    "colon_fence",
    "deflist",
    "linkify",
    "substitution",
]
myst_heading_anchors = 3

# Number the lines of every Beancount block on these pages.
myst_number_code_blocks = ["beancount"]

# -- autodoc ----------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}
autodoc_member_order = "bysource"
autodoc_typehints = "description"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pygments": ("https://pygments.org/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# Report every reference that does not resolve.
nitpicky = True

# -- Link checking ----------------------------------------------------------

linkcheck_ignore = [
    r"http://localhost.*",
    r"http://127\.0\.0\.1.*",
    # Anchors on GitHub are generated client-side.
    r"https://github\.com/.*#.*",
    # Not published until the first push and the first release.
    r"https://github\.com/ericof/pygments-beancount.*",
    r"https://ericof\.github\.io/pygments-beancount.*",
    r"https://pypi\.org/project/pygments-beancount/?",
]

# -- HTML output ------------------------------------------------------------

html_theme = "plone_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/ericof/pygments-beancount",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pygments-beancount/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
    "logo": {"text": "pygments-beancount"},
    "navigation_with_keys": True,
    "path_to_docs": "docs",
    "repository_branch": "main",
    "repository_url": "https://github.com/ericof/pygments-beancount",
    "search_bar_text": "Search",
    "show_toc_level": 2,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
}
html_sidebars = {
    "**": [
        "navbar-logo",
        "search-button-field",
        "sbt-sidebar-nav",
    ]
}
html_title = f"{project} {release}"
html_extra_path = ["robots.txt"]

# The trailing slash matters: sphinxext.opengraph joins page URLs to it with
# urljoin, which drops the last path segment of a base without one.
html_baseurl = "https://ericof.github.io/pygments-beancount/"
sitemap_url_scheme = "{link}"
sitemap_filename = "sitemap-custom.xml"

ogp_site_url = html_baseurl
ogp_site_name = project
