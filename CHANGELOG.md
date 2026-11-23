# Changelog

<!--
   Do not add entries to this file by hand.
   Add a news fragment to the news/ directory instead; towncrier writes this
   file on release. See docs/how-to/contribute.md.
-->

<!-- towncrier release notes start -->

## 1.0.0a1 (2026-11-23)

### New features:

- Added `BeancountLexer`, a Pygments lexer for Beancount v3 ledgers. Installing the package is the only setup: Pygments finds it under the aliases `beancount` and `bean` and for `*.beancount` and `*.bean` files, so ```` ```beancount ```` blocks highlight in Sphinx and MyST with no configuration. It never emits an `Error` token, so blocks with placeholders such as `...` still highlight. @ericof

### Internal:

- Added `make release`, which makes a release with zest.releaser and zestreleaser.towncrier. @ericof

### Documentation:

- Documented the lexer in MkDocs, Material for MkDocs, Pelican and Python-Markdown, and put the install command, the language names and a fuller example on the landing page. @ericof
