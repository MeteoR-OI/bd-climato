from app.models import Observation
from app.tools.jsonPlus import JsonPlus
import datetime
import pytz
import pytest
import logging
from django.utils import timezone


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
        current_tz = timezone.get_current_timezone()
        if Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = Observation.objects.filter(poste_id_id=poste_id).filter(stop_dat=stop_dt_utc).first()
            current_tz.normalize(self.data.start_dat)
            current_tz.normalize(self.data.stop_dat)
            JsonPlus().deserialize(self.data.j)
        else:
            tmp_dat = datetime.datetime(1900, 1, 1, 0, 0)
            tmp_dat = pytz.timezone('Indian/Reunion').localize(tmp_dat, is_dst=None)
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
            if self.data.j != {}:
                JsonPlus().serialize(self.data.j)
            if self.data.j_agg != {}:
                for a_jagg in self.data.j_agg:
                    JsonPlus().serialize(a_jagg)
            self.data.save()
            if self.data.j != {}:
                JsonPlus().deserialize(self.data.j)
            if self.data.j_agg != {}:
                for a_jagg in self.data.j_agg:
                    JsonPlus().deserialize(a_jagg)

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat)
