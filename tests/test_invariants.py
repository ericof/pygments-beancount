"""Properties that hold for every input, valid or not."""

import time
from collections.abc import Callable

import pytest
from conftest import ALL_EXAMPLES
from conftest import VALID_EXAMPLES
from conftest import tokenize
from pygments.token import Error
from pygments.token import Text
from token_cases import CASES

from pygments_beancount import BeancountLexer

INPUTS = [pytest.param(text, id=name) for name, text, _ in CASES]


def _check(text: str) -> None:
    tokens = tokenize(text)
    assert "".join(value for _, value in tokens) == text
    assert [value for ttype, value in tokens if ttype in Error] == []
    assert [ttype for ttype, value in tokens if value == ""] == []


@pytest.mark.parametrize("text", INPUTS)
def test_case_invariants(text: str) -> None:
    _check(text)


@pytest.mark.parametrize("name", ALL_EXAMPLES)
def test_example_invariants(name: str, read_example: Callable[[str], str]) -> None:
    _check(read_example(name))


@pytest.mark.parametrize("name", VALID_EXAMPLES)
def test_valid_example_has_no_text(
    name: str, read_example: Callable[[str], str]
) -> None:
    # The fallback rule must not hide a gap in the rules for valid input.
    tokens = tokenize(read_example(name))
    assert [value for ttype, value in tokens if ttype is Text] == []


def test_placeholders_fall_back_to_text(read_example: Callable[[str], str]) -> None:
    tokens = tokenize(read_example("cheatsheet"))
    assert [value for ttype, value in tokens if ttype is Text] == [
        "...",
        "...",
        "...",
        "<amount>",
    ]


@pytest.mark.parametrize(
    ("text", "normalized"),
    [
        pytest.param(
            "2026-01-01 open Assets:Cash\r\n",
            "2026-01-01 open Assets:Cash\n",
            id="crlf",
        ),
        pytest.param(
            "2026-01-01 open Assets:Cash\r", "2026-01-01 open Assets:Cash\n", id="cr"
        ),
        pytest.param(
            "2026-01-01 open Assets:Cash",
            "2026-01-01 open Assets:Cash",
            id="no-final-newline",
        ),
    ],
)
def test_line_endings(text: str, normalized: str) -> None:
    # Pygments turns CRLF and CR into LF before the lexer sees the text.
    tokens = tokenize(text)
    assert "".join(value for _, value in tokens) == normalized
    assert [value for ttype, value in tokens if ttype in Error] == []


def test_default_options_end_with_a_newline() -> None:
    # With Pygments' defaults, the output always ends with one newline.
    tokens = list(BeancountLexer().get_tokens("2026-01-01 open Assets:Cash"))
    assert tokens[-1][1] == "\n"


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("A" * 20_000, id="capitals"),
        pytest.param("A" * 20_000 + "x", id="capitals-then-lowercase"),
        pytest.param("1," * 20_000, id="thousands-separators"),
        pytest.param('"' + "\\" * 20_001, id="backslashes-in-unterminated-string"),
        pytest.param("/" + "-" * 20_000, id="slash-then-dashes"),
        pytest.param("Assets:" * 5_000, id="account-colons"),
        pytest.param("  " + "a" * 20_000 + ":", id="long-key"),
    ],
)
def test_pathological_input_is_fast(text: str) -> None:
    start = time.perf_counter()
    tokens = tokenize(text)
    elapsed = time.perf_counter() - start
    assert "".join(value for _, value in tokens) == text
    assert elapsed < 2.0
