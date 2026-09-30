# Decision and Reasoning

The result is match when the absolute difference between the stated and calculated totals is within the explicit tolerance. Otherwise it reports mismatch and the signed difference without approving or paying the invoice. The implementation returns structured findings so a reviewer can see how each result was derived.

# Inputs and Data Sources

The caller supplies one or more uniquely identified lines with nonnegative quantity and unit price and a tax rate from zero through one. A nonnegative stated total is required, and an optional bounded tolerance defaults to one cent. The only data source is the caller-provided payload plus the checked-in rules and code; no network or private-file access is used.

# Known Limitations and Constraints

The core checks arithmetic only and cannot validate delivery, tax jurisdiction, contract terms, discounts, currency, authenticity, or duplicate invoices across systems. It does not approve, reject, book, or pay an invoice. The result is a bounded pre-review aid and must not be presented as professional certification or an official HiDevs result.
