from app.models import Poste, Load_Type, Data_Source
from datetime import datetime


class PosteMeteor:
    """
        PosteMeteor

        objets Poste metier

        p1=PosteMeteor(1) -> recupere le poste id = 1
        p2=PosteMeteor("BBF015") -> recupere le poste meteor BBF015
    """

    LoadType = Load_Type
    DataSource = Data_Source

    def __init__(self, key):
        if 'int' in str(type(key)):
            """ load our instance from db """
            if Poste.objects.filter(id=key).exists():
                self.data = Poste.objects.get(id=key)
            else:
                self.data = Poste()
        else:
            """ load our instance from db """
            if Poste.objects.filter(meteor=key).exists():
                self.data = Poste.objects.get(meteor=key)
            else:
                self.data = Poste()
                self.data.meteor = key

    def save(self):
        """ save Poste """
        self.data.save()

    @staticmethod
    def getPosteIdByMeteor(meteor: str):
        if Poste.objects.filter(meteor=meteor).exists():
            return Poste.objects.filter(meteor=meteor).first().id
        return None

    @staticmethod
    def getPosteByMeteor(meteor: str):
        if Poste.objects.filter(meteor=meteor).exists():
            return Poste(meteor)
        else:
            return None

    @staticmethod
    def getPosteByCode(other_code: str):
        if Poste.objects.filter(other_code=other_code).exists():
            p = Poste.objects.filter(other_code=other_code).first()
            cur_poste = PosteMeteor(p.meteor)
            return cur_poste
        else:
            return None

    @staticmethod
    def getOvpfStations():
        ovpf_postes = []
        tmp_postes = Poste.objects.filter(data_source=3).all()
        for p in tmp_postes:
            ovpf_postes.append({'id': p.id, 'meteor': p.meteor.lower(), 'last_obs_date_local': p.last_obs_date_local if p.last_obs_date_local is not None else datetime(2007,1,1,0,0,0)})
        return ovpf_postes

    def __str__(self) -> None:
        """print myself"""
        return "PosteMeteor id: " + str(self.data.id) + ", meteor: " + self.data.meteor
