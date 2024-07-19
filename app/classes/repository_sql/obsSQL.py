# check __reverse_delta_values (j_xtreme)
#
from app.models import Observation, Code_QA
from datetime import datetime

class ObsData:
    id = 0
    date_local = None
    date_utc = None
    poste_id = None
    duration = None
    barometer = None
    pressure = None
    in_temp = None
    out_temp = None
    dewpoint = None
    etp = None
    heatindex = None
    extra_temp1 = None
    extra_temp2 = None
    extra_temp3 = None
    in_humidity = None
    out_humidity = None
    extra_humid1 = None
    extra_humid2 = None
    leaf_temp1 = None
    leaf_temp2 = None
    leaf_wet1 = None
    leaf_wet2 = None
    radiation = None
    radiation_rate = None
    uv = None
    rain = None
    rain_utc = None
    rain_rate = None
    rx = None
    soil_moist1 = None
    soil_moist2 = None
    soil_moist3 = None
    soil_moist4 = None
    soil_temp1 = None
    soil_temp2 = None
    soil_temp3 = None
    soil_temp4 = None
    voltage = None
    wind_dir = None
    wind = None
    wind_gust_dir = None
    wind_gust = None
    wind10 = None
    wind10_dir = None
    windchill = None
    hail = None
    zone_1 = None
    zone_2 = None
    zone_3 = None
    zone_4 = None
    zone_5 = None
    zone_6 = None
    zone_7 = None
    zone_8 = None
    zone_9 = None
    zone_10 = None
    j = None
    qa_all = None
    qa_details = None
    qa_modifications = None
    
class ObsSQL():
    """
        ObsSQL

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    CodeQA = Code_QA

    select_sql = 'select id, name, table, diridx, json_input, json_input_bis, archive_col, min, max, agreg_type, is_wind, zero, convert, barometer, pressure, in_temp, out_temp, ' +\
        'dewpoint, etp, heatindex, extra_temp1, extra_temp2, extra_temp3, in_humidity, out_humidity, extra_humid1, extra_humid2, leaf_temp1, leaf_temp2, leaf_wet1, leaf_wet2, ' +\
        'radiation, radiation_rate, uv, rain, rain_utc, rain_rate, rx, soil_moist1, soil_moist2, soil_moist3, soil_moist4, soil_temp1, soil_temp2, soil_temp3, soil_temp4, voltage, ' +\
        'wind_dir, wind, wind_gust_dir, wind_gust, wind10, wind10_dir, windchill, hail, zone_1, zone_2, zone_3, zone_4, zone_5, zone_6, zone_7, zone_8, zone_9, zone_10, j, qa_all, ' +\
        'qa_details, qa_modifications from obs'

    def __init__(self, pg_cur, obs_id: int):
        """ load our instance from db """
        self.data = ObsData()
        self.data.id = 0
        pg_cur.execute(self.select_sql + ' where id = %s', (obs_id,))
            
        row = pg_cur.fetchall()
        if len(row) > 0:
            self.data.id = row[0][0]
            self.data.date_local = row[0][1]
            self.data.date_utc = row[0][2]
            self.data.poste_id = row[0][3]
            self.data.duration = row[0][4]
            self.data.barometer = row[0][5]
            self.data.pressure = row[0][6]
            self.data.in_temp = row[0][7]
            self.data.out_temp = row[0][8]
            self.data.dewpoint = row[0][9]
            self.data.etp = row[0][10]
            self.data.heatindex = row[0][11]
            self.data.extra_temp1 = row[0][12]
            self.data.extra_temp2 = row[0][13]
            self.data.extra_temp3 = row[0][14]
            self.data.in_humidity = row[0][15]
            self.data.out_humidity = row[0][16]
            self.data.extra_humid1 = row[0][17]
            self.data.extra_humid2 = row[0][18]
            self.data.leaf_temp1 = row[0][19]
            self.data.leaf_temp2 = row[0][20]
            self.data.leaf_wet1 = row[0][21]
            self.data.leaf_wet2 = row[0][22]
            self.data.radiation = row[0][23]
            self.data.radiation_rate = row[0][24]
            self.data.uv = row[0][25]
            self.data.rain = row[0][26]
            self.data.rain_utc = row[0][27]
            self.data.rain_rate = row[0][28]
            self.data.rx = row[0][29]
            self.data.soil_moist1 = row[0][30]
            self.data.soil_moist2 = row[0][31]
            self.data.soil_moist3 = row[0][32]
            self.data.soil_moist4 = row[0][33]
            self.data.soil_temp1 = row[0][34]
            self.data.soil_temp2 = row[0][35]
            self.data.soil_temp3 = row[0][36]
            self.data.soil_temp4 = row[0][37]
            self.data.voltage = row[0][38]
            self.data.wind_dir = row[0][39]
            self.data.wind = row[0][40]
            self.data.wind_gust_dir = row[0][41]
            self.data.wind_gust = row[0][42]
            self.data.wind10 = row[0][43]
            self.data.wind10_dir = row[0][44]
            self.data.windchill = row[0][45]
            self.data.hail = row[0][46]
            self.data.zone_1 = row[0][47]
            self.data.zone_2 = row[0][48]
            self.data.zone_3 = row[0][49]
            self.data.zone_4 = row[0][50]
            self.data.zone_5 = row[0][51]
            self.data.zone_6 = row[0][52]
            self.data.zone_7 = row[0][53]
            self.data.zone_8 = row[0][54]
            self.data.zone_9 = row[0][55]
            self.data.zone_10 = row[0][56]
            self.data.j = row[0][57]
            self.data.qa_all = row[0][58]
            self.data.qa_details = row[0][59]
            self.data.qa_modifications = row[0][60]

    def save(self):
        """ save Poste and Exclusions """
        raise Exception("Not implemented")

    def delete(self):
        # delete cascade implemented as a delete trigger
        raise Exception("Not implemented")

    @staticmethod
    def count_obs_poste_local(pg_cur, poste_id: int, dt_obs: datetime):
        pg_cur.execute('select count(*) from obs where poste_id = %s and date_local = %s', (poste_id, dt_obs))
        return pg_cur.fetchall()[0][0]

    def __str__(self):
        """print myself"""
        return "ObsSQL id: " + '{0}'.format(self.data.id) + ", poste_id: " + '{0}'.format(self.data.poste_id) + ", date locale: " + '{0}'.format(self.data.date_local) + ", duration: " + '{0}'.format(self.data.duration)
