from app.models import Mesure


class MesureMeteor():
    """
        MesureMeteor

        gere les objets Mesure

        o=MesureMeteor(id_mesure)
        0=MesureMeteor(json_key)
    """

    def __init__(self, key):
        """Init a new MesureMeteor object"""

        # Load Mesure definitions and decas
        if hasattr(MesureMeteor, "all_decas") is False:
            self.loadMesureDefs()

        if 'int' in str(type(key)):
            """ load our instance from db """
            if Mesure.objects.filter(id=key).exists():
                self.data = Mesure.objects.get(id=key)
            else:
                self.data = Mesure()
        else:
            """ load our instance from db """
            if Mesure.objects.filter(json_input=key).exists():
                self.data = Mesure.objects.get(json_input=key)
            else:
                self.data = Mesure()
                self.data.json_input = key

    def save(self):
        """ save Poste """
        self.data.save()

    @staticmethod
    def getAllDecas():
        if hasattr(MesureMeteor, "all_decas") is False:
            # Dummy call to load mesures in cache
            MesureMeteor('out_temp')
        return MesureMeteor.all_decas

    @staticmethod
    def getDefinitions():
        if hasattr(MesureMeteor, "all_defs") is False:
            MesureMeteor('out_temp')
        return MesureMeteor.all_defs

    def loadMesureDefs(self):
        def_mesures = []
        m_data = Mesure.objects.order_by('id').values()
        for a_data in m_data:
            m_item = {
                'id': a_data['id'],
                'name': a_data['name'],
                'col': a_data['json_input'],
                'col2': a_data['json_input_bis'],
                'field': a_data['archive_col'],
                "csv_field": None,
                'min': a_data['min'],
                'max': a_data['max'],
                'isavg': a_data['is_avg'],
                'iswind': a_data['is_wind'],
                'zero': a_data['allow_zero']
            }

            def_mesures.append(m_item)
        MesureMeteor.all_defs = def_mesures

    def __str__(self):
        """print myself"""
        return "MesureMeteor id: " + str(self.data.id) + ", name: " + str(self.name)
