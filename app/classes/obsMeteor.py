from app.models import Observation, Poste
import datetime


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste: Poste, dt_utc: datetime):
        """Init a new ObsMeteor object"""
        # todo : check that my_datetime_utc > previous dat + duration pour le poste_id
        # todo: put a warning somewhere if my_datetime_utc > previous dat+duration
        # todo: what is happening if the date given is at the middle of an existing period ?
        try:
            if Observation.objects.filter(poste_id_id=poste.id).filter(dat=dt_utc).exists():
                self.data = Observation.objects.filter(
                    poste_id_id=poste.id).filter(dat=dt_utc).first()
            else:
                self.data = Observation(
                    poste_id=poste, dat=dt_utc, last_rec_dat=dt_utc, duration=0)
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def save(self):
        """ save Poste and Exclusions """
        try:
            self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
