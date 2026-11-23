"""Shared helpers: lexing without Pygments' newline handling, and goldens."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pygments.token import Whitespace
from pygments.token import _TokenType

from pygments_beancount import BeancountLexer

EXAMPLES = Path(__file__).parent / "examples"

# Examples that are complete, valid ledgers: Beancount's parser accepts them,
# and the lexer must emit no Text token for them.
VALID_EXAMPLES = ("full", "orgmode", "unicode")

# Every example, including snippets with placeholders.
ALL_EXAMPLES = tuple(sorted(path.stem for path in EXAMPLES.glob("*.beancount")))

Token = tuple[_TokenType, str]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-goldens",
        action="store_true",
        default=False,
        help="Rewrite tests/examples/*.tokens from the current lexer output.",
    )


def tokenize(text: str) -> list[Token]:
    """Lex *text* exactly as given.

    ``stripnl`` and ``ensurenl`` are off, so the token values join back into
    the input. Pygments still turns CRLF and CR into LF before lexing.

    :param text: The Beancount source.
    :returns: Every ``(token type, value)`` pair.
    """
    lexer = BeancountLexer(stripnl=False, ensurenl=False)
    return list(lexer.get_tokens(text))


def significant(text: str) -> list[Token]:
    """Lex *text* and drop whitespace tokens.

    :param text: The Beancount source.
    :returns: The ``(token type, value)`` pairs that are not whitespace.
    """
    return [
        (ttype, value) for ttype, value in tokenize(text) if ttype is not Whitespace
    ]


def format_tokens(tokens: list[Token]) -> str:
    """Render tokens as a golden file: one ``Type 'value'`` line per token.

    :param tokens: The tokens to render.
    :returns: The golden file's text.
    """
    lines = [
        f"{str(ttype).removeprefix('Token.'):<24} {value!r}" for ttype, value in tokens
    ]
    return "\n".join(lines) + "\n"


@pytest.fixture
def update_goldens(request: pytest.FixtureRequest) -> bool:
    """Whether ``--update-goldens`` was passed."""
    return bool(request.config.getoption("--update-goldens"))


@pytest.fixture
def read_example() -> Callable[[str], str]:
    """Return a function that reads ``tests/examples/<name>.beancount``."""

    def _read(name: str) -> str:
        return (EXAMPLES / f"{name}.beancount").read_text(encoding="utf-8")

    return _read
