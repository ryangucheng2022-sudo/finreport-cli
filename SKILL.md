# Skill: finreport

Fetch formal financial reports for any A-share listed company.

## When to use

The user asks for a Chinese listed company's financials — key indicators,
income statement, balance sheet, cash flow statement, latest quarter, or a
specific report period — for any A-share company.

## Command

```bash
finreport report <name-or-6-digit-code> [--date YYYY-MM-DD] [--output PATH] [--json-only]
finreport resolve <name>
```

## Rules

1. Formal reports only (quarterly / semi-annual / annual). Never present
   forecasts, flash reports or estimates as report data.
2. If name resolution returns candidates, show them and let the user pick;
   never guess between listed companies.
3. Always state the period basis explicitly (e.g. "2026 Jan–Sep
   cumulative"); never mix cumulative and single-quarter figures in one
   comparison without labeling both.
4. Turnover days come from the tool as-is; do not recompute them locally.
5. If a period is not disclosed, say so; never fill gaps with estimates or
   stale periods.
6. Report headline figures from the tool's JSON output (revenue, gross
   margin, parent/deducted net profit, operating cash flow, turnover days)
   and attach or link the workbook for the full statements.
