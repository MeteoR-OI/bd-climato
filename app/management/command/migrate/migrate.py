import mysql.connector
import psycopg2
from datetime import datetime, timedelta

# column idx in our select statement from archive table
dateTime = 0
usUnits = 1
interval = 2
barometer = 3
pressure = 4
altimeter = 5
inTemp = 6
outTemp = 7
inHumidity = 8
outHumidity = 9
windSpeed = 10
windDir = 11
windGust = 12
windGustDir = 13
rainRate = 14
rain = 15
dewpoint = 16
windchill = 17
heatindex = 18
ET = 19
radiation = 20
UV = 21
soilTemp1 = 22
rxCheckPercent = 23
consBatteryVoltage = 24


def load_data(meteor):
    myconn = None
    json_keys = []
    try:
        myconn = mysql.connector.connect(
            host="localhost",
            user="nico",
            password="Funiculi",
            database=meteor
        )
        pgconn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
        )
        if myconn.is_connected() is False:
            print("bug in db access")
            return
        my_cur = myconn.cursor()

        # set session timezone to utc
        my_cur.execute("set time_zone = '+00:00'")
        myconn.commit()
        my_cur.close()

        poste_id = get_poste_id(pgconn, meteor)
        if poste_id is None:
            print('stations ' + meteor + ' not found, bye')
            return
        print('loading db for ' + meteor + ', id: ' + str(poste_id))

        # load mesures definition in memory
        mesures = get_mesures(pgconn)
        # load omm link array, between base mesures and linked omm mesures
        omm_link = get_omm_link(mesures)

        print('start loading measures for ' + meteor)
        insert_archives(myconn, pgconn, poste_id, mesures, omm_link)

        print('start loading extremes for ' + meteor)
        insert_xtremes(meteor, pgconn, mesures, omm_link, poste_id)

        print('ok')

    except Exception as e:
        print(e)

    finally:
        if pgconn is not None:
            pgconn.close()
        if myconn is not None and myconn.is_connected():
            myconn.close()
        for j_key in json_keys:
            if j_key['db'].is_connected():
                j_key['db'].close()
        print("ok all done")


def insert_archives(myconn, pgconn, poste_id, mesures, omm_link):
    try:
        date_omm_decas = []
        my_cur = myconn.cursor()
        query_my = """
        select from_unixTime(dateTime + 4 * 3600), usUnits, `interval`, barometer, pressure, altimeter, inTemp,
               outTemp, inHumidity, outHumidity, windSpeed, windDir, windGust, windGustDir, rainRate, rain, dewpoint,
               windchill, heatindex, ET, radiation, UV, soilTemp1, rxCheckPercent, consBatteryVoltage
               from archive order by dateTime"""
        my_cur.execute(query_my)
        pg_cur = pgconn.cursor()
        query_pg = """
            insert into obs(id_poste, time, duration, out_temp, windchill, dewpoint, soiltemp, humidity, barometer,
                              pressure, wind, wind_dir, wind_gust, wind_gust_dir, rain, rain_rate, heatindex,
                              uv_indice, radiation, etp_sum, in_temp, in_humidity, rx, voltage,
                              out_temp_omm, humidity_omm, wind10_omm, rain_omm, barometer_omm) values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;"""

        # load ins_idx for omm field in our insert statement
        for an_omm_base in omm_link:
            match(an_omm_base['col']):
                case 'outTemp':
                    an_omm_base['ins_idx'] = 3
                case 'barometer':
                    an_omm_base['ins_idx'] = 8
                case 'outHumidity':
                    an_omm_base['ins_idx'] = 7
                case 'wind':
                    an_omm_base['ins_idx'] = 10
                case 'rain':
                    an_omm_base['ins_idx'] = 14
                case _:
                    raise Exception('unknown omm column: ' + an_omm_base['col'])
            for an_omm in an_omm_base['omms']:
                match(an_omm['col']):
                    case 'outTemp_omm':
                        an_omm['ins_idx'] = 24
                    case 'outHumidity_omm':
                        an_omm['ins_idx'] = 25
                    case 'wind_omm':
                        an_omm['ins_idx'] = 26
                    case 'rain_omm':
                        an_omm['ins_idx'] = 27
                    case 'barometer_omm':
                        an_omm['ins_idx'] = 28
                    case _:
                        raise Exception('unknown omm column: ' + an_omm['col'])
                if an_omm['decas'][0] not in date_omm_decas:
                    date_omm_decas.append(an_omm['decas'][0])

        row = my_cur.fetchone()
        nb_inserted = 0
        while row is not None:
            if row[usUnits] != 16:
                raise Exception('bad usUnits: ' + str(usUnits) + ', dateTime: ' + str(row[dateTime]))
            args = [
                poste_id,
                row[dateTime],
                row[interval],
                row[outTemp],
                row[windchill],
                row[dewpoint],
                row[soilTemp1],
                row[outHumidity],
                row[barometer],
                row[pressure],
                row[windSpeed],
                row[windDir],
                row[windGust],
                row[windGustDir],
                row[rain],
                row[rainRate],
                row[heatindex],
                row[UV],
                row[radiation],
                row[ET],
                row[inTemp],
                row[inHumidity],
                row[rxCheckPercent],
                row[consBatteryVoltage],
                None,
                None,
                None,
                None,
                None
            ]
            for an_omm_base in omm_link:
                for an_omm in an_omm_base['omms']:
                    if an_omm['decas'][0] == 0:
                        args[an_omm['ins_idx']] = args[an_omm_base['ins_idx']]

            pg_cur.execute(query_pg, args)
            nb_inserted += 1

            for a_deca in date_omm_decas:
                if a_deca == 0:
                    continue
                args = [
                    poste_id,
                    row[dateTime] + timedelta(hours=a_deca),
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None
                ]
                for an_omm_base in omm_link:
                    for an_omm in an_omm_base['omms']:
                        if an_omm['decas'][0] == a_deca:
                            args[an_omm['ins_idx']] = row[an_omm_base['ins_idx']]
                pg_cur.execute(query_pg, args)
                nb_inserted += 1

            if nb_inserted > 1000:
                test_id = pg_cur.fetchone()[0]
                print("   1000 archive inserted, last id: " + str(test_id))
                pgconn.commit()
                pg_cur.close()
                pg_cur = pgconn.cursor()
                nb_inserted = 0
            row = my_cur.fetchone()
        pgconn.commit()
        my_cur.close()
        pg_cur.close()
    except Exception as e:
        print(e)


