from app.models import Mesure, Aggreg_Type


class MesureData:
    id = 0
    name = None
    json_input = None
    json_input_bis = None
    archive_col = None
    archive_table = None
    field_dir = None
    min = None
    max = None
    agreg_type = None
    is_wind = None
    allow_zero = None
    convert = None
    j = None

class MesureSQL():
    """
        MesureSQL

        gere les objets Mesure

        o=MesureSQL(id_mesure)
        0=MesureSQL(json_key)
    """
    AgregationType = Aggreg_Type
    select_sql = 'select id, name, json_input, json_input_bis, archive_col, archive_table, field_dir, min, max, agreg_type, is_wind, allow_zero, convert, j from mesures '

    def __init__(self, pg_cur, key):
        # Load Mesure definitions and decas
        if hasattr(MesureSQL, "all_defs") is False:
            self.loadMesureDefs(pg_cur)

        if key == 'no_load':
            return

        """ load our instance from db """
        if 'int' in '{0}'.format(type(key)):
            self.data = Mesure()
            self.data.id = 0
            pg_cur.execute(self.select_sql + ' where id = %s', (key,))
        else:
            self.data = Mesure()
            self.data.json_input = key
            self.data.id = 0
            pg_cur.execute(self.select_sql + ' where json_input = %s', (key,))
            
        row = pg_cur.fetchall()
        if len(row) > 0:
            row = row[0]  # Extract the first row from the result
            self.data.id = row['id']
            self.data.name = row['name']
            self.data.json_input = row['json_input']
            self.data.json_input_bis = row['json_input_bis']
            self.data.archive_col = row['archive_col']
            self.data.archive_table = row['archive_table']
            self.data.field_dir = row['field_dir']
            self.data.min = row['min']
            self.data.max = row['max']
            self.data.agreg_type = row['agreg_type']
            self.data.is_wind = row['is_wind']
            self.data.allow_zero = row['allow_zero']
            self.data.convert = row['convert']
            self.data.j = row['j']

    def save(self):
        """ save Poste """
        raise Exception("Not implemented")

    @staticmethod
    def getDefinitions(pg_cur):
        if hasattr(MesureSQL, "all_defs") is False:
            MesureSQL(pg_cur, 'no_load')
        return MesureSQL.all_defs

    def loadMesureDefs(self, pg_cur):
        def_mesures = []
        pg_cur.execute(self.select_sql)
        m_data = pg_cur.fetchall()
        for a_data in m_data:
            m_item = {
                'id': a_data[0],
                'name': a_data[1],
                'json_input': a_data[2],
                'json_input_bis': a_data[3],
                'archive_col': a_data[4],
                'archive_table': a_data[5],
                'field_dir': a_data[6],
                'min': a_data[7],
                'max': a_data[8],
                'agreg_type': a_data[9],
                'is_wind': a_data[10],
                'allow_zero': a_data[11],
                'convert': a_data[12],
                'j': a_data[13],
                'diridx': None
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

        MesureSQL.all_defs = def_mesures

    def __str__(self):
        """print myself"""
        return "MesureSQL id: " + '{0}'.format(self.data.id) + ", name: " + '{0}'.format(self.name)
