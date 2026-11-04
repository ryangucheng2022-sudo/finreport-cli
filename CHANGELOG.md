# Changelog

## v1.0.0 (2026-11-04)

Initial open-source release.

- **Name resolution**: any A-share company by short name, full name, or
  6-digit code; ambiguous names return an explicit candidate list.
- **Full statements**: income statement, balance sheet and cash flow
  statement in full (all non-empty fields from the structured feed),
  current period vs. same period last year.
- **Key indicators**: revenue, gross profit/margin, parent & deducted net
  profit, expenses, operating cash flow, EPS, ROE, ROIC, leverage and
  turnover days (vendor basis, never locally recomputed).
- **Single-quarter split**: cumulative-difference derivation for flow
  items, with the prior-year quarter alongside.
- **Formal reports only**: forecasts, flash reports and estimates are
  excluded by design.
- **Outputs**: six-sheet Excel workbook (basis & source links included for
  audit) + JSON summary for pipelines and agents.
- 14 offline unit tests.
