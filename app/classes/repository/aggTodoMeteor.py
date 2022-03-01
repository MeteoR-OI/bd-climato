from app.models import AggTodo, Observation
from app.tools.modelTools import getAggTodoObject
from django.db import transaction


class AggTodoMeteor():
    """
        AggTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, id: int, json_type: str):
        """Init a new AggTodoMeteor object"""

        if AggTodo.objects.filter(id=id).exists():
            self.data = AggTodo.objects.filter(id=id).first()
        else:
            self.data = AggTodo(id=id, priority=9, json_type=json_type, j=[])

    def save(self):
        """ save or delete our AggTodo """
        self.data.save()

    def delete(self):
        self.data.delete()

    @staticmethod
    def count(is_tmp: bool = None):
        return getAggTodoObject(False).objects.count()

    def ReportError(self, err):
        self.status = 9
        self.data.j_error = {"Error": repr(err)}
        self.save()

    @staticmethod
    @transaction.atomic
    def popOne(is_tmp: bool = None):
        if AggTodo.objects.filter(status=0).count() == 0:
            return None
        a_todo = AggTodo.objects.filter(status=0).order_by("priority", "id").select_for_update(skip_locked=True).first()
        a_todo.status = 1
        a_todo.save()
        agg_todo = AggTodoMeteor(a_todo.id, is_tmp)
        agg_todo.obs = Observation.objects.filter(id=a_todo.id).first()
        return agg_todo

    def __str__(self):
        """print myself"""
        return "AggTodo id: " + str(self.data.id) + ", obs: " + str(self.data.id)
