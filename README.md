# Invoice Line Auditor

Recalculates invoice subtotal, tax, and total from structured line items and compares the result with a stated total. It exposes line-level arithmetic for review.

## Architecture

```text
JSON payload → domain algorithm → evidence-backed findings → human review
                              └→ OpenAI / CrewAI / Claude Code / Lyzr export surfaces
```

The core implementation is `agent.py` and exposes `analyze(payload)`. Tests include valid, malformed, boundary, and domain-specific cases.

## Run

```bash
python3 agent.py examples/good-input.json
python3 -m unittest discover -s tests -v
python3 tools/audit-invoice-line-auditor.py examples/good-input.json
```

## Limitations

The core checks arithmetic only and cannot validate delivery, tax jurisdiction, contract terms, discounts, currency, authenticity, or duplicate invoices across systems. It does not approve, reject, book, or pay an invoice.
