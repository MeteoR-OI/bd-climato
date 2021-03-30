from django.test import TestCase
from app.classes.repository.posteMeteor import PosteMeteor
import pytest
# import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # logging.info("scope function with autouse")
    # print('I am in !')
    pass


@pytest.mark.functional
class PosteMeteorTest(TestCase):

    def create_poste_meteor(self):
        return PosteMeteor(4)

    def test_poste_meteor_creation(self):
        w = self.create_poste_meteor()
        w.data.meteor = "BBF015"
        w.data.fuseau = 4
        w.save()
        # print('Poste ' + str(w.data.id) + ', meteor: ' + w.data.meteor)
        self.assertTrue(isinstance(w, PosteMeteor))
        # self.assertEqual(w.data.meteor, meteor)
