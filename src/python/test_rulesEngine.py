import duckdb
import unittest
from rulesEngine import LandParcel, LandFeature, Rule, load_data


class TestRule(unittest.TestCase):

    def set_up(self):
        load_data()

    def test_evaluate_rule(self):
        parcel = duckdb.query("SELECT * from appezimenti WHERE id=1")
        rule = duckdb.query("SELECT * from rules WHERE name = 'ditch_boundary_below_moorline'")
        rule
        result = rule.evaluate()
        self.assertTrue(result[0])
