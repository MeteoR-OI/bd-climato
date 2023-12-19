# check __reverse_delta_values (j_xtreme)
#
from app.models import Observation
from datetime import datetime


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, obs_id: int):
        if 'int' in str(type(obs_id)) and Observation.objects.filter(id=obs_id).exists():
            self.data = Observation.objects.filter(id=obs_id).first()
        else:
            self.data = Observation()

    def save(self):
        """ save Poste and Exclusions """
        if self.data.id is not None:
            self.data.qa_modifications += 1
        self.data.save()

    def delete(self):
        # delete cascade implemented as a delete trigger
        self.data.delete()

    @staticmethod
    def count_obs_poste_utc(poste_id: int, dt_obs: datetime):
        return Observation.objects.filter(poste_id=poste_id).filter(date_utc=dt_obs).count()

    @staticmethod
    def count_obs_poste_local(poste_id: int, dt_obs: datetime):
        return Observation.objects.filter(poste_id=poste_id).filter(date_local=dt_obs).count()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", time: " + str(self.data.time)
