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

    # def test_simple_omm_aggregation(self):
    #     self.t_engine.run_test('simple_omm_aggregation')

    # def test_max_min_aggregation_same_day(self):
    #     self.t_engine.run_test('max_min_aggregation_same_day')

    # def test_max_min_aggregation_different_days(self):
    #     self.t_engine.run_test('max_min_aggregation_different_days')

    # def test_max_min_date_aggregation_different_days(self):
    #     self.t_engine.run_test('max_min_date_aggregation_different_days')

    # def test_max_min_omm_aggregation_same_day(self):
    #     self.t_engine.run_test('max_min_aggregation_same_day')

    # def test_max_min_omm_aggregation_different_days(self):
    #     self.t_engine.run_test('max_min_omm_aggregation_different_days')

    # def test_max_min_omm_aggregation_regeneration_to_be_fixed_final_omm_min_is_20(self):
    #     self.t_engine.run_test('max_min_omm_aggregation_regeneration')

    # def test_max_min_simple_replace(self):
    #     self.t_engine.run_test('max_min_simple_replace')
