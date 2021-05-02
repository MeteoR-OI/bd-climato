from app.models import AggTodo, TmpAggTodo
import pytest
import app.tools.myTools as t
from django.db import transaction


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    t.logInfo('fixture AggTodoMeteor::enable_db_access_for_all_tests called')
    pass


class AggTodoMeteor():
    """
        AggTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, obs_id: int, is_tmp: bool = None):
        """Init a new AggTodoMeteor object"""

        myModelObj = self.getAggTodoObject(is_tmp)
        self.is_tmp = is_tmp
        if myModelObj.objects.filter(obs_id_id=obs_id).exists():
            self.data = myModelObj.objects.filter(obs_id=obs_id).first()
            self.exist_in_db = True
            self.is_tmp = is_tmp
        else:
            self.data = myModelObj(obs_id_id=obs_id, priority=9, j_dv=[])
            self.exist_in_db = False
            self.is_tmp = is_tmp

    def getAggTodoObject(self, is_tmp: bool = None):
        """get the aggregation depending on the level"""
        if is_tmp is None:
            raise Exception('AggTodoMeteor', 'agg_level not given')
        if is_tmp is False:
            return AggTodo
        return TmpAggTodo

    def save(self):
        """ save or delete our AggTodo """
        if self.data.j_error.__len__() > 0 or self.data.j_dv.__len__() > 0:
            self.data.save()
        else:
            if self.exist_in_db:
                myModelObj = self(self.level)
                myModelObj.objects.delete()

    def delete(self):
        if self.exist_in_db:
            self.data.delete()

    def count(self):
        if self.is_tmp is True:
            return TmpAggTodo.objects.count()
        return AggTodo.objects.count()

    def ReportError(self, err):
        self.status = 9
        self.data.j_error = {"Error": err}
        self.save()

    @staticmethod
    @transaction.atomic
    def popOne(is_tmp: bool = None):
        myModelObj = AggTodo if is_tmp is False else TmpAggTodo
        if myModelObj.objects.filter(status=0).count() == 0:
            return None
        a_todo = myModelObj.objects.filter(status=0).order_by("priority", "id").select_for_update(skip_locked=True).first()
        a_todo.status = 9
        a_todo.save()
        agg_todo = AggTodoMeteor(a_todo.obs_id_id, is_tmp)
        return agg_todo

    def __str__(self):
        """print myself"""
        return "AggTodo id: " + str(self.data.id) + ", obs: " + str(self.data.obs_id_id) + ", poste: " + str(self.data.obs_id.poste_id_id) + ", on " + str(self.data.obs_id.stop_dat)
