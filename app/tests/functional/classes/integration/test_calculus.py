from django.test import TestCase
from app.classes.integrationTests.typeTemp import TypeTempTest
from app.classes.metier.posteMetier import PosteMetier
from app.tools.jsonPlus import JsonPlus
import pytest
import logging
import os


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info("scope function with autouse")
    # print('I am in !')
    pass


@pytest.mark.functional
class CalculusTestSuite(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.tt = TypeTempTest()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_name = os.path.join(base_dir, '../fixtures/calculus_test_suite.json')
        texte = ''

        with open(file_name, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)
            self.my_test_suite = JsonPlus().loads(texte)

    # @pytest.mark.django_db
    def test_run_calculus_test_suite(self):
        """
            Run all tests in our suite test
        """
        pid = PosteMetier.getPosteIdByMeteor('BBF015')
        if pid is None:
            p = PosteMetier(1)
            p.data.meteor = 'BBF015'
            p.save()
        my_json = JsonPlus().loads("""
            {
                "meteor" : "BBF015",
                "info" : {
                    "blabla": "blabla"
                },
                "data": []
            }
            """)
        for a_test in self.my_test_suite:
            my_json['data'] = a_test['data']
            self.tt.delete_obs_agg()
            resp = self.tt.doCalculus(my_json, True)
            for a_check in a_test['test']:
                tmp_j = resp
                for a_key in a_check['f']:
                    tmp_j = tmp_j[a_key]
                if str(tmp_j) != str(a_check['v']):
                    assert a_test['name'] + ' failed, check: ' + str(a_check) + ', value: ' == str(tmp_j)
            print('    test ' + a_test['name'] + ' -> OK')