def insert_xtremes(meteor, pgconn, mesures, json_keys, poste_id):
    day_process = None
    pg_cur = pgconn.cursor()
    inserted_row = 0

    try:
        json_keys = get_json_keys(mesures, meteor)
        while True:
            day_process, is_done = get_next_process_day(json_keys)
            if is_done is True:
                break
            for aj_key in json_keys:
                if aj_key['r'] is None or aj_key['ok'] is False:
                    continue
                min_val = max_val = None

                if mesures[aj_key['idx'][0]]['zero'] is False and aj_key['r'][1] == 0:
                    min_val = None
                else:
                    min_val = aj_key['r'][1]

                if mesures[aj_key['idx'][0]]['zero'] is False and aj_key['r'][3] == 0:
                    max_val = None
                else:
                    max_val = aj_key['r'][3]

                if mesures[aj_key['idx'][0]]['iswind'] is True:
                    wind_dir = aj_key['r'][5]
                else:
                    wind_dir = None

                args = [
                    poste_id,
                    day_process,
                    0,
                    0,
                    min_val,
                    None if min_val is None or aj_key['r'][2] is None else datetime.utcfromtimestamp(aj_key['r'][2]),      # min time
                    max_val,
                    None if max_val is None or aj_key['r'][4] is None else datetime.utcfromtimestamp(aj_key['r'][4]),      # max time
                    wind_dir
                ]

                idx_idx = 0
                while idx_idx < len(aj_key['idx']):
                    args[3] = mesures[aj_key['idx'][idx_idx]]['id']
                    insert_xtreme_row(mesures, pg_cur, args)
                    idx_idx += 1
                    inserted_row += 1
                    if (inserted_row % 1000) == 0:
                        pg_cur.execute('commit')
                        pg_cur.close()
                        print('   1000 extremes inserted')
                        pg_cur = pgconn.cursor()
                        inserted_row = 0

                aj_key['r'] = aj_key['c'].fetchone()

    finally:
        pg_cur.close()


# Utility functions
def get_poste_id(pgconn, meteor):
    pg_cur = pgconn.cursor()
    poste_id = None
    try:
        pg_cur.execute("select id from postes where meteor = '" + meteor + "'")
        row = pg_cur.fetchone()
        if row is not None:
            poste_id = row[0]

    except Exception as e:
        print(e)
        poste_id = None
    finally:
        pg_cur.close()
        return poste_id


