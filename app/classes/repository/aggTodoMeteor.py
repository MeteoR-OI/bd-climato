from app.models import Agg_todo, Observation
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

        if Agg_todo.objects.filter(obs_id=obs_id).exists():
            self.data = Agg_todo.objects.filter(obs_id=obs_id).first()
            self.exist_in_db = True
        else:
            if Observation.objects.filter(id=obs_id).exists() is False:
                raise Exception('aggTodo', 'cannot get AggTodo for a non existing observation')
            o = Observation(obs_id)
            self.data = Agg_todo(poste_id_id=o.pid, stop_dat=o.stop_dat, obs_id_id=obs_id, j_dv=[])
            self.exist_in_db = False

    def save(self):
        """ save or delete our AggTodo """
        if self.data.j_dv.__len__() > 0:
            self.data.save()
        else:
            if self.exist_in_db:
                Agg_todo.objects.delete()

    def __str__(self):
        """print myself"""
        return "Agg_todo id: " + str(self.id) + ", obs: " + str(self.obs_id) + ", poste: " + str(self.poste_id) + ", on " + str(self.stop_dat)
