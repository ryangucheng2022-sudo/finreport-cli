"""Offline unit tests for finreport (no network). Run:
python3 -m unittest discover -s tests -v"""
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
from importlib.machinery import SourceFileLoader
SPEC = importlib.util.spec_from_loader(
    "finreport",
    SourceFileLoader("finreport", os.path.join(HERE, "..", "bin", "finreport")))
fr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fr)

STOCKS = [
    {"code": "300661", "name": "圣邦股份"},
    {"code": "600519", "name": "贵州茅台"},
    {"code": "601318", "name": "中国平安"},
    {"code": "000001", "name": "平安银行"},
    {"code": "688798", "name": "艾为电子"},
    {"code": "920001", "name": "纬达光电"},
]


class ResolveTests(unittest.TestCase):
    def test_exact_name(self):
        s, f = fr.resolve_company("圣邦股份", STOCKS)
        self.assertEqual(s, "unique")
        self.assertEqual(f["code"], "300661")

    def test_code_direct(self):
        s, f = fr.resolve_company("600519", STOCKS)
        self.assertEqual(s, "unique")
        self.assertEqual(f["name"], "贵州茅台")

    def test_ambiguous(self):
        s, f = fr.resolve_company("平安", STOCKS)
        self.assertEqual(s, "ambiguous")
        self.assertGreaterEqual(len(f), 2)

    def test_not_found(self):
        s, _ = fr.resolve_company("不存在的公司", STOCKS)
        self.assertEqual(s, "none")

    def test_market_prefix(self):
        self.assertEqual(fr.market_prefix("688798"), "SH")
        self.assertEqual(fr.market_prefix("600519"), "SH")
        self.assertEqual(fr.market_prefix("300661"), "SZ")
        self.assertEqual(fr.market_prefix("000001"), "SZ")
        self.assertEqual(fr.market_prefix("920001"), "BJ")
        self.assertEqual(fr.market_prefix("830799"), "BJ")


class PeriodTests(unittest.TestCase):
    def test_prior_year(self):
        self.assertEqual(fr.prior_year("2026-09-30"), "2025-09-30")

    def test_prev_cumulative(self):
        self.assertEqual(fr.prev_cumulative("2026-06-30"), "2026-03-31")
        self.assertEqual(fr.prev_cumulative("2026-09-30"), "2026-06-30")
        self.assertEqual(fr.prev_cumulative("2026-12-31"), "2026-09-30")
        self.assertIsNone(fr.prev_cumulative("2026-03-31"))

    def test_label_is_cumulative_explicit(self):
        self.assertIn("1-9月累计", fr.period_label("2026-09-30"))
        self.assertIn("1-3月累计", fr.period_label("2026-03-31"))


class DeriveTests(unittest.TestCase):
    ROW = {"TOTALOPERATEREVE": 1000.0, "MLR": 400.0, "XSMLL": 40.0,
           "PARENTNETPROFIT": 150.0, "KCFJCXSYJLR": 120.0,
           "CHZZTS": 100.0, "YSZKZZTS": 30.0, "PAYABLE_TDAYS": 60.0}

    def test_derive(self):
        d = fr.derive_key_indicators(self.ROW)
        self.assertEqual(d["revenue"], 1000.0)
        self.assertEqual(d["gross_profit"], 400.0)
        self.assertEqual(d["inventory_days"], 100.0)

    def test_yoy(self):
        self.assertAlmostEqual(fr.yoy(110, 100), 10.0)
        self.assertAlmostEqual(fr.yoy(50, -100), 150.0)  # |prev| base
        self.assertIsNone(fr.yoy(10, 0))
        self.assertIsNone(fr.yoy(None, 5))

    def test_single_quarter_q2(self):
        main = {"2026-06-30": dict(self.ROW, TOTALOPERATEREVE=1000.0,
                                   MLR=400.0),
                "2026-03-31": dict(self.ROW, TOTALOPERATEREVE=400.0,
                                   MLR=180.0)}
        cash = {"2026-06-30": {"NETCASH_OPERATE": 300.0},
                "2026-03-31": {"NETCASH_OPERATE": 100.0}}
        sq = fr.single_quarter(main, cash, "2026-06-30")
        self.assertEqual(sq["revenue"], 600.0)
        self.assertEqual(sq["gross_profit"], 220.0)
        self.assertAlmostEqual(sq["gross_margin"], 220.0 / 600.0 * 100)
        self.assertEqual(sq["operating_cash_flow"], 200.0)

    def test_single_quarter_q1_is_cumulative(self):
        main = {"2026-03-31": dict(self.ROW)}
        cash = {"2026-03-31": {"NETCASH_OPERATE": 55.0}}
        sq = fr.single_quarter(main, cash, "2026-03-31")
        self.assertEqual(sq["revenue"], 1000.0)
        self.assertEqual(sq["operating_cash_flow"], 55.0)

    def test_single_quarter_missing_prev(self):
        main = {"2026-09-30": dict(self.ROW)}
        self.assertIsNone(fr.single_quarter(main, {}, "2026-09-30"))


class StatementRowsTests(unittest.TestCase):
    def test_labels_and_filter(self):
        rows = {
            "2026-09-30": {"OPERATE_INCOME": 100.0, "OPERATE_COST": 60.0,
                           "OPERATE_INCOME_YOY": 5.0, "SECUCODE": "X",
                           "SOME_UNKNOWN": 7.0, "EMPTY_FIELD": None},
            "2025-09-30": {"OPERATE_INCOME": 90.0, "OPERATE_COST": 55.0},
        }
        out = fr.statement_rows(rows, "income", ["2026-09-30", "2025-09-30"])
        fields = [r[0] for r in out]
        self.assertIn("OPERATE_INCOME", fields)
        self.assertNotIn("OPERATE_INCOME_YOY", fields)
        self.assertNotIn("EMPTY_FIELD", fields)
        labels = {r[0]: r[1] for r in out}
        self.assertEqual(labels["OPERATE_INCOME"], "其中：营业收入")
        self.assertIn("SOME_UNKNOWN", fields)  # unknown fields are kept


if __name__ == "__main__":
    unittest.main()
