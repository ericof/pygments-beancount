"""Each ``tests/examples/<name>.beancount`` against its ``<name>.tokens`` golden.

Run ``make test-update-goldens`` (``pytest --update-goldens``) to rewrite the
goldens after a deliberate change to the lexer, then review the diff.
"""

from collections.abc import Callable

import pytest
from conftest import ALL_EXAMPLES
from conftest import EXAMPLES
from conftest import format_tokens
from conftest import tokenize


def test_every_example_has_a_golden() -> None:
    assert len(ALL_EXAMPLES) >= 4
    missing = [
        name for name in ALL_EXAMPLES if not (EXAMPLES / f"{name}.tokens").exists()
    ]
    assert missing == []


@pytest.mark.parametrize("name", ALL_EXAMPLES)
def test_golden(
    name: str, read_example: Callable[[str], str], update_goldens: bool
) -> None:
    golden = EXAMPLES / f"{name}.tokens"
    actual = format_tokens(tokenize(read_example(name)))
    if update_goldens:
        golden.write_text(actual, encoding="utf-8")
        pytest.skip(f"rewrote {golden.name}")
    assert actual == golden.read_text(encoding="utf-8")
