"""One short input per Beancount element, and the tokens it must produce."""

import pytest
from conftest import significant
from token_cases import CASES


@pytest.mark.parametrize(
    ("text", "expected"),
    [pytest.param(text, expected, id=name) for name, text, expected in CASES],
)
def test_tokens(text: str, expected: list[tuple[object, str]]) -> None:
    assert significant(text) == expected


def test_case_names_are_unique() -> None:
    names = [name for name, _, _ in CASES]
    assert len(names) == len(set(names))
