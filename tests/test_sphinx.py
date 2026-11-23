"""A real Sphinx + MyST build highlights Beancount with no configuration.

The build runs in a subprocess with warnings as errors, so a block that
Sphinx could not highlight fails the test.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from pygments.token import STANDARD_TYPES
from pygments.token import Keyword
from pygments.token import Literal
from pygments.token import Name

pytest.importorskip("sphinx")
pytest.importorskip("myst_parser")

pytestmark = pytest.mark.sphinx

ROOT = Path(__file__).parent / "roots" / "sphinx-myst"


@pytest.fixture(scope="module")
def html(tmp_path_factory: pytest.TempPathFactory) -> str:
    srcdir = tmp_path_factory.mktemp("sphinx") / "src"
    shutil.copytree(ROOT, srcdir)
    outdir = srcdir / "_build" / "html"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "--keep-going",
            "-q",
            "-b",
            "html",
            str(srcdir),
            str(outdir),
        ],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return (outdir / "index.html").read_text(encoding="utf-8")


def _span(ttype: object) -> str:
    return f'<span class="{STANDARD_TYPES[ttype]}">'  # type: ignore[index]


def test_every_block_is_highlighted(html: str) -> None:
    # Fenced block, code-block, literalinclude and the placeholder block.
    assert html.count('class="highlight-beancount') == 4


def test_spans(html: str) -> None:
    assert f"{_span(Literal.Date)}2026-01-01</span>" in html
    assert f"{_span(Keyword)}open</span>" in html
    assert f"{_span(Keyword)}balance</span>" in html
    assert f"{_span(Name.Namespace)}Assets:Cash</span>" in html


def test_code_block_options(html: str) -> None:
    assert "A transaction" in html
    assert 'class="linenos"' in html
    assert 'class="hll"' in html


def test_inline_span(html: str) -> None:
    inline = re.search(
        r'<code class="[^"]*highlight[^"]*beancount[^"]*">(.*?)</code>', html, re.DOTALL
    )
    assert inline is not None
    assert _span(Name.Namespace) in inline.group(1)
