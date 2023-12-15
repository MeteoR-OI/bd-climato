from app.models import Poste


class PosteMeteor:
    """
        PosteMeteor

        objets Poste metier

        p1=PosteMeteor(1) -> recupere le poste id = 1
        p2=PosteMeteor("BBF015") -> recupere le poste meteor BBF015
    """

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
    def getPosteIdAndTzByMeteor(meteor: str):
        if Poste.objects.filter(meteor=meteor).exists():
            p = Poste.objects.filter(meteor=meteor).first()
            return p.id, p.delta_timezone, p.load_json, p.stop_dat
        return None, 0, False, None

    def __str__(self):
        """print myself"""
        return "PosteMeteor id: " + str(self.data.id) + ", meteor: " + self.data.meteor
