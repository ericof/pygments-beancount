---
myst:
  html_meta:
    "description": "Set up the development environment for pygments-beancount, run the checks, and change the lexer."
    "keywords": "pygments-beancount, development, uv, pytest, ruff, mypy, towncrier"
---

(how-to-contribute)=

# Work on the code

This guide sets up the development environment, lists the checks, and shows how to change the lexer safely.

## Set up

The project uses [uv](https://docs.astral.sh/uv/) and a Makefile.
Clone the repository, then create the environment:

```shell
git clone https://github.com/ericof/pygments-beancount.git
cd pygments-beancount
make install
```

`make help` lists every target.

## Checks

```shell
make check        # ruff, mypy --strict and pytest: must pass before every commit
make format       # format the code and apply safe lint fixes
make coverage     # the tests with a coverage report; the lexer stays at 100%
make docs         # build the documentation; warnings are errors
make docs-vale    # check the documentation with Vale
```

## The tests

The suite has five kinds of test, all offline and all on synthetic ledgers in `tests/examples/`:

`test_tokens.py`
:   One short input per Beancount element and the tokens it must produce.
    The cases live in `tests/token_cases.py`.

`test_goldens.py`
:   Each `tests/examples/*.beancount` file against the `.tokens` file beside it.

`test_invariants.py`
:   Properties of every input: the tokens join back into the input, there is no `Error` token and no empty token, valid ledgers produce no `Text` token, and pathological input lexes quickly.

`test_plugin.py`
:   Pygments finds the installed lexer by alias, file name, MIME type and content.

`test_sphinx.py`
:   A real Sphinx and MyST build of `tests/roots/sphinx-myst/` highlights every block.

`test_examples_valid.py` also checks that the valid examples are real Beancount, with Beancount's own parser.
Beancount is a development dependency only; the lexer never imports it.

## Change the lexer

1. Read the rule in Beancount's [`lexer.l`](https://github.com/beancount/beancount/blob/master/beancount/parser/lexer.l) and where the grammar, [`grammar.y`](https://github.com/beancount/beancount/blob/master/beancount/parser/grammar.y), allows the token.
   Beancount is GPL-2.0: read its scanner for the rules, never copy its code.
2. Add a case to `tests/token_cases.py`, and watch it fail.
3. Change the rule in `src/pygments_beancount/lexer.py`, with a comment that names the `lexer.l` pattern it follows.
4. Rewrite the goldens and review every changed line of the diff:

   ```shell
   make test-update-goldens
   git diff tests/examples/
   ```

5. If the change is visible to users, update {doc}`/reference/tokens`.

## Supported versions

The package supports Python 3.11 to 3.14 and Pygments 2.13 or later.
Pygments 2.13 is the oldest release that finds plugins without `pkg_resources`; with older releases the lexer is installed but not found.
CI runs the tests on every supported Python and on the oldest supported Pygments:

```shell
make test-pygments-floor
```

## Changelog

Every change gets a news fragment in `news/`, which [towncrier](https://towncrier.readthedocs.io/) turns into `CHANGELOG.md` on release.
Name the file after the issue it closes, `news/<issue>.<type>`, or `news/+<slug>.<type>` without an issue.
The types are `breaking`, `feature`, `bugfix`, `internal`, `documentation` and `tests`.

```shell
make changelog    # preview the next changelog section
```

## Documentation

The documentation is written in Markdown with MyST, one sentence per line, and follows the [Diátaxis](https://diataxis.fr/) sections.
CI builds it on every push and publishes it to GitHub Pages from `main`.

```shell
make docs-livehtml   # rebuild on every change, at http://127.0.0.1:8050
```

## Make a release

Releases are made with [zest.releaser](https://zestreleaser.readthedocs.io/) and its towncrier plugin, from a clean `main` that is in sync with GitHub:

```shell
make release
```

The target refuses to start on another branch, with uncommitted changes, or when `news/` has no fragments, and it runs `make check` first.
zest.releaser then asks for the version, writes the changelog section from the fragments, commits, tags `v<version>`, moves `__version__` to the next `.dev0` version, commits again, and offers to push.
Each step waits for confirmation.

Pushing the tag starts the release workflow, which builds the package, publishes it to PyPI through trusted publishing, and creates the GitHub release.
Nothing is uploaded from your machine.
