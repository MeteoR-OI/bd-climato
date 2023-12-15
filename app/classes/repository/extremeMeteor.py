# check __reverse_delta_values (j_xtreme)
#
from app.models import Extreme, Poste, Mesure
from datetime import timedelta


class ExtremeMeteor():
    """
        ExtremeMeteor

        gere les objets Extreme metier

        o=ExtremeMeteor(id)
    """

    def __init__(self, extreme_id: int):
        if Extreme.objects.filter(id=extreme_id).exists():
            self.data = Extreme.objects.filter(id=extreme_id).first()
        else:
            self.data = Extreme()

    def save(self):
        """ save Poste """
        # we only save if there is some data
        self.data.save()

    def delete(self):
        # delete cascade linked agg_histo rows
        self.data.delete()

    @staticmethod
    def get_extreme(pid, mid, j_dat):
        if Extreme.objects.filter(poste_id=pid).filter(mesure_id=mid).filter(date_local=j_dat).exists():
            tmp_x = Extreme.objects.filter(poste_id=pid).filter(mesure_id=mid).filter(date_local=j_dat).first()
            return ExtremeMeteor(tmp_x.id)

        new_x = ExtremeMeteor(0)
        new_x.data.poste = Poste.objects.filter(id=pid).first()
        if new_x.data.poste is None:
            raise Exception('invalid poste_id: ' + str(pid))
        new_x.data.date_local = j_dat
        new_x.data.mesure = Mesure.objects.filter(id=mid).first()
        if new_x.data.mesure is None:
            raise Exception('invalid mesure_id: ' + str(mid))
        return new_x

    @staticmethod
    def get_recent(pid, lower_dt, min_dk=0):
        lower_dt = lower_dt + timedelta(hours=min_dk)
        return Extreme.objects.filter(poste_id=pid).filter(date_local__gt=lower_dt).all()

    def __str__(self):
        """print myself"""
        return "ExtremeMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", mesure: " + str(self.data.mesure_id) + ", time: " + str(self.data.date_local)
