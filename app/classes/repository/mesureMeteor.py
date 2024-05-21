from app.models import Mesure, Aggreg_Type


class MesureMeteor():
    """
        MesureMeteor

        gere les objets Mesure

        o=MesureMeteor(id_mesure)
        0=MesureMeteor(json_key)
    """
    AgregationType = Aggreg_Type

    def __init__(self, key):
        """Init a new MesureMeteor object"""

        # Load Mesure definitions and decas
        if hasattr(MesureMeteor, "all_defs") is False:
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
                'table': a_data['table'],
                'diridx': a_data['field_dir'],
                'json_input': a_data['json_input'],
                'json_input_bis': a_data['json_input_bis'],
                'archive_col': a_data['archive_col'],
                'min': a_data['min'],
                'max': a_data['max'],
                'agreg_type': a_data['agreg_type'],
                'is_wind': a_data['is_wind'],
                'zero': a_data['allow_zero'],
                'convert': a_data['convert']
            }

            def_mesures.append(m_item)
        for a_mesure in def_mesures:
            if a_mesure['diridx'] is not None:
                fi_dir = a_mesure['diridx']
                a_mesure['diridx'] = None
                dir_idx = 0
                while dir_idx < len(def_mesures):
                    if def_mesures[dir_idx]['id'] == fi_dir:
                        a_mesure['diridx'] = dir_idx
                        dir_idx = len(def_mesures)
                    dir_idx += 1

        MesureMeteor.all_defs = def_mesures

    def __str__(self):
        """print myself"""
        return "MesureMeteor id: " + str(self.data.id) + ", name: " + str(self.name)
