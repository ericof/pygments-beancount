"""Pygments finds the installed lexer by alias, file name and content."""

from collections.abc import Callable
from importlib.metadata import entry_points

import pytest
from pygments.lexers import find_lexer_class_by_name
from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import get_lexer_for_mimetype
from pygments.lexers import guess_lexer

from pygments_beancount import BeancountLexer
from pygments_beancount import __version__


def test_entry_point() -> None:
    found = [
        ep for ep in entry_points(group="pygments.lexers") if ep.name == "beancount"
    ]
    assert len(found) == 1
    assert found[0].value == "pygments_beancount.lexer:BeancountLexer"
    assert found[0].load() is BeancountLexer


@pytest.mark.parametrize("alias", ["beancount", "bean", "Beancount"])
def test_alias(alias: str) -> None:
    assert isinstance(get_lexer_by_name(alias), BeancountLexer)
    assert find_lexer_class_by_name(alias) is BeancountLexer


@pytest.mark.parametrize(
    "filename", ["ledger.beancount", "ledger.bean", "2026/main.beancount"]
)
def test_filename(filename: str) -> None:
    assert isinstance(get_lexer_for_filename(filename), BeancountLexer)


def test_mimetype() -> None:
    assert isinstance(get_lexer_for_mimetype("text/x-beancount"), BeancountLexer)


def test_guess_lexer(read_example: Callable[[str], str]) -> None:
    assert isinstance(guess_lexer(read_example("full")), BeancountLexer)


def test_analyse_text_scores(read_example: Callable[[str], str]) -> None:
    assert BeancountLexer.analyse_text(read_example("full")) == pytest.approx(0.9)
    assert BeancountLexer.analyse_text(
        "2026-01-01 open Assets:Cash USD\n"
    ) == pytest.approx(0.3)
    assert BeancountLexer.analyse_text('2026-01-01 * "Payee"\n') == pytest.approx(0.3)
    assert BeancountLexer.analyse_text('option "title" "x"\n') == pytest.approx(0.3)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            "import sys\n\ndef main() -> None:\n    print(sys.argv)\n", id="python"
        ),
        pytest.param("[section]\nkey = value\n; comment\n", id="ini"),
        pytest.param(
            "# Title\n\n* item\n* other item\n\n2026-01-01 is a date.\n", id="markdown"
        ),
        pytest.param("2026-01-01 15:00:00 INFO started\n", id="log"),
    ],
)
def test_analyse_text_ignores_other_formats(text: str) -> None:
    assert BeancountLexer.analyse_text(text) == 0.0


def test_version() -> None:
    assert __version__
