# check __reverse_delta_values (j_xtreme)
#
from app.models import Observation, Code_QA
from datetime import datetime
from enum import Enum



class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    CodeQA = Code_QA

    def __init__(self, obs_id: int):
        if 'int' in '{0}'.format(type(obs_id)) and Observation.objects.filter(id=obs_id).exists():
            self.data = Observation.objects.filter(id=obs_id).first()
        else:
            self.data = Observation()

    def save(self):
        """ save Poste and Exclusions """
        self.data.save()

    def delete(self):
        # delete cascade implemented as a delete trigger
        self.data.delete()

    @staticmethod
    def countObsForAMesure(poste_id: int, dt_obs: datetime, mid):
        return Observation.objects.filter(poste_id=poste_id).filter(mesure_id=mid).filter(date_utc=dt_obs).count()

    @staticmethod
    def count_obs_poste_local(poste_id: int, dt_obs: datetime):
        return Observation.objects.filter(poste_id=poste_id).filter(date_local=dt_obs).count()

    @staticmethod
    def load_obs(poste_id: int, dt_obs: datetime):
        return Observation.objects.filter(poste_id=poste_id).filter(date_local=dt_obs).first()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + '{0}'.format(self.data.id) + ", poste_id: " + '{0}'.format(self.data.poste_id) + ", date locale: " + '{0}'.format(self.data.date_local) + ", duration: " + '{0}'.format(self.data.duration)
