from app.models import TypeInstrument


class TypeInstrumentMeteor():
    """
        TypeInstrumentMeteor

        gere les objets TypeInstrument metier

        o=TypeInstrumentMeteor(type_instrument_id)
        o.me -> TypeInstrument object (data, methods...)

    """

    def __init__(self, type_instrument_id: int):
        """Init a new TypeInstrumentMeteor object"""

        try:
            if TypeInstrument.objects.filter(id=type_instrument_id).exists():
                self.me = TypeInstrument.objects.get(id=type_instrument_id)
            else:
                self.me = TypeInstrument()
                self.me.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

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
        return "TypeInstrumentMeteor id: " + str(self.me.id) + ", name: " + str(self.me.name)
