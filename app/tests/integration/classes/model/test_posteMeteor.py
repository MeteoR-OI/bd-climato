from django.test import TestCase
from app.classes.repository.posteMeteor import PosteMeteor


# models test
class PosteMeteorTest(TestCase):

    def create_poste_meteor(self, meteor='XYZ'):
        return PosteMeteor(1)
    
    def test_poste_meteor_creation(self, meteor='XYZ'):
        w = self.create_poste_meteor()
        self.assertTrue(isinstance(w, PosteMeteor))
        # self.assertEqual(w.data.meteor, meteor)
