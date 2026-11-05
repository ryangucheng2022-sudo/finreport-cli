"""Schema-drift contract tests.

The tool reads Eastmoney F10 responses through a small set of field names.
These tests pin that contract to sanitized fixtures (synthetic company,
round numbers — no real filings):

- the response envelope keeps the shape the fetchers navigate;
- every field the code reads out of a row is present in the fixture rows.
  The expected field set is extracted from bin/finreport itself, so editing
  the code's field list forces a fixture update here — that is the point:
  upstream schema drift should fail loudly in tests, not silently in output.

Refresh fixtures by re-capturing a response for any listed company and
replacing the values with synthetic ones, keeping every field name.
"""
import json, os, re, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, 'fixtures')
SRC = open(os.path.join(HERE, '..', 'bin', 'finreport'), encoding='utf-8').read()


def code_fields():
    """Fields read via main_row.get(...) plus the cashflow flow field."""
    fields = set(re.findall(r'main_row\.get\("([A-Z_]+)"\)', SRC))
    fields |= set(re.findall(r'\.get\("(NETCASH_[A-Z_]+)"\)', SRC))
    return fields


class TestEnvelope(unittest.TestCase):
    def test_envelope_and_row_keys(self):
        for name in ('eastmoney_zyzb.json', 'eastmoney_cashflow.json'):
            payload = json.load(open(os.path.join(FIX, name), encoding='utf-8'))
            self.assertIsInstance(payload.get('data'), list, name)
            for row in payload['data']:
                self.assertRegex(str(row.get('REPORT_DATE') or ''), r'^\d{4}-\d{2}-\d{2}',
                                 f'{name}: row lacks a usable REPORT_DATE')

    def test_zyzb_rows_carry_every_code_field(self):
        payload = json.load(open(os.path.join(FIX, 'eastmoney_zyzb.json'), encoding='utf-8'))
        expected = code_fields() - {'NETCASH_OPERATE'}
        self.assertGreater(len(expected), 10)
        for row in payload['data']:
            missing = expected - set(row)
            self.assertFalse(missing, f'fixture row missing fields the code reads: {missing}')

    def test_cashflow_rows_carry_flow_field(self):
        payload = json.load(open(os.path.join(FIX, 'eastmoney_cashflow.json'), encoding='utf-8'))
        for row in payload['data']:
            self.assertIn('NETCASH_OPERATE', row)


if __name__ == '__main__':
    unittest.main()
