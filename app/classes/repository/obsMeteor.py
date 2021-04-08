from app.models import Observation
import datetime
import pytest
import logging
from app.tools.aggTools import calcAggDate


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture obsMeteor::enable_db_access_for_all_tests called')
    pass


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste_id: int, stop_dt_utc: datetime):
        """Init a new ObsMeteor object"""
        # todo: block if my_datetime_utc > previous dat+duration
        if Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).first()
        else:
            agg_start_dat = calcAggDate('H', stop_dt_utc, 0, True)
            self.data = Observation(poste_id_id=poste_id, stop_dat=stop_dt_utc, duration=0, agg_start_dat=agg_start_dat, j={}, j_agg={})

    @staticmethod
    def getById(id: int):
        if Observation.objects.filter(id=id).exists():
            my_obs = Observation.objects.filter(id=id).first()
            return ObsMeteor(my_obs.poste_id_id, my_obs.stop_dat)
        raise Exception('obsMeteor', 'no data for id: ' + str(id))

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j != {} or self.data.j_agg != {}:
            self.data.agg_start_dat = calcAggDate('H', self.data.stop_dat, 0, True)
            self.data.save()

    def count(self, poste_id: int = None, stop_dat_mask: str = '') -> int:
        # return count of aggregations
        if poste_id is None:
            return Observation.objects.filter(stop_dat__contains=stop_dat_mask).count()
        return Observation.objects.filter(poste_id=poste_id).filter(stop_dat__contains=stop_dat_mask).count()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
