from django.test import TestCase
from app.tests.functional.classes.integration.calcTestEngine import CalcTestEngine
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info("scope function with autouse")
    # print('I am in !')
    pass


@pytest.mark.functional
class CalculusTestSuite(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.t_engine = CalcTestEngine()

    def test_1_simple_agg_hour(self):
        self.t_engine.run_test('1_simple_agg_hour')

    def test_2_simple_agg_hour_round_hour(self):
        self.t_engine.run_test('2_simple_agg_hour_round_hour')

    def test_3_max_min_agg_same_day(self):
        self.t_engine.run_test('3_max_min_agg_same_day')

    def test_4_max_min_date_agg_different_days(self):
        self.t_engine.run_test('4_max_min_date_agg_different_days')

    def test_5_simple_omm_agg_same_day(self):
        self.t_engine.run_test('5_simple_omm_agg_same_day')

    def test_6_simple_omm_agg_different_days(self):
        self.t_engine.run_test('6_simple_omm_agg_different_days')

    def test_7_max_min_omm_agg_different_days(self):
        self.t_engine.run_test('7_max_min_omm_agg_different_days')

    # will write in a specific table
    # def test_8_max_min_omm_agg_regen(self):
    #     self.t_engine.run_test('8_max_min_omm_agg_regen')

    def test_9_max_min_simple_replace(self):
        self.t_engine.run_test('9_max_min_simple_replace')
