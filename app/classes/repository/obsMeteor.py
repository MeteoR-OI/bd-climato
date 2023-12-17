# check __reverse_delta_values (j_xtreme)
#
from app.models import Observation, Poste
import json
from datetime import datetime, timedelta


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
    def load_all_needed_obs(poste_id: int, decas: json, dt_obs: datetime, poste_tz: int):
        all_obs = []
        for a_deca in decas:
            dt_to_find = dt_obs + timedelta(hours=a_deca)
            if Observation.objects.filter(poste_id=poste_id).filter(dt_local=dt_to_find).exists():
                tmp_obs = Observation.objects.filter(poste_id=poste_id).filter(dt_local=dt_to_find).first()
                new_obs = ObsMeteor(tmp_obs.id)
            else:
                new_obs = ObsMeteor(0)
                new_obs.data.poste = Poste.objects.filter(id=poste_id).first()
                if new_obs.data.poste is None:
                    raise Exception('invalid poste_id')
                new_obs.data.dt_local = dt_to_find
                new_obs.data.dt_utc = dt_to_find - timedelta(hours=poste_tz)

            all_obs.append({'deca': a_deca, 'obs': new_obs})
        return all_obs

    @staticmethod
    def count_obs_poste_date(self, poste_id: int, dt_obs: datetime):
        return Observation.objects.filter(poste_id=poste_id).filter(dt_local=dt_obs).count()
    
    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", time: " + str(self.data.time)
