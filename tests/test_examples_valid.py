"""The valid examples are real Beancount: its own parser accepts them.

Beancount is a test dependency only; the lexer never imports it.
"""

from collections.abc import Callable

import pytest
from conftest import VALID_EXAMPLES

parser = pytest.importorskip("beancount.parser.parser")


@pytest.mark.parametrize("name", VALID_EXAMPLES)
def test_beancount_parses_example(
    name: str, read_example: Callable[[str], str]
) -> None:
    entries, errors, _ = parser.parse_string(read_example(name))
    assert [error.message for error in errors] == []
    assert entries


def test_cheatsheet_is_not_valid(read_example: Callable[[str], str]) -> None:
    # The control: the parser does report errors, so the test above can fail.
    _, errors, _ = parser.parse_string(read_example("cheatsheet"))
    assert len(errors) == 5


def test_lexer_does_not_import_beancount() -> None:
    import pygments_beancount.lexer

    source = pygments_beancount.lexer.__file__
    assert source is not None
    with open(source, encoding="utf-8") as handle:
        assert "import beancount" not in handle.read()
