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
            """ load our instance from db, load exclusions at date_histo """
            if Mesure.objects.filter(id=key).exists():
                self.data = Mesure.objects.get(id=key)
            else:
                self.data = Mesure()
        else:
            """ load our instance from db, load exclusions at date_histo """
            if Mesure.objects.filter(json_input=key).exists():
                self.data = Mesure.objects.get(json_input=key)
            else:
                self.data = Mesure()
                self.data.json_input = key

    def save(self):
        """ save Poste and Exclusions """
        self.data.save()

    @staticmethod
    def getAllDecas():
        if hasattr(MesureMeteor, "all_decas") is False:
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
                'valdk': a_data['val_deca'],
                'min': a_data['min'],
                'mindk': a_data['min_deca'],
                'max': a_data['max'],
                'maxdk': a_data['max_deca'],
                'isavg': a_data['is_avg'],
                'iswind': a_data['is_wind'],
                'zero': a_data['allow_zero'],
                'ommidx': None
            }
            if a_data['omm_link'] is not None and a_data['omm_link'] != 0:
                idx_mesure = len(def_mesures) - 1
                while idx_mesure >= 0:
                    if def_mesures[idx_mesure]['id'] == a_data['omm_link']:
                        m_item['ommidx'] = idx_mesure
                        idx_mesure = 0
                    idx_mesure -= 1
            def_mesures.append(m_item)
        self.load_all_decas(def_mesures)
        MesureMeteor.all_defs = def_mesures

    def load_all_decas(self, def_mesures):
        decas = [0]
        for a_mesure in def_mesures:
            if a_mesure['valdk'] not in decas:
                decas.append(a_mesure['valdk'])
            # if a_mesure['mindk'] != 0 and a_mesure['mindk'] not in decas:
            #     decas.append(a_mesure['mindk'])
            # if a_mesure['maxdk'] != 0 and a_mesure['maxdk'] not in decas:
            #     decas.append(a_mesure['maxdk'])
        MesureMeteor.all_decas = decas

    def __str__(self):
        """print myself"""
        return "MesureMeteor id: " + str(self.data.id) + ", name: " + str(self.name)
