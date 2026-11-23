"""The Beancount lexer.

The token patterns follow Beancount's own scanner, ``lexer.l``, and the
places where each token may appear follow its grammar, ``grammar.y``:

* https://github.com/beancount/beancount/blob/master/beancount/parser/lexer.l
* https://github.com/beancount/beancount/blob/master/beancount/parser/grammar.y
* https://beancount.github.io/docs/beancount_language_syntax/

The lexer highlights; it never validates. It emits no
``Error`` token, because Sphinx refuses to highlight a
block that contains one, and documentation snippets often hold placeholders
such as ``...``.
"""

import re

from pygments.lexer import RegexLexer
from pygments.lexer import bygroups
from pygments.lexer import default
from pygments.lexer import include
from pygments.lexer import words
from pygments.token import Comment
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import Literal
from pygments.token import Name
from pygments.token import Number
from pygments.token import Operator
from pygments.token import Punctuation
from pygments.token import String
from pygments.token import Text
from pygments.token import Whitespace

__all__ = ["BeancountLexer"]

# Any character outside ASCII. Beancount's scanner works on UTF-8 bytes and
# accepts any multi-byte sequence in account names (``UTF-8-ONLY``).
_NONASCII = r"[^\x00-\x7f]"

# ``ACCOUNTTYPE(:ACCOUNTNAME)+`` in lexer.l: the root component starts with a
# capital letter, the others may also start with a digit.
ACCOUNT = (
    rf"(?:[A-Z]|{_NONASCII})(?:[A-Za-z0-9\-]|{_NONASCII})*"
    rf"(?::(?:[A-Z0-9]|{_NONASCII})(?:[A-Za-z0-9\-]|{_NONASCII})*)+"
)

# ``(17|18|19|20)[0-9]{2}[\-/][0-9]+[\-/][0-9]+`` in lexer.l. Any four-digit
# year is highlighted, since the lexer does not validate.
DATE = r"[0-9]{4}[\-/][0-9]+[\-/][0-9]+"

# A currency or a capital letter must not run into a letter or a digit, so
# ``USDx`` is not split into a currency and debris.
_CURRENCY_END = rf"(?![A-Za-z0-9]|{_NONASCII})"

# ``[A-Z][A-Z0-9\'\.\_\-]*[A-Z0-9]`` in lexer.l: at least two characters.
CURRENCY = rf"[A-Z][A-Z0-9'._\-]*[A-Z0-9]{_CURRENCY_END}"

# The futures form, such as ``/ESM24``: a slash, then at least one letter.
# lexer.l tries it before the division operator.
SLASH_CURRENCY = rf"/[A-Z0-9'._\-]*[A-Z](?:[A-Z0-9'._\-]*[A-Z0-9])?{_CURRENCY_END}"

# ``CAPITAL`` in lexer.l: one capital letter followed by whitespace. The
# grammar reads it as a flag where a flag may appear, and as a one-letter
# currency (``currency: CURRENCY | CAPITAL``) everywhere else.
CAPITAL = r"[A-Z](?=\s|$)"

# ``FLAGS`` in lexer.l. ``*`` and ``#`` are flags too, lexed as their own
# tokens there.
FLAG = r"[!&#?%]"

# ``#[A-Za-z0-9\-_/.]+`` and ``\^[A-Za-z0-9\-_/.]+`` in lexer.l.
_TAG_CHARS = r"[A-Za-z0-9\-_/.]"

# ``([0-9]+|[0-9][0-9,]+[0-9])(\.[0-9]*)?`` in lexer.l: no leading dot, and
# the sign is a separate operator token.
_INTEGER = r"(?:[0-9][0-9,]*[0-9]|[0-9])"

# Keywords that follow a date. ``txn`` is listed apart because it is a flag.
DATED_KEYWORDS = (
    "balance",
    "close",
    "commodity",
    "custom",
    "document",
    "event",
    "note",
    "open",
    "pad",
    "price",
    "query",
)

# Keywords that start a line without a date.
UNDATED_KEYWORDS = (
    "include",
    "option",
    "plugin",
    "popmeta",
    "poptag",
    "pushmeta",
    "pushtag",
)

# What ``analyse_text`` looks for: lines that are characteristic of a
# Beancount file and unlikely in any other format.
_ANALYSE_PATTERNS = (
    re.compile(
        rf"^{DATE}[ \t]+(?:open|close|balance|price|commodity|pad)[ \t]",
        re.MULTILINE,
    ),
    re.compile(rf'^{DATE}[ \t]+(?:txn|[*!])[ \t]+"', re.MULTILINE),
    re.compile(r'^option[ \t]+"', re.MULTILINE),
)


