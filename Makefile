### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

UV ?= uv
CODE := src tests docs
# The oldest Pygments release the package supports; see docs/how-to/contribute.md.
PYGMENTS_FLOOR ?= 2.13.0

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-22s %s\n", $$1, $$2}'

.PHONY: install
install: ## Create the virtualenv with the development tools
	$(UV) sync

.PHONY: clean
clean: ## Remove the virtualenv, caches and build output
	rm -rf .venv .ruff_cache .pytest_cache .mypy_cache .coverage dist docs/_build

############################################
# QA
############################################
.PHONY: format
format: ## Format code and apply safe lint fixes
	$(UV) run ruff format $(CODE)
	$(UV) run ruff check --fix $(CODE)

.PHONY: lint
lint: ## ruff (format check and lint) and mypy; changes nothing
	$(UV) run ruff format --check $(CODE)
	$(UV) run ruff check $(CODE)
	$(UV) run mypy

.PHONY: test
test: ## Run the test suite
	$(UV) run pytest

.PHONY: coverage
coverage: ## Run the test suite with a coverage report
	$(UV) run pytest --cov=pygments_beancount --cov-report=term-missing

.PHONY: test-update-goldens
test-update-goldens: ## Rewrite tests/examples/*.tokens; review the diff afterwards
	$(UV) run pytest tests/test_goldens.py --update-goldens

# uv run would sync the locked Pygments back, hence --no-sync.
.PHONY: test-pygments-floor
test-pygments-floor: ## Run the tests against the oldest supported Pygments
	$(UV) sync
	$(UV) pip install "pygments==$(PYGMENTS_FLOOR)"
	$(UV) run --no-sync python -c "import pygments; assert pygments.__version__ == '$(PYGMENTS_FLOOR)', pygments.__version__"
	$(UV) run --no-sync pytest -m "not sphinx"
	$(UV) sync

.PHONY: check
check: lint test ## lint and test: must pass before every commit

############################################
# Build
############################################
.PHONY: build
build: ## Build the sdist and the wheel into dist/
	rm -rf dist
	$(UV) build

############################################
# Documentation
############################################
DOCS_DIR := docs
DOCS_BUILDDIR := $(DOCS_DIR)/_build
DOCS_SPHINXOPTS ?=
DOCS_VALEFILES := $(shell find $(DOCS_DIR) -type f -name "*.md" -not -path "$(DOCS_BUILDDIR)/*" -not -path "$(DOCS_DIR)/_styles/*" -print)
DOCS_VALEOPTS ?=

.PHONY: docs
docs: ## Build the documentation (warnings are errors)
	$(UV) run --group docs sphinx-build -W --keep-going -b html $(DOCS_DIR) "$(DOCS_BUILDDIR)/html" $(DOCS_SPHINXOPTS)

.PHONY: docs-livehtml
docs-livehtml: ## Rebuild the documentation on changes, with live reload in the browser
	$(UV) run --group docs sphinx-autobuild --ignore "*.swp" --port 8050 \
		-b html $(DOCS_DIR) "$(DOCS_BUILDDIR)/html" $(DOCS_SPHINXOPTS)

.PHONY: docs-linkcheck
docs-linkcheck: ## Check that all links in the documentation resolve
	$(UV) run --group docs sphinx-build -b linkcheck $(DOCS_DIR) "$(DOCS_BUILDDIR)/linkcheck"

.PHONY: docs-vale
docs-vale: ## Check the documentation with Vale
	$(UV) run --group docs vale sync
	$(UV) run --group docs vale --no-wrap $(DOCS_VALEOPTS) $(DOCS_VALEFILES)

.PHONY: docs-clean
docs-clean: ## Remove the built documentation
	rm -rf "$(DOCS_BUILDDIR)"

############################################
# Changelog
############################################
.PHONY: changelog
changelog: ## Preview the next changelog section from news/
	$(UV) run --group release towncrier build --draft --version "next"

############################################
# Release
############################################
# zest.releaser asks for the version, writes the changelog with towncrier,
# commits, tags v<version>, bumps to the next .dev0 and offers to push.
# Pushing the tag starts the workflow that publishes to PyPI.
.PHONY: release
release: ## Make a release from a clean, up-to-date main
	@test "$$(git branch --show-current)" = main || { echo "Releases are made from main." >&2; exit 1; }
	@test -z "$$(git status --porcelain)" || { echo "The working tree is not clean." >&2; exit 1; }
	@git fetch --quiet origin main
	@test "$$(git rev-parse HEAD)" = "$$(git rev-parse origin/main)" || { echo "main is not in sync with origin/main." >&2; exit 1; }
	@find news -maxdepth 1 -type f ! -name '.*' | grep -q . || { echo "news/ has no fragments: nothing to release." >&2; exit 1; }
	$(MAKE) check
	$(UV) run --group release fullrelease
