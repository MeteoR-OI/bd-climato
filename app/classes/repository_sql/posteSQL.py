from app.models import Load_Type, Data_Source

class PosteData:
    id = 0
    meteor = None
    delta_timezone = None
    data_source = None
    load_type = None
    api_key = None
    type = None
    altitude = None
    lat = None
    long = None
    info = None
    stop_date = None
    last_obs_date_local = None
    last_obs_id = None
    last_json_date_local = None
    info_sync = None
    
class PosteSQL:
    """
        PosteSQL

        objets Poste metier

        p1=PosteSQL(1) -> recupere le poste id = 1
        p2=PosteSQL("BBF015") -> recupere le poste meteor BBF015
    """

    LoadType = Load_Type
    DataSource = Data_Source
    select_sql = 'select id, meteor, delta_timezone, data_source, load_type, api_key, type, altitude, lat, long, info, stop_date, last_obs_date_local, last_obs_id, last_json_date_local, info_sync from postes'

    def __init__(self, pg_cur, key):
        """ load our instance from db """
        if 'int' in '{0}'.format(type(key)):
            self.data = PosteData()
            self.data.id = 0
            pg_cur.execute(self.select_sql + ' where id = %s', (key,))
        else:
            self.data = PosteData()
            self.data.meteor = key
            self.data.id = 0
            pg_cur.execute(self.select_sql + ' where meteor = %s', (key,))
            
        row = pg_cur.fetchall()
        if len(row) > 0:
            self.data.id = row[0][0]
            self.data.meteor = row[0][1]
            self.data.delta_timezone = row[0][2]
            self.data.data_source = row[0][3]
            self.data.load_type = row[0][4]
            self.data.api_key = row[0][5]
            self.data.type = row[0][6]
            self.data.altitude = row[0][7]
            self.data.lat = row[0][8]
            self.data.long = row[0][9]
            self.data.info = row[0][10]
            self.data.stop_date = row[0][11]
            self.data.last_obs_date_local = row[0][12]
            self.data.last_obs_id = row[0][13]
            self.data.last_json_date_local = row[0][14]
            self.data.info_sync = row[0][15]

    def save(self, pg_cur):
        """ save Poste """
        raise Exception("Not implemented")

    def update_last_obs(self, pg_cur, last_obs_date_local, last_obs_id=None):
        """ update last obs """
        if last_obs_date_local is None:
            raise Exception("last_obs_date_local is None")
        self.data.last_obs_date_local = last_obs_date_local
        if last_obs_id is not None:
            self.data.last_obs_id = last_obs_id
        pg_cur.execute('update postes set last_obs_date_local = %s, last_obs_id = %s where id = %s',
                       (last_obs_date_local, last_obs_id, self.data.id)) 

    def update_last_json_date_local(self, pg_cur, last_json_date_local):
        """ update last obs """
        self.data.last_json_date_local = last_json_date_local
        pg_cur.execute('update postes set last_json_date_local = %s where id = %s', (last_json_date_local, self.data.id)) 

    def __str__(self) -> None:
        """print myself"""
        return "PosteSQL id: " + '{0}'.format(self.data.id) + ", meteor: " + self.data.meteor
