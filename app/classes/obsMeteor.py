from app.models import Observation
from app.tools.jsonPlus import JsonPlus
import datetime


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste_id: int, dt_utc: datetime):
        """Init a new ObsMeteor object"""
        # todo: block if my_datetime_utc > previous dat+duration
        try:
            if Observation.objects.filter(poste_id_id=poste_id).filter(dat=dt_utc).exists():
                self.data = Observation.objects.filter(poste_id_id=poste_id).filter(dat=dt_utc).first()
                JsonPlus().deserialize(self.data.j)
            else:
                self.data = Observation(poste_id_id=poste_id, dat=dt_utc, last_rec_dat=dt_utc, duration=0, j={})
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def save(self):
        """ save Poste and Exclusions """
        try:
            if self.data.j != {}:
                JsonPlus().serialize(self.data.j)
            self.data.save()
            JsonPlus().deserialize(self.data.j)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
