# migrate process
#   addNewWorkItem(self, work_item)
#       add a db in the todo list
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item, my_span):
#       Process the work item
#   succeedWorkItem(work_item, my_span):
#       Mark the work_item as processed
#   failWorkItem(work_item, exc, my_span):
#       mark the work_item as failed
# ---------------
# more info on wind vs windGust: https://github-wiki-see.page/m/weewx/weewx/wiki/windgust
# ---------------
import app.tools.myTools as t
import mysql.connector
import psycopg2
from datetime import datetime, timedelta
from app.tools.myTools import logException


class MigrateDB:
    def __init__(self):
        self._meteors_to_process = []
        pgconn = None
        try:
            pgconn = self.getPGConnexion()

            # load mesures definition in memory
            self.mesures = self.get_mesures(pgconn)
            # load omm link array, between base mesures and linked omm mesures
            self.omm_link = self.get_omm_link()

        except Exception as e:
            logException(e)

        finally:
            if pgconn is not None:
                pgconn.close()

    def addNewWorkItem(self, meteor):
        pgconn = None
        try:
            pgconn = self.getPGConnexion()
            # get pid, and push in queue
            poste_id = self.get_poste_id(pgconn, meteor)
            if poste_id is None:
                raise Exception('station ' + meteor + ' not found')

            self._meteors_to_process.append({'pid': poste_id, 'meteor': meteor})

        except Exception as e:
            logException(e)

        finally:
            if pgconn is not None:
                pgconn.close()

    def getNextWorkItem(self):
        if self._meteors_to_process.__len__() == 0:
            return None
        work_item = self._meteors_to_process[0]
        self._meteors_to_process = self._meteors_to_process[1::]
        return work_item

    def processWorkItem(self, work_item, my_span, op_tracer):
        myconn = None
        pgconn = None
        try:
            meteor = work_item['meteor']
            pid = work_item['pid']
            pgconn = self.getPGConnexion()
            myconn = self.getMSQLConnection(meteor)

            with op_tracer.start_as_current_span('loading measures for ' + meteor) as my_data_span:
                self.insert_obs(pid, myconn, pgconn, my_data_span)

            with op_tracer.start_as_current_span('loading extremes for ' + meteor) as my_data_span:
                self.insert_xtremes(pid, meteor, pgconn, my_data_span)

        except Exception as e:
            raise(e)

        finally:
            if pgconn is not None:
                pgconn.close()
            if myconn is not None and myconn.is_connected():
                myconn.close()

    def getObsStartingDate(self, pgconn, pid):
        pg_cur = pgconn.cursor()
        my_q = 'select max(time) from obs where duration != 0 and poste_id = ' + str(pid)
        pg_cur.execute(my_q)
        row = pg_cur.fetchone()
        if row is None or row[0] is None or row[0] == 0:
            return 0
        start_dt = datetime(str(row[0]))
        return start_dt.timestamp() - 2 * 3600

    def getExtremesStartingDate(self, pgconn, pid):
        pg_cur = pgconn.cursor()
        my_q = 'select max(date) from extremes where '
        my_q += " poste_id = " + str(pid)
        pg_cur.execute(my_q)
        row = pg_cur.fetchone()
        if row is None or row[0] is None or row[0] == 0:
            return 0
        my_date = row[0] + timedelta(1)
        my_time = datetime.min.time()
        start_dt = datetime.combine(my_date, my_time)
        return start_dt.timestamp()

    def insert_obs(self, pid, myconn, pgconn, my_span):
        start_date = self.getObsStartingDate(pgconn, pid)

        mesures = self.mesures
        query_my = "select from_unixTime(dateTime + 2 * 3600), usUnits, `interval`"
        query_args = []
        query_pg1 = "insert into obs(poste_id, time, duration"
        query_pg2 = ") values (%s, %s, %s"
        row_datetime = 0
        row_usunit = 1
        row_interval = 2

        # get all needed valdk
        used_decas = [0]
        for a_mesure in mesures:
            if a_mesure['valdk'] not in used_decas:
                used_decas.append(a_mesure['valdk'])

        # query_args = array of query args, one for each valdk
        for a_deca in used_decas:
            query_args.append({'valdk': a_deca, 'dirty': False, 'args': []})

        nb_col = 0
        for a_mesure in mesures:
            nb_col += 1

            # add field name into our select statement
            query_my += ', ' + a_mesure['col']

            # add field name into our insert statements
            query_pg1 += ", " + a_mesure['field']
            query_pg2 += ', %s'

        query_my += " from archive where dateTime > " + str(start_date) + " order by dateTime"""
        query_pg = query_pg1 + query_pg2 + ") returning id;"""

        # get our cursors
        my_cur = myconn.cursor()
        pg_cur = pgconn.cursor()

        # execute the select statement
        my_cur.execute(query_my)
        row = my_cur.fetchone()
        nb_inserted = 0
        nb_new_rows = 0
        test_id = -1

        try:
            while row is not None:
                if row[row_usunit] != 16:
                    raise Exception('bad usUnits: ' + str(row[row_usunit]) + ', dateTime: ' + str(row[row_datetime]))

                # reset dirty flag
                for a_q in query_args:
                    a_q['dirty'] = False
                    a_q['args'] = [
                        str(pid),
                        str(row[row_datetime] + timedelta(hours=a_q['valdk'])),
                        str(row[row_interval] if a_q['valdk'] == 0 else 0)
                        ]

                idx = 0
                while idx < nb_col:
                    a_mesure = mesures[idx]
                    row_data = row[idx + 3]

                    for a_q in query_args:
                        if a_q['valdk'] == a_mesure['valdk'] and row_data is not None:
                            a_q['args'].append(str(row_data))
                            a_q['dirty'] = True
                        else:
                            a_q['args'].append(None)
                    idx += 1

                for a_q in query_args:
                    if a_q['dirty'] is True:
                        pg_cur.execute(query_pg, a_q['args'])
                        nb_inserted += 1
                        nb_new_rows += 1

                if test_id == -1 and pg_cur.rowcount > 0:
                    test_id = pg_cur.fetchone()[0]
                    t.logInfo("first archive inserted, id: " + str(test_id) + ", from date: " + str(a_q['args'][1]), my_span, {"svc": self.display})

                if nb_inserted > 10000:
                    pgconn.commit()
                    pg_cur.close()
                    pg_cur = pgconn.cursor()
                    nb_inserted = 0
                row = my_cur.fetchone()
        finally:
            if pg_cur.rowcount > 0:
                test_id = pg_cur.fetchone()[0]
                t.logInfo('all archive(s) inserted, last id: ' + str(test_id) + ", date: " + str(a_q['args'][1]), my_span, {"svc": self.display})
                my_span.add_event(str(nb_new_rows) + ' rows inserted from archive with timestamp > ' + str(start_date))
            else:
                t.logInfo('no new data in archive', my_span, {"svc": self.display})
                my_span.add_event('no new data in archive from timestamp: ' + str(start_date))

            pgconn.commit()

    def succeedWorkItem(self, work_item, my_span):
        t.logInfo('migration ' + work_item['meteor'] + ' successfull', my_span, {"svc": self.display})
        return

    def failWorkItem(self, work_item, exc, my_span):
        t.logError('migration ' + str(work_item['meteor']) + ' not done...', my_span, {"svc": self.display})
        return

    def getSpanTitle(self, work_item):
        return 'Migrate ' + work_item['meteor']

    # ----------------
    # private methods
    # ----------------
    def insert_xtremes(self, pid, meteor, pgconn, my_span):
        start_date = self.getExtremesStartingDate(pgconn, pid)
        day_process = None
        pg_cur = pgconn.cursor()
        inserted_row = 0
        json_keys = []
        test_id = -1
        nb_new_row = 0

        try:
            json_keys = self.get_json_keys(meteor, start_date)
            while True:
                day_process, is_done = self.get_next_process_day(json_keys)
                if is_done is True:
                    break
                for aj_key in json_keys:
                    if aj_key['r'] is None or aj_key['ok'] is False:
                        continue
                    min_val = max_val = None

                    if self.mesures[aj_key['idx'][0]]['zero'] is False and aj_key['r'][1] == 0:
                        min_val = None
                    else:
                        min_val = aj_key['r'][1]

                    if self.mesures[aj_key['idx'][0]]['zero'] is False and aj_key['r'][3] == 0:
                        max_val = None
                    else:
                        max_val = aj_key['r'][3]

                    if self.mesures[aj_key['idx'][0]]['iswind'] is True:
                        wind_dir = aj_key['r'][5]
                    else:
                        wind_dir = None

                    args = [
                        pid,
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
                        args[3] = self.mesures[aj_key['idx'][idx_idx]]['id']
                        self.insert_xtreme_row(self.mesures, pg_cur, args)
                        idx_idx += 1
                        inserted_row += 1
                        nb_new_row += 1

                        if test_id == -1 and pg_cur.rowcount > 0:
                            test_id = pg_cur.fetchone()[0]
                            t.logInfo("first extreme inserted, id: " + str(test_id) + ", date: " + str(day_process), my_span, {"svc": self.display})

                        if (inserted_row % 10000) == 0:
                            test_id = pg_cur.fetchone()[0]
                            pg_cur.execute('commit')
                            pg_cur.close()
                            pg_cur = pgconn.cursor()
                            inserted_row = 0

                    aj_key['r'] = aj_key['c'].fetchone()

        finally:
            for j_key in json_keys:
                if j_key['db'].is_connected():
                    j_key['db'].close()
            if pg_cur.rowcount > 0:
                test_id = pg_cur.fetchone()[0]
                t.logInfo('all extremes inserted, last id: ' + str(test_id) + ", date: " + str(day_process), my_span, {"svc": self.display})
                my_span.add_event(str(nb_new_row) + ' rows inserted from archive_day_XXX with timestamp > ' + str(start_date))
            else:
                t.logInfo('no new data for our extremes', {"svc": self.display})
                my_span.add_event('no new data in archive_day_XXX from timestamp: ' + str(start_date))
            pg_cur.execute('commit')
            pg_cur.close()

    # Utility functions
    def get_poste_id(self, pgconn, meteor):
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

    def insert_xtreme_row(self, mesures, pg_cur, args):
        query_pg = """
            insert into extremes (poste_id, date, id_obs, mesure_id, min, min_time, max, max_time, max_dir) values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id"""
        pg_cur.execute(query_pg,  args)

    def get_next_process_day(self, json_keys):
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

    def get_mesures(self, pgconn):
        mesures = []
        pg_query = "select id, archive_col, archive_table, json_input, val_deca, min, min_deca, max, max_deca, is_avg, is_wind, allow_zero, omm_link from mesures"

        pg_cur = pgconn.cursor()
        pg_cur.execute(pg_query)
        row = pg_cur.fetchone()
        while row is not None:
            one_mesure = {
                'id': row[0],
                'col': row[1],
                'table': row[2],
                'field': row[3],
                'valdk': row[4],
                'min': row[5],
                'mindk': row[6],
                'max': row[7],
                'maxdk': row[8],
                'isavg': row[9],
                'iswind': row[10],
                'zero': row[11],
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

    def get_omm_link(self):
        omm_link = []
        m_idx = 0

        while m_idx < len(self.mesures):
            if self.mesures[m_idx]['ommidx'] is not None:
                my_mesure_data = None
                my_omm_mesure = self.mesures[m_idx]
                my_mesure = self.mesures[my_omm_mesure['ommidx']]
                for an_omm_link in omm_link:
                    if an_omm_link['base_idx'] == my_omm_mesure['ommidx']:
                        my_mesure_data = an_omm_link
                if my_mesure_data is None:
                    my_mesure_data = {'base_idx': my_omm_mesure['ommidx'], 'col': my_mesure['col'], 'ins_idx': -1, 'omms': []}
                    omm_link.append(my_mesure_data)
                my_mesure_data['omms'].append({'ommidx': m_idx, 'col': my_omm_mesure['col'], 'decas': [my_omm_mesure['valdk'], my_omm_mesure['maxdk'], my_omm_mesure['mindk']], 'ins_idx': 0})
            m_idx += 1

        return omm_link

    def get_json_keys(self, meteor, start_date):
        idx = 0
        json_keys = []
        while idx < len(self.mesures):
            bcont = False
            mymesure = self.mesures[idx]

            if (mymesure['min'] is False and mymesure['max'] is False):
                idx += 1
                continue

            if mymesure['ommidx'] is not None:
                for aj_key in json_keys:
                    if self.mesures[mymesure['ommidx']]['id'] == self.mesures[aj_key['idx'][0]]['id']:
                        aj_key['idx'].append(idx)
                        bcont = True

            if bcont is True:
                idx += 1
                continue

            # fix for wind table
            table_name = mymesure['col']
            if mymesure['table'] is not None:
                table_name = mymesure['table']

            if mymesure['iswind'] is True:
                my_query = 'select dateTime, min, mintime, max, maxtime, max_dir from archive_day_' + table_name + ' where dateTime > ' + str(start_date) + ' order by dateTime'
            else:
                my_query = 'select dateTime, min, mintime, max, maxtime from archive_day_' + table_name + ' where dateTime > ' + str(start_date) + ' order by dateTime'
            myconn = self.getMSQLConnection(meteor)
            my_cur = myconn.cursor()
            my_cur.execute(my_query)
            tmp_row = my_cur.fetchone()

            json_keys.append({'idx': [idx], 'db': myconn, 'r': tmp_row, 'ok': False, 'c': my_cur})
            idx += 1
        return json_keys

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato2"
        )

    def getMSQLConnection(self, meteor):
        myconn = mysql.connector.connect(
            host="localhost",
            user="nico",
            password="Funiculi",
            database=meteor
        )
        if myconn.is_connected() is False:
            raise Exception("bug in db access")

        # set session timezone to utc
        my_cur = myconn.cursor()
        my_cur.execute("set time_zone = '+00:00'")
        myconn.commit()
        my_cur.close()

        return myconn
