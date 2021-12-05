from app.models import Poste

# import pytest
# import app.tools.myTools as t


# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     # t.logInfo('fixture posteMeteor::enable_db_access_for_all_tests called')
#     pass


class PosteMeteor:
    """
        PosteMeteor

        objets Poste metier

        p1=PosteMeteor(1) -> recupere le poste id = 1 + exclusions actuelles
        p2=PosteMeteor(1, my_date) -> recupere le poste id = 1 et exclusions a la date de my_date
    """

    def __init__(self, poste_id: int):
        """ load our instance from db, load exclusions at date_histo """
        if Poste.objects.filter(id=poste_id).exists():
            self.data = Poste.objects.get(id=poste_id)
        else:
            self.data = Poste()

    @staticmethod
    def getPosteIdByMeteor(meteor: str) -> int:
        """ find a poste with his meteor name """
        if Poste.objects.filter(meteor=meteor).exists():
            return Poste.objects.filter(meteor=meteor).first().id
        return None

    def save(self):
        """ save Poste """
        self.data.save()

    def __str__(self):
        """print myself"""
        return "PosteMeteor id: " + str(self.data.id) + ", meteor: " + self.data.meteor