class BeancountLexer(RegexLexer):
    """Lexer for `Beancount <https://beancount.github.io/>`_ ledgers.

    Beancount is line-oriented, so the lexer needs context in three places
    only: the first column of a line, the token right after a date, and the
    inside of a string. The ``directive`` state handles the token after a
    date, the ``string`` state handles strings, which may span lines, and
    every other token is matched by the ``values`` rules.
    """

    name = "Beancount"
    url = "https://beancount.github.io/docs/beancount_language_syntax/"
    aliases = ["beancount", "bean"]  # noqa: RUF012
    filenames = ["*.beancount", "*.bean"]  # noqa: RUF012
    mimetypes = ["text/x-beancount"]  # noqa: RUF012

    # The first-column rules depend on ``^`` matching at every line start.
    flags = re.MULTILINE

    tokens = {  # noqa: RUF012
        "root": [
            # A hashbang, on the first line only.
            (r"\A#!.*", Comment.Hashbang),
            # Lines that lexer.l ignores: ``^[\*\:\#]/.`` and ``^{FLAGS}/.``.
            # A ``*`` line is an org-mode heading. ``#tag`` at the start of
            # a line is still a tag, because flex prefers the longer match.
            (r"^\*.+", Generic.Heading),
            (rf"^#(?!{_TAG_CHARS}).+", Comment.Special),
            (r"^[:!&?%].+", Comment.Special),
            # A date at the start of a line opens a directive.
            (
                rf"^({DATE})([ \t]+)",
                bygroups(Literal.Date, Whitespace),
                "directive",
            ),
            (words(UNDATED_KEYWORDS, prefix=r"^", suffix=r"\b"), Keyword.Namespace),
            # A posting flag: ``INDENT optflag account`` in grammar.y.
            (
                rf"^([ \t]+)(\*)([ \t]+)(?={ACCOUNT})",
                bygroups(Whitespace, Keyword, Whitespace),
            ),
            (
                rf"^([ \t]+)({FLAG}|[A-Z])([ \t]+)(?={ACCOUNT})",
                bygroups(Whitespace, Keyword.Pseudo, Whitespace),
            ),
            include("values"),
        ],
        # The token after a date: a directive keyword or a transaction flag
        # (``txn`` in grammar.y). Every rule leaves the state.
        "directive": [
            (r"txn\b", Keyword, "#pop"),
            (words(DATED_KEYWORDS, suffix=r"\b"), Keyword, "#pop"),
            (r'\*(?=[\s"]|$)', Keyword, "#pop"),
            (rf'(?:{FLAG}|[A-Z])(?=[\s"]|$)', Keyword.Pseudo, "#pop"),
            default("#pop"),
        ],
        "values": [
            (r"\n+", Whitespace),
            (r"[^\S\n]+", Whitespace),
            (r";.*", Comment.Single),
            (r'"', String.Double, "string"),
            # Order matters: the first rule that matches wins.
            (DATE, Literal.Date),
            # Not when a longer currency could be read, as in ``TRUEUSD``.
            (r"(?:TRUE|FALSE|NULL)(?![A-Z0-9'._\-]*[A-Z0-9])", Keyword.Constant),
            (ACCOUNT, Name.Namespace),
            # ``[a-z][a-zA-Z0-9\-_]+/:`` in lexer.l: at least two characters.
            (r"([a-z][A-Za-z0-9\-_]+)(:)", bygroups(Name.Attribute, Punctuation)),
            (CURRENCY, Name.Constant),
            (SLASH_CURRENCY, Name.Constant),
            (CAPITAL, Name.Constant),
            (rf"{_INTEGER}\.[0-9]*", Number.Float),
            (_INTEGER, Number.Integer),
            (rf"#{_TAG_CHARS}+", Name.Tag),
            (rf"\^{_TAG_CHARS}+", Name.Label),
            (r"@@|@|~|[+\-*/#]", Operator),
            (r"\{\{|\}\}|[{}(),|:]", Punctuation),
            # Anything else, as a run. The excluded characters always match
            # a rule above, so every character is consumed and no Error
            # token is ever emitted.
            (r'[^\s";{}(),|:@~+\-*/#]+', Text),
        ],
        # ``\"([^\\\"]|\\.)*\"`` in lexer.l. A state rather than one regular
        # expression: strings span lines, and an unterminated string must not
        # make the regular expression backtrack.
        "string": [
            (r'[^"\\]+', String.Double),
            (r"\\[\s\S]?", String.Escape),
            (r'"', String.Double, "#pop"),
        ],
    }

    @staticmethod
    def analyse_text(text: str) -> float:
        """Score how likely *text* is a Beancount ledger.

        Pygments wraps it so the result is always a float from 0.0 to 1.0
        (``pygments.util.make_analysator``). The score grows by 0.3 for
        each kind of characteristic line found: a dated ``open``, ``close``,
        ``balance``, ``price``, ``commodity`` or ``pad`` line; a dated
        transaction whose flag is followed by a string; an ``option`` line.
        It stays at 0.9 or below so the lexer does not claim files that only
        resemble a ledger.

        :param text: The text to score.
        :returns: A score from 0.0 to 0.9.
        """
        hits = sum(1 for pattern in _ANALYSE_PATTERNS if pattern.search(text))
        return 0.3 * hits
