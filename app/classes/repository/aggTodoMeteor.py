from app.tools.dateTools import date_to_str, str_to_date
from app.models import Agg_todo
from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.jsonPlus import JsonPlus
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture Agg_todoMeteor::enable_db_access_for_all_tests called')
    pass


class AggTodoMeteor():
    """
        AggTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, obs_id: int):
        """Init a new Agg_todoMeteor object"""

        if Agg_todo.objects.filter(obs_id_id=obs_id).exists():
            self.data = Agg_todo.objects.filter(obs_id=obs_id).first()
            self.exist_in_db = True
        else:
            o = ObsMeteor.getById(obs_id)
            self.data = Agg_todo(poste_id=o.data.poste_id, stop_dat=o.data.stop_dat, obs_id_id=obs_id, j_dv=[])
            self.exist_in_db = False

    def save(self):
        """ save or delete our AggTodo """
        if self.data.j_dv.__len__() > 0:
            for a_jdv in self.data.j_dv:
                JsonPlus().serialize(a_jdv)
            self.data.stop_dat = date_to_str(self.data.stop_dat)
            self.data.save()
            for a_jdv in self.data.j_dv:
                JsonPlus().deserialize(a_jdv)
            self.data.stop_dat = str_to_date(self.data.stop_dat)
        else:
            if self.exist_in_db:
                Agg_todo.objects.delete()

    def __str__(self):
        """print myself"""
        return "Agg_todo id: " + str(self.id) + ", obs: " + str(self.obs_id) + ", poste: " + str(self.poste_id) + ", on " + str(self.stop_dat)
