from app.models import AggTodo, TmpAggTodo
from app.tools.modelTools import getAggTodoObject
from django.db import transaction


class AggTodoMeteor():
    """
        AggTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, obs_id: int, is_tmp: bool = None):
        """Init a new AggTodoMeteor object"""

        myModelObj = getAggTodoObject(is_tmp)
        self.is_tmp = is_tmp
        if myModelObj.objects.filter(obs_id=obs_id).exists():
            self.data = myModelObj.objects.filter(obs_id=obs_id).first()
            self.exist_in_db = True
        else:
            self.data = myModelObj(obs_id=obs_id, priority=9, j_dv=[])
            self.exist_in_db = False

    def save(self):
        """ save or delete our AggTodo """
        if self.data.j_error.__len__() > 0 or self.data.j_dv.__len__() > 0:
            self.data.save()
        else:
            if self.exist_in_db:
                self.data.delete()

    def delete(self):
        if self.exist_in_db:
            self.data.delete()

    @staticmethod
    def count(is_tmp: bool = None):
        if is_tmp is not None:
            return getAggTodoObject(is_tmp).objects.count()
        count_all = getAggTodoObject(True).objects.count()
        return getAggTodoObject(False).objects.count() + count_all
    
    def ReportError(self, err):
        self.status = 9
        self.data.j_error = {"Error": repr(err)}
        self.save()

    @staticmethod
    @transaction.atomic
    def popOne(is_tmp: bool = None):
        myModelObj = AggTodo if is_tmp is False else TmpAggTodo
        if myModelObj.objects.filter(status=0).count() == 0:
            return None
        a_todo = myModelObj.objects.filter(status=0).order_by("priority", "id").select_for_update(skip_locked=True).first()
        a_todo.status = 1
        a_todo.save()
        agg_todo = AggTodoMeteor(a_todo.obs_id, is_tmp)
        return agg_todo

    def __str__(self):
        """print myself"""
        return "AggTodo id: " + str(self.data.id) + ", obs: " + str(self.data.obs_id) + ", poste: " + str(self.data.obs_id.poste_id) + ", on " + str(self.data.obs_id.stop_dat)
