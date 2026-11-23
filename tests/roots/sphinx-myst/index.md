# Beancount in MyST

A fenced block:

```beancount
2026-01-01 open Assets:Cash USD
```

A `code-block` directive with options:

```{code-block} beancount
:caption: A transaction
:linenos:
:emphasize-lines: 2

2026-01-05 * "Employer" "Salary"
  Assets:Cash      100.00 USD
  Income:Salary
```

An included ledger file:

```{literalinclude} example.beancount
:language: beancount
```

An inline span: `Assets:Cash`{l=beancount}.

A placeholder that must not fail the build:

```beancount
2026-01-01 open Assets:Cash ...
```
