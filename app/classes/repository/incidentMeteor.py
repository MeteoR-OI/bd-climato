from app.models import Incident
import datetime
import json


class IncidentMeteor():
    """
        IncidentMeteor

        obj.data -> datarow
    """

    def __init__(self, id: int):
        """Init a new IncidentMeteor object"""
        self.data = Incident.objects.filter(id=id).first()
        if self.data is None:
            self.data = Incident(dat=datetime.datetime.today(), source="??", level="??", reason="??", j={}, active=False)

    @staticmethod
    def new(source: str, level: str, reason: str, j: json):
        """Init a new IncidentMeteor object"""
        my_incident = IncidentMeteor(-1)
        my_incident.data.source = source
        my_incident.data.level = level
        my_incident.data.reason = reason
        my_incident.data.j = j
        my_incident.data.active = True
        my_incident.save()

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
