# check __reverse_delta_values (j_xtreme)
#
from app.models import XMin, Code_QA


class xMinMeteor():
    """
        ExtremeMeteor

        gere les objets Extreme metier

        o=ExtremeMeteor(id)
    """
    CodeQA = Code_QA
    
    def __init__(self, extreme_id: int):
        if XMin.objects.filter(id=extreme_id).exists():
            self.data = XMin.objects.filter(id=extreme_id).first()
        else:
            self.data = XMin()

    def save(self):
        """ save Poste """
        # we only save if there is some data
        self.data.save()

    def delete(self):
        # delete cascade linked agg_histo rows
        self.data.delete()

    def __str__(self):
        """print myself"""
        return "Extreme Min id: " + '{0}'.format(self.data.id) + ", poste_id: " + '{0}'.format(self.data.poste_id) + ", mesure: " + '{0}'.format(self.data.mesure_id) + ", time: " + '{0}'.format(self.data.date_local)
