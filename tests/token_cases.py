"""Short inputs and the tokens they must produce, whitespace left out.

Shared by ``test_tokens.py``, which checks the tokens, and by
``test_invariants.py``, which checks the invariants on every input.
"""

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
from pygments.token import _TokenType

Date = Literal.Date
Account = Name.Namespace
Currency = Name.Constant
Key = Name.Attribute
Str = String.Double
Float = Number.Float
Integer = Number.Integer
Colon = (Punctuation, ":")

Case = tuple[str, str, list[tuple[_TokenType, str]]]

CASES: list[Case] = [
    # -- Comments and ignored lines ----------------------------------------
    ("comment-line", "; a comment", [(Comment.Single, "; a comment")]),
    (
        "comment-trailing",
        "2026-01-01 open Assets:Cash ; opened",
        [
            (Date, "2026-01-01"),
            (Keyword, "open"),
            (Account, "Assets:Cash"),
            (Comment.Single, "; opened"),
        ],
    ),
    (
        "hashbang",
        "#!/usr/bin/env bean-check\n",
        [(Comment.Hashbang, "#!/usr/bin/env bean-check")],
    ),
    (
        "hashbang-not-first-line",
        "\n#!not a hashbang",
        [(Comment.Special, "#!not a hashbang")],
    ),
    ("heading", "* Section", [(Generic.Heading, "* Section")]),
    ("heading-nested", "** Sub section", [(Generic.Heading, "** Sub section")]),
    ("ignored-colon", ":PROPERTIES:", [(Comment.Special, ":PROPERTIES:")]),
    ("ignored-hash", "# skipped line", [(Comment.Special, "# skipped line")]),
    ("ignored-bang", "! skipped line", [(Comment.Special, "! skipped line")]),
    ("ignored-ampersand", "& skipped", [(Comment.Special, "& skipped")]),
    ("ignored-question", "? skipped", [(Comment.Special, "? skipped")]),
    ("ignored-percent", "% skipped", [(Comment.Special, "% skipped")]),
    # flex prefers the longer match: a tag at the start of a line is a tag.
    ("hash-tag-first-column", "#trip", [(Name.Tag, "#trip")]),
    # -- Dates ---------------------------------------------------------------
    (
        "date-slashes",
        "2026/01/31 close Assets:Cash",
        [(Date, "2026/01/31"), (Keyword, "close"), (Account, "Assets:Cash")],
    ),
    (
        "date-one-digit",
        "2026-1-5 close Assets:Cash",
        [(Date, "2026-1-5"), (Keyword, "close"), (Account, "Assets:Cash")],
    ),
    (
        "date-as-value",
        "  booked: 2026-01-15",
        [(Key, "booked"), Colon, (Date, "2026-01-15")],
    ),
    # -- Dated directives ----------------------------------------------------
    *[
        (
            f"keyword-{keyword}",
            f"2026-01-01 {keyword}",
            [(Date, "2026-01-01"), (Keyword, keyword)],
        )
        for keyword in (
            "txn",
            "open",
            "close",
            "commodity",
            "balance",
            "pad",
            "note",
            "document",
            "price",
            "event",
            "query",
            "custom",
        )
    ],
    (
        "keyword-needs-boundary",
        "2026-01-01 openly",
        [(Date, "2026-01-01"), (Text, "openly")],
    ),
    (
        "date-at-end-of-line",
        "2026-01-01\n",
        [(Date, "2026-01-01")],
    ),
    # -- Undated directives --------------------------------------------------
    (
        "option",
        'option "title" "Ledger"',
        [
            (Keyword.Namespace, "option"),
            (Str, '"'),
            (Str, "title"),
            (Str, '"'),
            (Str, '"'),
            (Str, "Ledger"),
            (Str, '"'),
        ],
    ),
    (
        "plugin",
        'plugin "beancount.plugins.auto"',
        [
            (Keyword.Namespace, "plugin"),
            (Str, '"'),
            (Str, "beancount.plugins.auto"),
            (Str, '"'),
        ],
    ),
    (
        "include",
        'include "2026.beancount"',
        [
            (Keyword.Namespace, "include"),
            (Str, '"'),
            (Str, "2026.beancount"),
            (Str, '"'),
        ],
    ),
    ("pushtag", "pushtag #trip", [(Keyword.Namespace, "pushtag"), (Name.Tag, "#trip")]),
    ("poptag", "poptag #trip", [(Keyword.Namespace, "poptag"), (Name.Tag, "#trip")]),
    (
        "pushmeta",
        'pushmeta location: "Lisbon"',
        [
            (Keyword.Namespace, "pushmeta"),
            (Key, "location"),
            Colon,
            (Str, '"'),
            (Str, "Lisbon"),
            (Str, '"'),
        ],
    ),
    (
        "popmeta",
        "popmeta location:",
        [(Keyword.Namespace, "popmeta"), (Key, "location"), Colon],
    ),
    ("undated-keyword-indented", "  option", [(Text, "option")]),
    # -- Transaction flags ---------------------------------------------------
    (
        "flag-asterisk",
        '2026-01-01 * "Payee"',
        [(Date, "2026-01-01"), (Keyword, "*"), (Str, '"'), (Str, "Payee"), (Str, '"')],
    ),
    *[
        (
            f"flag-{name}",
            f'2026-01-01 {flag} "Payee"',
            [
                (Date, "2026-01-01"),
                (Keyword.Pseudo, flag),
                (Str, '"'),
                (Str, "Payee"),
                (Str, '"'),
            ],
        )
        for name, flag in (
            ("bang", "!"),
            ("ampersand", "&"),
            ("hash", "#"),
            ("question", "?"),
            ("percent", "%"),
            ("capital", "P"),
        )
    ],
    ("flag-at-end-of-line", "2026-01-01 *", [(Date, "2026-01-01"), (Keyword, "*")]),
    (
        "flag-before-quote",
        '2026-01-01 !"Payee"',
        [
            (Date, "2026-01-01"),
            (Keyword.Pseudo, "!"),
            (Str, '"'),
            (Str, "Payee"),
            (Str, '"'),
        ],
    ),
    # -- Postings ------------------------------------------------------------
    (
        "posting",
        "  Assets:Cash  -10.00 USD",
        [
            (Account, "Assets:Cash"),
            (Operator, "-"),
            (Float, "10.00"),
            (Currency, "USD"),
        ],
    ),
    ("posting-no-amount", "  Assets:Cash", [(Account, "Assets:Cash")]),
    (
        "posting-trailing-comment",
        "  Assets:Cash  1 USD ; cash",
        [
            (Account, "Assets:Cash"),
            (Integer, "1"),
            (Currency, "USD"),
            (Comment.Single, "; cash"),
        ],
    ),
    (
        "posting-flag-asterisk",
        "  * Assets:Cash",
        [(Keyword, "*"), (Account, "Assets:Cash")],
    ),
    (
        "posting-flag-bang",
        "  ! Assets:Cash",
        [(Keyword.Pseudo, "!"), (Account, "Assets:Cash")],
    ),
    (
        "posting-flag-hash",
        "  # Assets:Cash",
        [(Keyword.Pseudo, "#"), (Account, "Assets:Cash")],
    ),
    (
        "posting-flag-capital",
        "  P Assets:Cash",
        [(Keyword.Pseudo, "P"), (Account, "Assets:Cash")],
    ),
    # -- Accounts ------------------------------------------------------------
    ("account-digits", "Liabilities:Card:0042", [(Account, "Liabilities:Card:0042")]),
    (
        "account-dashes",
        "Equity:Opening-Balances",
        [(Account, "Equity:Opening-Balances")],
    ),
    (
        "account-non-ascii",
        "Assets:BR:Itaú:Conta-Corrente",
        [(Account, "Assets:BR:Itaú:Conta-Corrente")],
    ),
    ("account-non-ascii-root", "Ativos:Ásia", [(Account, "Ativos:Ásia")]),
    ("account-root-only", "Assets", [(Text, "Assets")]),
    # -- Currencies ----------------------------------------------------------
    ("currency", "USD", [(Currency, "USD")]),
    (
        "currency-special-characters",
        "NT.TO TLT_040921C144 A'B",
        [(Currency, "NT.TO"), (Currency, "TLT_040921C144"), (Currency, "A'B")],
    ),
    ("currency-slash", "/ESM24", [(Currency, "/ESM24")]),
    (
        "currency-slash-option",
        "/NQH21_QNEG21C13100",
        [(Currency, "/NQH21_QNEG21C13100")],
    ),
    ("currency-single-letter", "2 V ", [(Integer, "2"), (Currency, "V")]),
    ("currency-single-letter-at-end", "2 V", [(Integer, "2"), (Currency, "V")]),
    (
        "currency-list",
        "USD,EUR",
        [(Currency, "USD"), (Punctuation, ","), (Currency, "EUR")],
    ),
    ("currency-trailing-dash", "AB-", [(Currency, "AB"), (Operator, "-")]),
    ("currency-glued-lowercase", "USDx", [(Text, "USDx")]),
    ("currency-glued-non-ascii", "USDé", [(Text, "USDé")]),
    # -- Booleans and null ---------------------------------------------------
    ("true", "TRUE", [(Keyword.Constant, "TRUE")]),
    ("false", "FALSE", [(Keyword.Constant, "FALSE")]),
    ("null", "NULL", [(Keyword.Constant, "NULL")]),
    ("true-prefix-of-currency", "TRUEUSD", [(Currency, "TRUEUSD")]),
    ("null-prefix-of-currency", "NULL.X", [(Currency, "NULL.X")]),
    ("true-then-minus", "TRUE-", [(Keyword.Constant, "TRUE"), (Operator, "-")]),
    # -- Strings -------------------------------------------------------------
    ("string-empty", '""', [(Str, '"'), (Str, '"')]),
    (
        "string-escapes",
        r'"a \"b\" \\"',
        [
            (Str, '"'),
            (Str, "a "),
            (String.Escape, r"\""),
            (Str, "b"),
            (String.Escape, r"\""),
            (Str, " "),
            (String.Escape, "\\\\"),
            (Str, '"'),
        ],
    ),
    ("string-multi-line", '"one\ntwo"', [(Str, '"'), (Str, "one\ntwo"), (Str, '"')]),
    ("string-unterminated", '"open', [(Str, '"'), (Str, "open")]),
    (
        "string-backslash-at-end",
        '"open\\',
        [(Str, '"'), (Str, "open"), (String.Escape, "\\")],
    ),
    # -- Numbers -------------------------------------------------------------
    ("integer", "1", [(Integer, "1")]),
    ("float-trailing-dot", "1.", [(Float, "1.")]),
    ("float", "1.50", [(Float, "1.50")]),
    ("thousands", "1,234.56", [(Float, "1,234.56")]),
    ("thousands-integer", "1,234", [(Integer, "1,234")]),
    ("negative", "-7", [(Operator, "-"), (Integer, "7")]),
    ("leading-dot", ".5", [(Text, ".5")]),
    (
        "parentheses",
        "(1 + 2) * 3",
        [
            (Punctuation, "("),
            (Integer, "1"),
            (Operator, "+"),
            (Integer, "2"),
            (Punctuation, ")"),
            (Operator, "*"),
            (Integer, "3"),
        ],
    ),
    ("division", "90.00 / 3", [(Float, "90.00"), (Operator, "/"), (Integer, "3")]),
    ("division-glued", "10/2", [(Integer, "10"), (Operator, "/"), (Integer, "2")]),
    # -- Tags and links ------------------------------------------------------
    ("tag", "#trip-2026/lisbon.v1", [(Name.Tag, "#trip-2026/lisbon.v1")]),
    ("link", "^invoice_2026-01", [(Name.Label, "^invoice_2026-01")]),
    ("caret-alone", "^ x", [(Text, "^"), (Text, "x")]),
    # -- Metadata ------------------------------------------------------------
    (
        "metadata-string",
        '  name: "x"',
        [(Key, "name"), Colon, (Str, '"'), (Str, "x"), (Str, '"')],
    ),
    (
        "metadata-keyword-as-key",
        '  price: "USD:yahoo/VTI"',
        [(Key, "price"), Colon, (Str, '"'), (Str, "USD:yahoo/VTI"), (Str, '"')],
    ),
    (
        "metadata-account",
        "  from: Assets:Cash",
        [(Key, "from"), Colon, (Account, "Assets:Cash")],
    ),
    (
        "metadata-currency",
        "  currency: USD",
        [(Key, "currency"), Colon, (Currency, "USD")],
    ),
    (
        "metadata-tag",
        "  category: #food",
        [(Key, "category"), Colon, (Name.Tag, "#food")],
    ),
    (
        "metadata-bool",
        "  done: TRUE",
        [(Key, "done"), Colon, (Keyword.Constant, "TRUE")],
    ),
    (
        "metadata-null",
        "  voucher: NULL",
        [(Key, "voucher"), Colon, (Keyword.Constant, "NULL")],
    ),
    (
        "metadata-amount",
        "  rate: 120.00 USD",
        [(Key, "rate"), Colon, (Float, "120.00"), (Currency, "USD")],
    ),
    ("metadata-empty", "  remarks:", [(Key, "remarks"), Colon]),
    ("metadata-dashes", "  paid-with_card:", [(Key, "paid-with_card"), Colon]),
    # lexer.l requires two characters at least.
    ("metadata-one-letter", "  a:", [(Text, "a"), Colon]),
    # -- Costs and prices ----------------------------------------------------
    (
        "cost",
        '{250.10 USD, 2026-01-08, "lot"}',
        [
            (Punctuation, "{"),
            (Float, "250.10"),
            (Currency, "USD"),
            (Punctuation, ","),
            (Date, "2026-01-08"),
            (Punctuation, ","),
            (Str, '"'),
            (Str, "lot"),
            (Str, '"'),
            (Punctuation, "}"),
        ],
    ),
    (
        "cost-total",
        "{{1,251.00 USD}}",
        [
            (Punctuation, "{{"),
            (Float, "1,251.00"),
            (Currency, "USD"),
            (Punctuation, "}}"),
        ],
    ),
    (
        "cost-per-unit-and-total",
        "{502.12 # 9.95 USD}",
        [
            (Punctuation, "{"),
            (Float, "502.12"),
            (Operator, "#"),
            (Float, "9.95"),
            (Currency, "USD"),
            (Punctuation, "}"),
        ],
    ),
    ("cost-merge", "{*}", [(Punctuation, "{"), (Operator, "*"), (Punctuation, "}")]),
    ("cost-empty", "{}", [(Punctuation, "{"), (Punctuation, "}")]),
    ("price-unit", "@ 1.10 USD", [(Operator, "@"), (Float, "1.10"), (Currency, "USD")]),
    (
        "price-total",
        "@@ 11.00 USD",
        [(Operator, "@@"), (Float, "11.00"), (Currency, "USD")],
    ),
    (
        "tolerance",
        "3,000.00 ~ 0.01 USD",
        [(Float, "3,000.00"), (Operator, "~"), (Float, "0.01"), (Currency, "USD")],
    ),
    (
        "pipe",
        '"Payee" | "Narration"',
        [
            (Str, '"'),
            (Str, "Payee"),
            (Str, '"'),
            (Punctuation, "|"),
            (Str, '"'),
            (Str, "Narration"),
            (Str, '"'),
        ],
    ),
    # -- Fallback ------------------------------------------------------------
    ("placeholder", "...", [(Text, "...")]),
    ("placeholder-angle", "<amount>", [(Text, "<amount>")]),
    ("fallback-stops-at-brace", "x}", [(Text, "x"), (Punctuation, "}")]),
    ("non-breaking-space", "1\u00a0USD", [(Integer, "1"), (Currency, "USD")]),
]
