from app.models import ExtremeTodo, TmpExtremeTodo
import datetime
import pytest
import app.tools.myTools as t


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # t.logInfo('fixture ExtremeTodoMeteor::enable_db_access_for_all_tests called')
    pass


class ExtremeTodoMeteor():
    """
        ExtremeTodoMeteor

        obj.data -> datarow
    """

    def __init__(self, poste_id: int, agg_niveau: str, start_dat: datetime, invalid_type: str):
        """Init a new ExtremeTodoMeteor object"""

        if agg_niveau.__len__() > 1:
            self.data = TmpExtremeTodo(poste_id_id=poste_id, level=agg_niveau, start_dat=start_dat, invalid_type=invalid_type, j_invalid={})
        else:
            self.data = ExtremeTodo(poste_id_id=poste_id, level=agg_niveau, start_dat=start_dat, invalid_type=invalid_type, j_invalid={})

    def save(self):
        """ save or delete our ExtremeTodo """
        if self.data.j_invalid != {}:
            self.data.save()

    def __str__(self):
        """print myself"""

        if self.level.__len__() > 1:
            return "TmpExtremeTodo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type
        return "ExtremeTodo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type
