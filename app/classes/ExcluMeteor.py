from app.models import Exclusion, Poste, TypeInstrument
from app.classes.posteMeteor import PosteMeteor
from app.classes.typeInstrumentMeteor import TypeInstrumentMeteor
import datetime
import json

class ExcluMeteor():
    """
        ExcluMeteor

        gere les objets Observation metier

        o=ExcluMeteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste: Poste, type_instrument: TypeInstrument):
        """Init a new ExcluMeteor object"""

        try:
            if Exclusion.objects.filter(poste_id_id=poste.id).filter(type_instrument=type_instrument).exists():
                self.data = Exclusion.objects.filter(poste_id_id=poste.id).filter(
                    type_instrument=type_instrument).first()
            else:
                self.data = Exclusion(
                    poste_id=poste, type_instrument=type_instrument)
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    @staticmethod
    def getAllForAPoste(poste_meteor: PosteMeteor, my_date: datetime = datetime.datetime.now(datetime.timezone.utc)) -> json:
        return Exclusion.objects.filter(poste_id_id=poste_meteor.data.id).filter(start_x_gt=my_date).filter(end_x__lt=my_date).values('type_instrument', 'value')

    def save(self):
        """ save Poste and Exclusions """
        try:
            self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "ExcluMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", typeInstrument: " + str(self.data.type_instrument.id)
