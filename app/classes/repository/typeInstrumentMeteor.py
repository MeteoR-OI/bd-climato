from app.models import TypeInstrument
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture typeInstrumentMeteor::enable_db_access_for_all_tests called')
    pass


class TypeInstrumentMeteor():
    """
        TypeInstrumentMeteor

        gere les objets TypeInstrument metier

        o=TypeInstrumentMeteor(type_instrument_id)
        o.data -> TypeInstrument object (data, methods...)

    """

    def __init__(self, type_instrument_id: int):
        """Init a new TypeInstrumentMeteor object"""

        if TypeInstrument.objects.filter(id=type_instrument_id).exists():
            self.data = TypeInstrument.objects.get(id=type_instrument_id)
        else:
            self.data = TypeInstrument()
            self.data.save()

    def save(self):
        """ save Poste and Exclusions """
        self.data.save()

    def __str__(self):
        """print myself"""
        return "TypeInstrumentMeteor id: " + str(self.data.id) + ", name: " + str(self.data.name)
