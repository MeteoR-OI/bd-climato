from app.models import Observation
from app.tools.jsonPlus import JsonPlus
import datetime
import pytz
import pytest
import logging


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
            JsonPlus().deserialize(self.data.j)
        else:
            tmp_dat = datetime.datetime(1900, 1, 1, 0, 0, tzinfo=pytz.UTC)
            self.data = Observation(poste_id_id=poste_id, start_dat=tmp_dat, stop_dat=stop_dt_utc, duration=0, j={}, j_agg={})

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j != {} or self.data.j_agg != {}:
            if self.data.start_dat == datetime.datetime(1900, 1, 1, 0, 0, tzinfo=pytz.UTC):
                if self.data.duration == 0:
                    raise Exception('obsMeteor', 'duration is null with data loaded')
                measure_duration = datetime.timedelta(minutes=int(self.my_obs.data.duration))
                self.my_obs.data.start_dat = self.my_obs.data.stop_dat - measure_duration
            JsonPlus().serialize(self.data.j)
            self.data.save()
            JsonPlus().deserialize(self.data.j)

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
