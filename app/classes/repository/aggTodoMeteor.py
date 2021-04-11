from app.models import Agg_todo
import pytest
import logging
from django.db import transaction


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
            self.data = Agg_todo(obs_id_id=obs_id, priority=9, j_dv=[])
            self.exist_in_db = False

    def save(self):
        """ save or delete our AggTodo """
        if self.data.j_error.__len__() > 0 or self.data.j_dv.__len__() > 0:
            self.data.save()
        else:
            if self.exist_in_db:
                Agg_todo.objects.delete()

    def delete(self):
        if self.exist_in_db:
            self.data.delete()

    def count(sef):
        return Agg_todo.objects.count()

    def ReportError(self, err):
        self.status = 9
        self.data.j_error = {"Error": err}
        self.save()

    @staticmethod
    @transaction.atomic
    def popOne():
        if Agg_todo.objects.filter(status=0).count() == 0:
            return None
        a_todo = Agg_todo.objects.filter(status=0).order_by("priority", "id").select_for_update(skip_locked=True).first()
        a_todo.status = 9
        a_todo.save()
        agg_todo = AggTodoMeteor(a_todo.obs_id_id)
        return agg_todo

    def __str__(self):
        """print myself"""
        return "Agg_todo id: " + str(self.data.id) + ", obs: " + str(self.data.obs_id_id) + ", poste: " + str(self.data.obs_id.poste_id_id) + ", on " + str(self.data.obs_id.stop_dat)