def insert_xtreme_row(mesures, pg_cur, args):
    query_pg = """
        insert into extremes (id_poste, date, id_obs, id_mesure, min, mintime, max, maxtime, max_dir) values
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    pg_cur.execute(query_pg,  args)


def get_next_process_day(json_keys):
    is_done = True
    next_date = datetime.now().date()

    for aj_key in json_keys:
        if aj_key['r'] is None:
            dt_in_row = next_date
        else:
            dt_in_row = datetime.utcfromtimestamp(aj_key['r'][0]).date()

        # first_dt store the smallest date in all our rouws
        if next_date > dt_in_row:
            next_date = dt_in_row

    for aj_key in json_keys:
        if aj_key['r'] is None:
            aj_key['ok'] = False
        else:
            dt_in_row = datetime.utcfromtimestamp(aj_key['r'][0]).date()
            if dt_in_row == next_date:
                aj_key['ok'] = True
                is_done = False
            else:
                aj_key['ok'] = False
    return next_date, is_done


def get_mesures(pgconn):
    mesures = []
    pg_query = "select id, archive_col, archive_col, val_deca, min, min_deca, max, max_deca, is_avg, is_wind, allow_zero, omm_link from mesures"

    pg_cur = pgconn.cursor()
    pg_cur.execute(pg_query)
    row = pg_cur.fetchone()
    while row is not None:
        one_mesure = {
            'id': row[0],
            'col': row[1],
            'field': row[2],
            'valdk': row[3],
            'min': row[4],
            'mindk': row[5],
            'max': row[6],
            'maxdk': row[7],
            'isavg': row[8],
            'iswind': row[9],
            'zero': row[10],
            'ommidx': None
        }
        if row[11] != 0:
            idx_mesure = len(mesures) - 1
            while idx_mesure >= 0:
                if mesures[idx_mesure]['id'] == row[11]:
                    one_mesure['ommidx'] = idx_mesure
                    idx_mesure = 0
                idx_mesure -= 1
        mesures.append(one_mesure)
        row = pg_cur.fetchone()
    pg_cur.close()
    return mesures


def get_omm_link(mesures):
    omm_link = []
    m_idx = 0

    while m_idx < len(mesures):
        if mesures[m_idx]['ommidx'] is not None:
            my_mesure_idx = None
            my_omm_mesure = mesures[m_idx]
            my_mesure = mesures[my_omm_mesure['ommidx']]
            for an_omm_link in omm_link:
                if an_omm_link['base_idx'] == my_omm_mesure['ommidx']:
                    my_mesure_idx = an_omm_link
            if my_mesure_idx is None:
                my_mesure_idx = {'base_idx': my_omm_mesure['ommidx'], 'col': my_mesure['col'], 'ins_idx': -1, 'omms': []}
                omm_link.append(my_mesure_idx)
            my_mesure_idx['omms'].append({'ommidx': m_idx, 'col': my_omm_mesure['col'], 'decas': [my_omm_mesure['valdk'], my_omm_mesure['maxdk'], my_omm_mesure['mindk']], 'ins_idx': 0})
        m_idx += 1

    return omm_link


def get_json_keys(mesures, meteor):
    idx = 0
    json_keys = []
    while idx < len(mesures):
        bcont = False
        mymesure = mesures[idx]

        if (mymesure['min'] is False and mymesure['max'] is False):
            idx += 1
            continue

        if '_omm' in mymesure['col']:
            for aj_key in json_keys:
                if mesures[mymesure['ommidx']]['id'] == mesures[aj_key['idx'][0]]['id']:
                    aj_key['idx'].append(idx)
                    bcont = True

        if bcont is True:
            idx += 1
            continue

        tmp_conn = mysql.connector.connect(
            host="localhost",
            user="nico",
            password="Funiculi",
            database=meteor
        )
        if tmp_conn.is_connected() is False:
            print("bug in db access, idx: " + str(idx))
            return

        if mymesure['iswind'] is True:
            my_query = 'select dateTime, min, mintime, max, maxtime, max_dir from archive_day_' + mymesure['field'] + ' order by dateTime'
        else:
            my_query = 'select dateTime, min, mintime, max, maxtime from archive_day_' + mymesure['field'] + ' order by dateTime'
        my_cur = tmp_conn.cursor()
        my_cur.execute(my_query)
        tmp_row = my_cur.fetchone()

        json_keys.append({'idx': [idx], 'db': tmp_conn, 'r': tmp_row, 'ok': False, 'c': my_cur})
        idx += 1
    return json_keys


if __name__ == '__main__':
    load_data('BBF015')
    # load_data(sys.argv[1])
