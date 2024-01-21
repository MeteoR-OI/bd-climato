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
            self.data = Incident(date_utc=datetime.datetime.utcnow(), source="??", level="??", reason="??", details={}, active=True)

    @staticmethod
    def new(source: str, level: str, reason: str, j_details: json):
        """Init a new IncidentMeteor object"""
        my_incident = IncidentMeteor(-1)
        my_incident.data.source = source
        my_incident.data.level = level
        my_incident.data.reason = reason
        details = {}
        # change datetime to string...
        for ki in j_details.keys():
            if "datetime" in str(type(j_details[ki])):
                details[ki] = str(j_details[ki])
            else:
                details[ki] = j_details[ki]
        my_incident.data.details = details
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
        ret = "Incident id: " + str(self.data.id) + ", dat: " + str(self.data.date_utc) + ", source: " + str(self.data.source)
        ret += ", level: " + self.data.level + ", reason: " + str(self.data.reason)
        return ret
