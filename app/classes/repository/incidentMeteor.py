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
    def new(source: str, level: str, reason: str, details: json):
        """Init a new IncidentMeteor object"""
        my_incident = IncidentMeteor(-1)
        my_incident.data.source = source
        my_incident.data.level = level
        my_incident.data.reason = reason
        my_incident.data.details = details
        my_incident.data.active = True
        my_incident.save()

    def save(self):
        """ save or delete our ExtremeTodo """
        if self.data.active is False:
            self.data.delete()
        else:
            # change datetime to string...
            self.data.details = self.fix_json(self.data.details)
            self.data.save()

    def fix_json(self, j: json):
        clean_j = {}
        # change datetime to string...
        for ki in j.keys():
            j_type = str(type(j[ki]))
            if "datetime" in j_type:
                clean_j[ki] = str(j[ki])
                continue
            if "class 'dict" in j_type:
                clean_j[ki] = self.fix_json(j[ki])
                continue
            clean_j[ki] = j[ki]
        return clean_j

    def __str__(self):
        """print myself"""
        ret = "Incident id: " + str(self.data.id) + ", dat: " + str(self.data.date_utc) + ", source: " + str(self.data.source)
        ret += ", level: " + self.data.level + ", reason: " + str(self.data.reason)
        return ret
