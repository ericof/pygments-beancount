# pygments-beancount

A Pygments lexer for Beancount ledgers, registered through the
`pygments.lexers` entry point. The user documentation is in `docs/` (start at
`docs/index.md`); this file holds the rules for working on the code.

## Fixed decisions

- Python 3.11 to 3.14, managed only with uv. No pip, poetry or requirements
  files. Pygments 2.13 or later: older releases look plugins up through
  `pkg_resources` and do not find the lexer.
- The lexer depends on Pygments only. Beancount is a development dependency,
  used to check that the valid examples parse; never import it from `src/`.
- Token patterns follow Beancount's scanner, `beancount/parser/lexer.l`, and
  token placement follows `beancount/parser/grammar.y`. Read them, never copy
  them: Beancount is GPL-2.0, this package is BSD-2-Clause. Each rule in
  `lexer.py` has a comment naming the `lexer.l` pattern it follows.
- Never emit an `Error` token. Sphinx drops the colours of a block that has
  one. The fallback rule turns unrecognized runs into `Text`; every character
  it excludes must match another rule.
- Only standard Pygments token types, so every style colours the output.
  `docs/reference/tokens.md` is the mapping; keep it in step with the lexer.
- All example ledgers are synthetic. No real accounts, names or balances.
- Check Pygments, Sphinx and MyST behaviour against the installed packages in
  `.venv` or their documentation, not from memory.

## Commands

Use the Makefile; do not invent the underlying tool invocations.

```shell
make install              # uv sync
make check                # ruff, mypy --strict, pytest: must pass before every commit
make format
make coverage             # the lexer stays at 100%
make test-update-goldens  # after a deliberate lexer change; review the diff
make test-pygments-floor  # the tests on the oldest supported Pygments
make docs                 # Sphinx + MyST, warnings are errors
make docs-vale            # Vale: errors fail, warnings are advisory
make build                # sdist and wheel into dist/
make changelog            # preview the next changelog section
make release              # Érico only: zest.releaser fullrelease from a clean main
```

## Tests

- New syntax: add a case to `tests/token_cases.py` first, watch it fail,
  then change the rule.
- `tests/examples/*.beancount` each have a `.tokens` golden beside it.
  Regenerate with `make test-update-goldens` and review every changed line.
- Examples listed in `VALID_EXAMPLES` (`tests/conftest.py`) must parse with
  Beancount and produce no `Text` token.

## Changelog

towncrier fragments in `news/`: `<issue>.<type>` or `+<slug>.<type>`, with the
types `breaking`, `feature`, `bugfix`, `internal`, `documentation` and
`tests`. English, past tense, ending with the author's GitHub handle.

## Documentation

MyST Markdown, one sentence per line, Diátaxis sections. Every Beancount block
in the docs goes through the lexer, so `make docs` is also a test.
