from app.models import Observation
from app.tools.jsonPlus import JsonPlus
import datetime
import pytest
import logging
from app.tools.dateTools import date_to_str, str_to_date
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
        stop_dt_utc = date_to_str(stop_dt_utc)
        if Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).first()
            self.data.agg_start_dat = str_to_date(self.data.agg_start_dat)
            self.data.stop_dat = str_to_date(self.data.stop_dat)
            JsonPlus().deserialize(self.data.j)
        else:
            agg_start_dat = calcAggDate('H', str_to_date(stop_dt_utc), 0, True)
            self.data = Observation(poste_id_id=poste_id, stop_dat=stop_dt_utc, duration=0, agg_start_dat=agg_start_dat, j={}, j_agg={})
            self.data.agg_start_dat = str_to_date(self.data.agg_start_dat)
            self.data.stop_dat = str_to_date(self.data.stop_dat)

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j != {} or self.data.j_agg != {}:
            self.data.agg_start_dat = calcAggDate('H', self.data.stop_dat, 0, True)
            self.data.stop_dat = date_to_str(self.data.stop_dat)
            self.data.agg_start_dat = date_to_str(self.data.agg_start_dat)
            if self.data.j != {}:
                JsonPlus().serialize(self.data.j)
            if self.data.j_agg != {}:
                for a_jagg in self.data.j_agg:
                    JsonPlus().serialize(a_jagg)
            self.data.save()
            self.data.agg_start_dat = str_to_date(self.data.agg_start_dat)
            self.data.stop_dat = str_to_date(self.data.stop_dat)
            if self.data.j != {}:
                JsonPlus().deserialize(self.data.j)
            if self.data.j_agg != {}:
                for a_jagg in self.data.j_agg:
                    JsonPlus().deserialize(a_jagg)

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
