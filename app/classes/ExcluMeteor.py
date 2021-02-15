from app.models import Exclusion, Poste, TypeInstrument
import datetime


class ExcluMeteor():
    """
        ExcluMeteor

        gere les objets Observation metier

        o=ExcluMeteor(poste, dat)
        o.me -> Observation object (data, methods...)

    """

    def __init__(self, poste: Poste, type_instrument: TypeInstrument):
        """Init a new ExcluMeteor object"""

        try:
            if Exclusion.objects.filter(poste_id_id=poste.id).filter(type_instrument=type_instrument).exists():
                self.me = Exclusion.objects.filter(poste_id_id=poste.id).filter(type_instrument=type_instrument).first()
            else:
                self.me = Exclusion(poste_id=poste, type_instrument=type_instrument)
                self.me.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    @staticmethod
    def getAllForAPoste(poste_id):
        return Exclusion.objects.filter(poste_id_id=poste_id).filter(
                end_x__gt=datetime.datetime.now(datetime.timezone.utc)).values('type_instrument', 'value')

    def save(self):
        """ save Poste and Exclusions """
        try:
            self.me.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "ExcluMeteor id: " + str(self.me.id) + ", poste_id: " + str(self.me.poste_id.id) + ", typeInstrument: " + str(self.me.type_instrument.id)
