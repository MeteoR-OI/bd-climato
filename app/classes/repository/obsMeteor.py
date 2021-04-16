from app.models import Observation, TmpObservation
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

    def __init__(self, poste_id: int, stop_dt_utc: datetime, is_tmp: bool = None):
        """Init a new ObsMeteor object"""
        # todo: block if my_datetime_utc > previous dat+duration
        myObsObj = self.getObsObject(is_tmp)
        if myObsObj.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = myObsObj.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).first()
            self.is_tmp = is_tmp
        else:
            agg_start_dat = calcAggDate('H', stop_dt_utc, 0, True)
            self.data = myObsObj(poste_id_id=poste_id, stop_dat=stop_dt_utc, duration=0, agg_start_dat=agg_start_dat, j={}, j_agg={})
            self.is_tmp = is_tmp

    def getObsObject(self, is_tmp: bool = None):
        """get the aggregation depending on the level"""
        if is_tmp is None:
            raise Exception('ObsMeteor::getObsObject', 'is_tmp is not given')

        if is_tmp is False:
            return Observation
        return TmpObservation

    @staticmethod
    def getById(id: int, is_tmp: bool = None):
        myObsObj = ObsMeteor.getObsObject(None, is_tmp)
        if myObsObj.objects.filter(id=id).exists():
            my_obs = myObsObj.objects.filter(id=id).first()
            return ObsMeteor(my_obs.poste_id_id, my_obs.stop_dat)
        raise Exception('obsMeteor', 'no data for id: ' + str(id))

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j != {} or self.data.j_agg != {}:
            self.data.agg_start_dat = calcAggDate('H', self.data.stop_dat, 0, True)
            self.data.save()

    def count(self, poste_id: int = None, stop_dat_mask: str = '', is_tmp: bool = None) -> int:
        # return count of aggregations
        myObsObj = self.getObsObject(is_tmp)
        if poste_id is None:
            return myObsObj.objects.filter(stop_dat__contains=stop_dat_mask).count()
        return myObsObj.objects.filter(poste_id=poste_id).filter(stop_dat__contains=stop_dat_mask).count()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
