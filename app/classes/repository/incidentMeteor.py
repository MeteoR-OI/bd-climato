from app.models import Incident
import datetime
import pytest
import json
# import app.tools.myTools as t


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # t.logInfo('fixture IncidentMeteor::enable_db_access_for_all_tests called')
    pass


class IncidentMeteor():
    """
        IncidentMeteor

        obj.data -> datarow
    """

    def __init__(self, id: int):
        """Init a new IncidentMeteor object"""
        if Incident.objects.exists(id=id):
            self.data = Incident.objects.filter(id=id).first()
        else:
            self.data = Incident(dat=datetime.data.today(), source="??", level="??", reason="??", j={}, active=False)

    @staticmethod
    def new(self, source: str, level: str, reason: str, j: json):
        """Init a new IncidentMeteor object"""
        my_incident = Incident()
        my_incident.data.source = source
        my_incident.data.level = level
        my_incident.data.reason = reason
        my_incident.data.j = j
        my_incident.data.active = True
        self.save()

    def save(self):
        """ save or delete our ExtremeTodo """
        if self.data.active is False:
            self.data.delete()
        else:
            self.data.save()

    def __str__(self):
        """print myself"""
        ret = "Incident id: " + str(self.data.id) + ", dat: " + str(self.data.dat) + ", source: " + str(self.data.source)
        ret += ", level: " + self.data.level + ", reason: " + str(self.data.reason)
