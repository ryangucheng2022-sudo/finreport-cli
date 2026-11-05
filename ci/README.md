# CI kit

Ready-to-enable GitHub Actions setup, kept outside `.github/workflows/`
so it can be reviewed and versioned like any other file.

**Enable it:** copy `ci.yml` to `.github/workflows/ci.yml` and push.

One job: installs openpyxl and runs the full unittest suite, including the
schema-drift contract tests that pin the Eastmoney F10 field names.
