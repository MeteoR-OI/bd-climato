from app.models import Extreme_todo
import datetime
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture Agg_todoMeteor::enable_db_access_for_all_tests called')
    pass


class ExtremeTodoMeteor():
    """
        ExtremeTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, poste_id: int, agg_niveau: str, start_dat: datetime, invalid_type: str):
        """Init a new Agg_todoMeteor object"""

        self.data = Extreme_todo(poste_id_id=poste_id, level=agg_niveau, start_dat=start_dat, invalid_type=invalid_type, j_invalid={})

    def save(self):
        """ save or delete our ExtremeTodo """
        if self.data.j_invalid != {}:
            self.data.save()

    def __str__(self):
        """print myself"""
        return "Extreme_todo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type
