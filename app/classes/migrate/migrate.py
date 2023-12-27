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
import app.tools as t
from app.tools.myTools import FromTimestampToDate, AsTimezone, GetFirstDayNextMonth
from app.tools.myTools import FromDateToLocalDateTime
import mysql.connector
import psycopg2
from datetime import datetime, timedelta
from app.classes.repository.posteMeteor import PosteMeteor


# --------------------------------------
# our class is called by worker service
#    need some methods...
# --------------------------------------
class MigrateDB:
    def __init__(self):
        self._meteors_to_process = []
        self.loadSelfVariables()

    # -----------------------------------
    # add an item in the list to execute
    # -----------------------------------
    def addNewWorkItem(self, meteor):
        self._meteors_to_process.append({
            'meteor': meteor,
            'info': meteor,
            'bd': meteor,
            'spanID': 'Start ' + meteor + ' migration'
        })

        t.myTools.logInfo("New work item added in queue", None, {"svc": "migrate", "meteor": meteor, "work_item": self._meteors_to_process[len(self._meteors_to_process) - 1]})

    # -----------------------------
    # get next item form our queue
    # -----------------------------
    def getNextWorkItem(self):
        if self._meteors_to_process.__len__() == 0:
            return None
        work_item = self._meteors_to_process[0]
        self._meteors_to_process = self._meteors_to_process[1::]
        return work_item

    # ---------------------
    # process was succesful
    # ---------------------
    def succeedWorkItem(self, work_item, my_span):
        return

    # ---------------
    # process failed
    # ---------------
    def failWorkItem(self, work_item, exc, my_span):
        return

    # -----------------
    # process our item
    # -----------------
    def processWorkItem(self, work_item, my_span):
        try:
            pgconn = self.getPGConnexion()
            pg_cur = pgconn.cursor()
            meteor = work_item['meteor']
            current_ts = datetime.now().timestamp() + 1

            cur_poste = PosteMeteor(meteor)
            if cur_poste.data.id is None:
                raise Exception('station ' + meteor + ' not found')

            if cur_poste.data.load_dump is False:
                my_span.add_event(meteor, {'status': 'Migration stopped, station load_dump is False'})
                return

            work_item['pid'] = cur_poste.data.id
            work_item['tz'] = cur_poste.data.delta_timezone
            work_item['stop_date_utc'] = cur_poste.data.stop_date if cur_poste.data.stop_date is None else AsTimezone(cur_poste.data.stop_date, 0)

            self.getNewDateBraket(work_item, my_span)

            # loop per year
            while work_item['start_ts_archive_utc'] < current_ts:

                # Load obs, records from archive
                new_extremes = self.loadExistingArchive(pg_cur, work_item, my_span)

                # Add data from WeeWx record tables
                new_extremes = self.loadMaxminFromWeewx(work_item, new_extremes, my_span)

                # Merge list in db
                self.storeMaxMinInDB(pg_cur, work_item['pid'], new_extremes, my_span)

                new_extremes = []

                pgconn.commit()
                self.getNewDateBraket(work_item, my_span)

        finally:
            pg_cur.close()
            pgconn.close()
            # if work_item['old_json_load'] is not None and work_item['old_json_load'] is True:
            #     self.updateLoadJsonValue(work_item)

    # ---------------------------------------
    # other methods specific to this service
    # ---------------------------------------
    def getNewDateBraket(self, work_item, my_span):

        """Get start_dt/end_dt from postes, and archive table"""
        myconn = self.getMSQLConnection(work_item['meteor'])
        my_cur = myconn.cursor()

        pgconn = self.getPGConnexion()
        pg_cur = pgconn.cursor()

        work_item['old_load_raw_data'] = False

        # 1/1/2100 00:00 UTC
        max_date = AsTimezone(datetime(2100, 1, 1, 4), 0)
        max_ts = int(max_date.timestamp())

        try:
            # Get scan limit
            if work_item.get('start_ts_limit') is None:
                my_cur.execute('select min(dateTime), max(dateTime) from archive')
                row = my_cur.fetchone()
                my_cur.close()
                if row is None or len(row) == 0 or row[0] is None or row[1] is None:
                    work_item['start_ts_archive_utc'] = max_ts
                    return
                work_item['start_ts_limit'] = row[0]
                work_item['end_ts_limit'] = row[1] + 1

            # Get start_dt/start_ts_archive_utc
            if work_item.get('end_dt_archive_utc') is None:
                # First pass
                sql = "select last_obs_date, last_extremes_date from postes where meteor='" + work_item['meteor'] + "';"
                pg_cur.execute(sql)
                row = pg_cur.fetchone()
                if row is None or len(row) < 1 or row[0] is None or row[1] is None:
                    work_item['start_ts_archive_utc'] = work_item['start_ts_limit']
                    work_item['start_dt_archive_utc'] = FromTimestampToDate(work_item['start_ts_archive_utc'])
                    work_item['start_date_extremes'] = AsTimezone((work_item['start_dt_archive_utc'] - timedelta(days=1)), work_item['tz']).date()

                else:
                    work_item['start_dt_archive_utc'] = AsTimezone(row[0], 0)
                    work_item['start_ts_archive_utc'] = work_item['start_dt_archive_utc'].timestamp() + 1
                    work_item['start_date_extremes'] = AsTimezone(row[1] - timedelta(days=1)).date()

            else:
                work_item['start_ts_archive_utc'] = work_item['end_ts_archive_utc']
                work_item['start_dt_archive_utc'] = FromTimestampToDate(work_item['start_ts_archive_utc'])
                work_item['start_date_extremes'] = AsTimezone((work_item['start_dt_archive_utc'] - timedelta(days=1)), work_item['tz']).date()

            work_item['start_ts_archive_utc_day'] = int(AsTimezone((work_item['start_dt_archive_utc'] - timedelta(days=1)), work_item['tz']).timestamp())

            if work_item['stop_date_utc'] is not None:
                # do not process data if start_archive_utc is after postes.stop_date
                if work_item['stop_date_utc'] < work_item['start_dt_archive_utc']:
                    work_item['start_ts_archive_utc'] = max_ts
                    return

            # if start_ts_archive_utc greater than end_ts_limit -> exit
            if work_item['start_ts_archive_utc'] > work_item['end_ts_limit']:
                work_item['start_ts_archive_utc'] = max_ts
                return

            work_item['end_dt_archive_utc'] = GetFirstDayNextMonth(FromTimestampToDate(work_item['start_ts_archive_utc']), work_item['tz'])
            # Do not process data after postes.stop_date
            if work_item['stop_date_utc'] is not None and work_item['stop_date_utc'] < work_item['end_dt_archive_utc']:
                work_item['end_dt_archive_utc'] = work_item['stop_date_utc']

            work_item['end_ts_archive_utc'] = int(work_item['end_dt_archive_utc'].timestamp())
            work_item['end_date_extremes'] = AsTimezone((work_item['end_dt_archive_utc'] + timedelta(days=1)), work_item['tz']).date()
            work_item['end_ts_archive_utc_day'] = int(AsTimezone((work_item['end_dt_archive_utc'] + timedelta(days=1)), work_item['tz']).timestamp())

            t.myTools.logInfo(
                'ts_archive (ts utc)    from: ' + str(work_item['start_ts_archive_utc']) + ' to ' + str(work_item['end_ts_archive_utc']),
                my_span,
                {"svc": "migrate", "meteor":  work_item['meteor']})

            print('-------------------------------------------------')
            print('Archive (dt utc)       from: ' + str(work_item['start_dt_archive_utc']) + ' to ' + str(work_item['end_dt_archive_utc']))
            print('ts_archive (ts utc)    from: ' + str(work_item['start_ts_archive_utc']) + ' to ' + str(work_item['end_ts_archive_utc']))
            print('ts_arch_day (date utc) from: ' + str(work_item['start_ts_archive_utc_day']) + ' to ' + str(work_item['end_ts_archive_utc_day']))
            print('X_Days  (date local)   from: ' + str(work_item['start_date_extremes']) + ' to ' + str(work_item['end_date_extremes']))
            print('-------------------------------------------------')

            return

        except Exception as ex:
            print("exception: " + str(ex))
            raise ex

        finally:
            myconn.close()

    # def updateLoadJsonValue(self, work_item):
    #     pgconn = self.getPGConnexion()
    #     pg_cur = pgconn.cursor()

    #     try:
    #         pg_cur.execute('update postes set load_raw_data = ' + str(work_item['old_json_load']) + " where meteor = '" + work_item['meteor'] + "'")
    #         pgconn.commit()

    #     except Exception as ex:
    #         pgconn.rollback()
    #         raise ex

    #     finally:
    #         pg_cur.close()

    # ---------------------------------------------------
    # insert mesures from weewx archive in our obs table
    # ---------------------------------------------------
    def getExistingRecord(self, pg_cur, work_item, my_span):
        existing_records = {}

        # store min/max in our cache
        for a_mesure in self.measures:
            cache = []
            sql = 'select id, mesure_id, date_local, min, min_time, max, max_time, max_dir from extremes ' +\
                ' where poste_id = ' + str(work_item['pid']) +\
                " and date_local >= '" + str(work_item['start_date_extremes'] - timedelta(days=1)) + "' " +\
                " and date_local < '" + str(work_item['end_date_extremes'] + timedelta(days=1)) + "' " +\
                ' order by mesure_id, date_local'

            current_mid = -1
            cache = []
            pg_cur.execute(sql)
            row = pg_cur.fetchone()
            while row is not None:
                if row[1] != current_mid:
                    cache = []
                    existing_records['m_' + str(row[1])] = {'mid': row[1], 'cache': cache}
                    current_mid = row[1]

                cache.append([row[2], row[1], row[3], row[4], None, row[5], row[6], row[7], None, row[0], FromDateToLocalDateTime(row[2], work_item['tz']).timestamp(), False])

                row = pg_cur.fetchone()

        return existing_records

    def loadExistingArchive(self, pg_cur, work_item, my_span):

        query_my = self.getWeewxSelectSql(work_item)
        sql_insert = "insert into obs(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value) values "

        minmax_values = []
        data_args = []

        # get a cursor to our archive db
        myconn = self.getMSQLConnection(work_item['meteor'])
        my_cur = myconn.cursor()

        # execute the select statement
        my_cur.execute(query_my)
        row2 = my_cur.fetchone()

        # load field_name/row_id mapping for weewx select
        col_mapping = {}
        idx = 0

        while idx < len(my_cur.column_names):
            col_mapping[my_cur.column_names[idx]] = idx
            idx += 1

        while row2 is not None:
            if row2[self.row_archive_usunits] != 16:
                raise Exception('bad usUnits: ' + str(row2[self.row_archive_usunits]) + ', dateTime(UTC): ' + str(row2[self.row_archive_dt_utc]))

            for a_mesure in self.measures:
                cur_val, ts_mesure_local = self.get_valeurs(a_mesure, row2, col_mapping)
                if cur_val is None:
                    continue

                date_obs_utc = FromTimestampToDate(ts_mesure_local + a_mesure['valdk'] * 3600)
                date_obs_local = AsTimezone(date_obs_utc, work_item['tz']).replace(tzinfo=None)
                data_args.append(([work_item['pid'], date_obs_utc, date_obs_local, a_mesure['id'], row2[self.row_archive_interval], cur_val, 0]))

                if a_mesure['valdk'] != 0:
                    date_obs_local = FromTimestampToDate(ts_mesure_local + work_item['tz'] * 3600).replace(tzinfo=None)
                date_obs_utc = date_obs_utc.replace(tzinfo=None)

                if a_mesure['id'] == 76 and cur_val == 15.6:
                    pass

                if a_mesure['iswind'] is True:
                    max_dir = None
                    if a_mesure['diridx'] is not None:
                        max_dir = row2[col_mapping[self.measures[a_mesure['diridx']]['archive_col']]]

                    minmax_values.append({'min': cur_val, 'max': cur_val, 'date_min': date_obs_local, 'date_max': date_obs_local, 'max_dir': max_dir, 'mid': a_mesure['id'], 'obs_id': -1})
                else:
                    minmax_values.append({'min': cur_val, 'max': cur_val, 'date_min': date_obs_local, 'date_max': date_obs_local, 'mid': a_mesure['id'], 'obs_id': -1})

            row2 = my_cur.fetchone()

        my_cur.close()

        # cursor.mogrify() to insert multiple values
        args = ','.join(pg_cur.mogrify("( %s, %s, %s, %s, %s, %s, %s )", i).decode('utf-8')
                        for i in data_args)

        pg_cur.execute(sql_insert + args + ' returning id')
        new_ids = pg_cur.fetchall()

        idx = 0
        while idx < len(new_ids):
            minmax_values[idx]['obs_id'] = new_ids[idx][0]
            idx += 1

        return minmax_values

    def get_valeurs(self, a_mesure, row2, col_mapping):
        if a_mesure['ommidx'] is not None:
            return self.get_valeurs(self.measures[a_mesure['ommidx']], row2, col_mapping)

        if row2[col_mapping[a_mesure['archive_col']]] is None:
            return None, None

        return row2[col_mapping[a_mesure['archive_col']]], row2[self.row_archive_dt_utc]

    # ------------------------------------
    # generate max/min from WeeWX records
    # ------------------------------------
    def loadMaxminFromWeewx(self, work_item, new_records, my_span):
        myconn = self.getMSQLConnection(work_item['meteor'])
        try:
            for a_mesure in self.measures:
                if a_mesure.get('table') == 'skip':
                    continue

                my_cur = myconn.cursor()
                try:
                    # get table name, fix for wind table
                    table_name = a_mesure['archive_col']
                    if a_mesure['table'] is not None:
                        table_name = a_mesure['table']

                    # We need to use mintime/maxtime as the date of the record
                    # the mintime and maxtime can be on two different days...
                    if a_mesure['iswind'] is False:
                        my_query = \
                            'select min, mintime, max, maxtime, null as max_dir, dateTime ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= " + str(work_item['start_ts_archive_utc_day']) +\
                            " and dateTime < " + str(work_item['end_ts_archive_utc_day']) +\
                            " order by dateTime"
                    else:
                        my_query = \
                            'select min, mintime, max, maxtime, max_dir, dateTime ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= " + str(work_item['start_ts_archive_utc_day']) +\
                            " and dateTime < " + str(work_item['end_ts_archive_utc_day']) +\
                            " order by dateTime"

                    my_cur.execute(my_query)
                    row = my_cur.fetchone()
                    while row is not None:
                        if row[0] is not None or row[2] is not None:
                            dt_min = AsTimezone(FromTimestampToDate((row[1] if row[1] is not None else row[5]) + a_mesure['valdk'] * 3600), work_item['tz']).replace(tzinfo=None)
                            dt_max = AsTimezone(FromTimestampToDate((row[3] if row[3] is not None else row[5]) + a_mesure['valdk'] * 3600), work_item['tz']).replace(tzinfo=None)
                            if a_mesure['iswind'] is True:
                                new_records.append({'min': row[0], 'date_min': dt_min, 'max': row[2], 'date_max': dt_max, 'max_dir': row[4], 'mid': a_mesure['id'], 'obs_id': -1})
                            else:
                                new_records.append({'min': row[0], 'date_min': dt_min, 'max': row[2], 'date_max': dt_max, 'mid': a_mesure['id'], 'obs_id': -1})
                        row = my_cur.fetchone()
                finally:
                    my_cur.close()
                    return new_records
        finally:
            myconn.close()

    def storeMaxMinInDB(self, pg_cur, pid, new_records, my_span):
        # check: nico use: last_in_db for insert-update or insert..
        insert_cde_min = "insert into x_min(obs_id, date_local, poste_id, mesure_id, min, min_time, qa_min) values "
        insert_cde_max = "insert into x_max(obs_id, date_local, poste_id, mesure_id, max, max_time, qa_max, max_dir) values "
        min_args = []
        max_args = []
        mesures_hash = {}
        for a_mesure in self.measures:
            mesures_hash[a_mesure['id']] = a_mesure

        for a_record in new_records:
            cur_mesure = mesures_hash[a_record['mid']]

            if a_record['mid'] == 76 and a_record['min'] == 15.6:
                pass

            if cur_mesure['min'] is True:
                dt_local_min = (a_record['date_min'] + timedelta(hours=cur_mesure['mindk'])).date()
                min_args.append((a_record['obs_id'] if a_record['obs_id'] > -1 else None, dt_local_min, pid, a_record['mid'], a_record['min'], a_record['date_min'], 0))

            if cur_mesure['max'] is True:
                dt_local_max = (a_record['date_min'] + timedelta(hours=cur_mesure['maxdk'])).date()
                max_args.append((a_record['obs_id'] if a_record['obs_id'] > -1 else None, dt_local_max, pid, a_record['mid'], a_record['max'], a_record['date_max'], 0, a_record.get('max_dir')))

        min_args_ok = ','.join(pg_cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in min_args)
        max_args_ok = ','.join(pg_cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in max_args)

        pg_cur.execute(insert_cde_min + min_args_ok)
        pg_cur.execute(insert_cde_max + max_args_ok)

    # --------------------------------
    # return the sql select statement
    # --------------------------------
    def getWeewxSelectSql(self, work_item):
        query_my = "select dateTime, usUnits, `interval`"

        # load an array of query args, one for each valdk, update sql statement
        for a_mesure in self.measures:
            # add field name into our select statement for weewx
            query_my += ', ' + a_mesure['archive_col']

        # finalize sql statements
        query_my += " from archive where dateTime >= " + str(work_item['start_ts_archive_utc'])
        query_my += " and dateTime < " + str(work_item['end_ts_archive_utc'])

        # query_my += " order by dateTime"""
        query_my += " order by dateTime"
        return query_my

    def getMeasures(self, pgconn):
        mesures = []
        pg_query = "select id, archive_col, archive_table, field_dir, json_input, val_deca, min, min_deca, max, max_deca, is_avg, is_wind, allow_zero, omm_link from mesures order by id"

        pg_cur = pgconn.cursor()
        pg_cur.execute(pg_query)
        row = pg_cur.fetchone()
        while row is not None:
            if row[1] is None:
                continue
            one_mesure = {
                'id': row[0],
                'archive_col': row[1],
                'table': row[2],
                'diridx': row[3],
                'field': row[4],
                'valdk': row[5],
                'min': row[6],
                'mindk': row[7],
                'max': row[8],
                'maxdk': row[9],
                'isavg': row[10],
                'iswind': row[11],
                'zero': row[12],
                'ommidx': None
            }
            if row[13] != 0:
                idx_mesure = len(mesures) - 1
                while idx_mesure >= 0:
                    if mesures[idx_mesure]['id'] == row[13]:
                        one_mesure['ommidx'] = idx_mesure
                        idx_mesure = 0
                    idx_mesure -= 1
            mesures.append(one_mesure)
            row = pg_cur.fetchone()
        pg_cur.close()
        for a_mesure in mesures:
            if a_mesure['diridx'] is not None:
                fi_dir = a_mesure['diridx']
                a_mesure['diridx'] = None
                dir_idx = 0
                while dir_idx < len(mesures):
                    if mesures[dir_idx]['id'] == fi_dir:
                        a_mesure['diridx'] = dir_idx
                        dir_idx = len(mesures)
                    dir_idx += 1
        return mesures

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
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
        # my_cur.execute("set time_zone = '+00:00'")
        my_cur.execute('SET @@session.time_zone = "+00:00"')
        myconn.commit()
        my_cur.close()

        myconn.time_zone = "+00:00"
        return myconn

    def loadSelfVariables(self):
        pgconn = None
        try:
            pgconn = self.getPGConnexion()

            # load mesures definition in memory
            self.measures = self.getMeasures(pgconn)

            # row_id for select from archive data, first 4 fields
            self.row_archive_dt_utc = 0
            self.row_archive_usunits = 1
            self.row_archive_interval = 2

            # row_id for extreme data
            self.row_extreme_min = 0
            self.row_extreme_mintime = 1
            self.row_extreme_max = 2
            self.row_extreme_maxtime = 3
            self.row_extreme_maxdir = 4
            self.row_extreme_mid = 5
            self.row_extreme_dateTime = 6

            # row_id for virtual data
            self.row_virtual_min_utc_ts = 0
            self.row_virtual_min = 1
            self.row_virtual_mintime = 2
            self.row_virtual_max_utc_ts = 3
            self.row_virtual_max = 4
            self.row_virtual_maxtime = 5
            self.row_virtual_maxdir = 6
            self.row_virtual_mid = 7
            self.row_virtual_obsid = 8

            self.row_cache_datetime = 0
            self.row_cache_mid = 1
            self.row_cache_min = 2
            self.row_cache_min_local_dt = 3
            self.row_cache_obsid_min = 4
            self.row_cache_max = 5
            self.row_cache_max_local_dt = 6
            self.row_cache_maxdir = 7
            self.row_cache_obsid_max = 8
            self.row_cache_row_id = 9
            self.row_cache_ts = 10
            self.row_cache_dirty = 11

        finally:
            if pgconn is not None:
                pgconn.close()
