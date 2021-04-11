from app.models import Exclusion
import datetime
import json
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture excluMeteor::enable_db_access_for_all_tests called')
    pass


class ExcluMeteor():
    """
        ExcluMeteor

        gere les objets Observation metier

        o=ExcluMeteor(poste, dat)
        o.data -> Observation object (data, methods...)

        value is a json with:
            key = measure name (ie. 'out_temp')
            value =
                'value' => keep the value from the json file
                'null'  => measure is invalid
                data    => force this data in the measure (numeric)
    """

    def __init__(self, poste_id: int, type_instrument_id: int):
        """Init a new ExcluMeteor object"""

        if Exclusion.objects.filter(poste_id_id=poste_id).filter(type_instrument=type_instrument_id).exists():
            self.data = Exclusion.objects.filter(poste_id_id=poste_id).filter(type_instrument=type_instrument_id).first()
        else:
            self.data = Exclusion(poste_id=poste_id, type_instrument=type_instrument_id)

    @staticmethod
    def getAllForAPoste(
        poste_id: int,
        measure_start_dat: datetime = datetime.datetime.now(datetime.timezone.utc),
    ) -> json:
        tmp_exlus = Exclusion.objects.filter(poste_id_id=poste_id).filter(start_dat__gte=measure_start_dat).filter(stop_dat__lte=measure_start_dat).order_by('poste_id', 'start_dat').values()
        # we only get the first in date for each type_intrument
        ret = []
        for an_exclu in tmp_exlus:
            store_in_ret = True
            for a_ret in ret:
                if a_ret['type_instrument'] == an_exclu['type_instrument']:
                    store_in_ret = False
                    break
            if store_in_ret is True:
                ret.append({'type_instrument': an_exclu['type_instrument_id'], 'value': ['value']})
        return ret

    def save(self):
        """ save Poste and Exclusions """
        self.data.save()

    def __str__(self):
        """print myself"""
        return "ExcluMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", typeInstrument: " + str(self.data.type_instrument.id)
