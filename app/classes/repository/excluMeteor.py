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

        try:
            if Exclusion.objects.filter(poste_id_id=poste_id).filter(type_instrument=type_instrument_id).exists():
                self.data = Exclusion.objects.filter(poste_id_id=poste_id).filter(
                    type_instrument=type_instrument_id).first()
            else:
                self.data = Exclusion(
                    poste_id=poste_id, type_instrument=type_instrument_id)
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    @staticmethod
    def getAllForAPoste(
        poste_id: int,
        start_date: datetime = datetime.datetime.now(datetime.timezone.utc),
        end_date: datetime = datetime.datetime(2100, 12, 21, 0, 0, 0, 0, datetime.timezone.utc)
    ) -> json:
        return Exclusion.objects.filter(poste_id_id=poste_id).filter(start_x__lte=start_date).filter(end_x__lte=end_date).values('type_instrument', 'value')

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
        return "ExcluMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", typeInstrument: " + str(self.data.type_instrument.id)
