# finreport

English | [简体中文](README.zh-CN.md)

Give it a company name — get back the company's full formal financial report. A single-file CLI for **A-share listed companies** that fetches structured data from Eastmoney's F10 APIs and produces a complete workbook: key indicators, the **full income statement, balance sheet and cash flow statement** (current period vs. same period last year), and a single-quarter split derived from cumulative figures.

**Formal reports only** — quarterly, semi-annual and annual reports. Earnings forecasts, flash reports, guidance and estimates are never included.

## Who is it for

| Role | Typical scenarios | What you get |
|---|---|---|
| **Finance & accounting** | Earnings-season cross-checks of peers or listed subsidiaries; audit and due-diligence data packs; monthly management reporting | All three statements in one run with two-period comparison — no more downloading PDFs and transcribing numbers page by page; every figure traceable to its structured source, with the basis of preparation stated in the workbook |
| **Strategy & corporate development** | Competitor tracking; first-pass screening of M&A / investment targets; industry benchmarking and board materials | Any A-share company in seconds, not just a fixed watchlist; a single-quarter split that shows the latest quarter's momentum instead of a cumulative average; YoY changes computed and ready to drop into analysis |
| **Investment research** | Earnings-season sweeps across a coverage list; post-results reviews; comparable-company tables | Formal disclosures only — forecasts and flash numbers are excluded by design, so estimates never contaminate actuals; JSON output feeds your own models and pipelines directly |
| **Executives, board office & IR** | Ad-hoc questions ("what was their gross margin and inventory days last period?"); roadshow and inquiry preparation | Decision-grade numbers on demand, each one auditable; if a company hasn't disclosed yet, the tool says so — it never fills the gap with an estimate |
| **Developers & AI agents** | Wiring report fetching into internal agents, RPA or data pipelines | One file, one dependency, JSON in/out; ambiguous names return explicit candidates instead of a guess — deterministic behavior built for automation |

## Why not just download the PDF?

- **Structured, not transcribed**: figures come from the same structured feeds the data terminals use — no OCR, no copy errors.
- **Consistent basis**: cumulative vs. single-quarter is always labeled; turnover days use the vendor's disclosed basis (verified against filings) instead of a locally recomputed approximation.
- **Comparable out of the box**: current vs. prior-year period, YoY and percentage-point changes computed the same way for every company.

## How it works

- **Data sources.** Eastmoney's F10 financial-analysis endpoints provide the main indicators and the three statements; the quote-list endpoint resolves a company name to its stock code.
- **Formal disclosures only.** The tool takes the latest formally published reporting period and the same period a year earlier. Forecasts, preliminary flashes, and announcements are never mixed into the statements.
- **No guessing.** If a name matches several companies, resolution returns the candidates instead of picking one.
- **Single-quarter derivation.** Quarterly figures are differenced from cumulative reports (e.g. Q3 alone = Jan–Sep minus Jan–Jun) and labeled as derived, never presented as originally disclosed.
- **As-reported values.** Amounts keep the source unit (thousands of CNY); turnover days are taken as reported by the source and never recomputed, so the output can be traced back to the filing line by line.
- **Output.** A six-sheet standard Excel workbook (key indicators plus full statements) and a JSON summary, verified cell by cell against a reference company's published report.

## Install

```bash
pip install git+https://github.com/ryangucheng2022-sudo/finreport-cli.git   # provides the `finreport` command
```

(openpyxl is installed automatically as the only dependency.) Or clone the repo and run `bin/finreport` directly.

## Quick start

```bash
finreport report 圣邦股份                    # latest disclosed period
finreport report 600519                      # or pass the 6-digit code
finreport report 贵州茅台 --date 2026-06-30  # a specific report period
finreport report 中国平安 --json-only        # JSON summary only, no workbook
finreport resolve 中国平安                    # name resolution only
```

- Name resolution: exact short name wins; multiple matches (e.g. a common word) return a candidate list — the tool **never guesses**.
- Default period: the latest formally disclosed one; the comparison period is the same period last year.
- Output: a JSON summary (key indicators for both periods, single-quarter split, workbook path) plus an Excel workbook with six sheets — `说明` (basis & source links), `关键指标` (key indicators), `利润表`, `资产负债表`, `现金流量表` (full statements), `单季拆分` (single-quarter split). Amounts in the workbook are in thousand CNY.
- Unknown statement fields are kept and shown with their raw field code — nothing is silently dropped or given an invented translation.

## Requirements

- Python 3.9+; the only third-party dependency is `openpyxl` (workbook output).
- The A-share company list (~5,900) is cached at `~/.finreport/stock_list.json` for 24h; the first fetch takes 1–2 minutes, afterwards lookups are instant.

## Verification

Reconciled line-by-line against a published peer-monitoring workbook (a semiconductor name, 2025 Jan–Sep cumulative: revenue, gross profit, gross margin, deducted net profit and all three turnover-day figures matched exactly), and tested across industries including a consumer name and a financial conglomerate (bank/insurance statement structure).

## Data-source contract

The Eastmoney F10 field names this tool reads are pinned by sanitized fixtures under `tests/fixtures/` and by `tests/test_schema_drift.py`, which extracts the expected field set from the code itself: if upstream renames a field, the test suite fails instead of the report silently degrading. Fixtures use a synthetic company and round numbers — refresh them by re-capturing a response and replacing the values, keeping every field name.

## Tests

```bash
python3 -m unittest discover -s tests -v   # 14 offline cases
```

## Version

v1.0.0 — see [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE).
