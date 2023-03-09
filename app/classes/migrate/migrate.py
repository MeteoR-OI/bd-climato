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
from app.tools.myTools import FromTimestampToDate, FromAwareDtToTimestamp, AsTimezone, GetFirstDayNextMonth
import mysql.connector
import psycopg2
from datetime import datetime, timedelta
from app.classes.repository.extremeMeteor import ExtremeMeteor
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
            'meteor': meteor,
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
        work_item['old_json_load'] = None
        try:
            pgconn = self.getPGConnexion()
            pg_cur = pgconn.cursor()
            meteor = work_item['meteor']
            current_dt = datetime.now()

            work_item['pid'], work_item['tz'], work_item['load_json'] = PosteMeteor.getPosteIdAndTzByMeteor(meteor)

            if work_item['pid'] is None:
                raise Exception('station ' + meteor + ' not found')

            self.getNewDateBraket(work_item)

            # loop per year
            while work_item['start_dt'] < current_dt:

                # Load obs, records from archive
                new_records = self.loadExistingObsAndFlushObs(pg_cur, work_item, my_span)

                # load archive data
                self.loadExistingRecordsAndFlush(pg_cur, work_item, new_records, start_dt, end_dt, last_ts_in_extreme, my_span)
                new_records = {}

                pgconn.commit()

                self.getNewDateBraket(work_item)

        finally:
            pg_cur.close()
            pgconn.close()
            if work_item['old_json_load'] is not None and work_item['old_json_load'] is True:
                self.updateLoadJsonValue(work_item)

    # ---------------------------------------
    # other methods specific to this service
    # ---------------------------------------
    def getNewDateBraket(self, work_item):

        """Get start_dt/end_dt from postes, and archive table"""
        myconn = self.getMSQLConnection(meteor)
        my_cur = myconn.cursor()

        old_load_json = False
        max_date = datetime(2100, 1, 1)
        max_ts = max_date.timestamp()

        try:
            # Get scan limit
            if work_item.get('start_limit_ts') is None:
                my_cur.execute('select min(dateTime), max(dateTime) from archive')
                row = my_cur.fetchone()
                my_cur.close()
                if row is None or len(row) == 0 or row[0] is None or row[1] is None:
                    work_item['start_dt'] = max_date
                    return
                work_item['start_limit_ts'] = row[0]
                work_item['end_limit_ts'] = row[1]

            # Get start_dt/start_ts
            if work_item.get('end_dt_utc') is None:
                work_item['start_dt_utc'] = FromTimestampToDate(work_item['start_limit_ts'] - 1)
                work_item['start_dt_local'] = AsTimezone(work_item['start_dt_utc'], work_item['tz'])
                work_item['start_ts'] = work_item['start_limit_ts'] - 1
            else:
                work_item['start_dt_utc'] = work_item['end_dt_utc']
                work_item['start_dt_local'] = work_item['end_dt_local']
                work_item['start_ts'] = work_item['end_ts']

            # if start_ts greater than end_limit_ts -> exit
            if work_item['start_ts'] > work_item['end_limit_ts']:
                work_item['start_dt'] = max_date
                return

            work_item['end_dt_local'] = GetFirstDayNextMonth(work_item['start_dt_local'])
            work_item['end_dt_utc'] = AsTimezone(work_item['end_dt_utc'], -1 * work_item['tz'])
            work_item['end_ts'] = work_item['end_dt_utc'].timestamp()

            if work_item['old_json_load'] is True:
                work_item['old_json_load'] = False
                self.updateLoadJsonValue(work_item)

            print('-------------------------------------------------')
            print('new period (local) from: ' + str(work_item['start_dt_local']) + ' to ' + str(work_item['end_dt_local']))
            print('new period (utc)   from: ' + str(work_item['start_dt_utc']) + ' to ' + str(work_item['end_dt_utc']))
            print('new period (ts)    from: ' + str(work_item['start_ts']) + ' to ' + str(work_item['end_ts']))
            print('-------------------------------------------------')

            return

        except Exception as ex:
            print("exception: " + str(ex))
            raise ex

        finally:
            myconn.close()

    def updateLoadJsonValue(self, work_item):
        pgconn = self.getPGConnexion()
        pg_cur = pgconn.cursor()

        try:
            pg_cur.execute('update postes set load_json = ' + str(work_item['old_json_load']) + " where meteor = '" + work_item['meteor'] + "'")
            pgconn.commit()

        except Exception as ex:
            pgconn.rollback()
            raise ex

        finally:
            pg_cur.close()

    # ---------------------------------------------------
    # insert mesures from weewx archive in our obs table
    # ---------------------------------------------------
    def loadExistingObsAndFlushObs(self, pg_cur, work_item, my_span):
        new_records = {}
        histo_o = []

        start_time = datetime.now()

        query_my = self.getWeewxSelectSql(work_item)
        query_pg, query_args = self.prepareSqlInsertStructure()

        # get a cursor to our archive db
        myconn = self.getMSQLConnection(work_item['meteor'])
        my_cur = myconn.cursor()

        # execute the select statement
        my_cur.execute(query_my)
        row2 = my_cur.fetchone()

        # load field_name/row_id mapping for weewx select
        col_mapping = {}
        idx = 0
        nb_record_cached = 0
        while idx < len(my_cur.column_names):
            col_mapping[my_cur.column_names[idx]] = idx
            idx += 1

        nb_new_obs_all = 0
        nb_histo_inserted = 0
        nb_new_obs_master = 0
        last_obs_id = -1

        while row2 is not None:
            if row2[self.row_archive_usunits] != 16:
                raise Exception('bad usUnits: ' + str(row2[self.row_archive_usunits]) + ', dateTime(UTC): ' + str(row2[self.row_archive_dt_utc]))

            # reset dirty flag and load 3 first arg values
            for a_q in query_args:
                a_q['dirty'] = False
                utc_date = FromTimestampToDate(row2[self.row_archive_dt_utc] + a_q['valdk'] * 3600)

                a_q['args'] = [
                    str(work_item['pid']),
                    AsTimezone(utc_date, work_item['tz']).strftime('%Y-%m-%d %H:%M:%S'),
                    utc_date.strftime('%Y-%m-%d %H:%M:%S'),
                    str(row2[self.row_archive_interval] if a_q['valdk'] == 0 else 0)
                ]

            # load mesure values in our sql queries
            idx = 0
            while idx < len(self.measures):
                a_mesure = self.measures[idx]

                row_mesure_value = row2[idx + 3]                        # row values are in same order as self.measures

                # load value in the right insert statement, depending on valdk
                for a_q in query_args:
                    if a_q['valdk'] == a_mesure['valdk'] and row_mesure_value is not None:
                        a_q['args'].append(str(row_mesure_value))
                        a_q['dirty'] = True
                    else:
                        a_q['args'].append(None)
                idx += 1

            # send dirty queries to our database
            id_obs_main = 0
            for a_q in query_args:
                if a_q['dirty'] is True:
                    pg_cur.execute(query_pg, a_q['args'])
                    obs_new_id = pg_cur.fetchone()[0]
                    if a_q['valdk'] == 0:
                        # Only count main obs (ie. obs with val_deca = 0)
                        nb_new_obs_master += 1
                    histo_o.append([id_obs_main, obs_new_id])
                    nb_new_obs_all += 1
                    if id_obs_main == 0 and a_q['args'][2] != 0:
                        id_obs_main = obs_new_id

            # message for first insert
            if last_obs_id == -1 and id_obs_main != 0:
                last_obs_id = id_obs_main
                t.myTools.logInfo("first archive inserted, id: " + str(last_obs_id) + ", from local time: " + str(a_q['args'][1]), my_span, {"svc": "migrate", "meteor":  work_item['meteor']})

            # store min/max in our cache
            for a_mesure in self.measures:
                mid = a_mesure['id']
                # get value for the measure, or for the linked measure for omm measures
                if a_mesure['ommidx'] is None:
                    mesure_value = row2[col_mapping[a_mesure['col']]]
                else:
                    mesure_value = row2[col_mapping[self.measures[a_mesure['ommidx']]['col']]]

                if mesure_value is not None:
                    # get cached_mesure
                    if new_records.get('m_' + str(mid)) is None:
                        new_records['m_' + str(mid)] = {'mid': mid, 'cache': [], 'last': 0, 'last_in_db': 0}
                    mesure_cached_item = new_records['m_' + str(mid)]

                    # get local date
                    local_date = None
                    for a_query in query_args:
                        if a_q['valdk'] == a_mesure['valdk']:
                            local_date = a_q['args'][1].date()

                    # cache mesure as max/min
                    nb_record_cached += 1
                    self.load_min_max_from_archive_row(
                        a_mesure,
                        mesure_value,
                        None if a_mesure['diridx'] is None else row2[a_mesure['diridx']],
                        local_date,
                        id_obs_main,
                        mesure_cached_item)

            row2 = my_cur.fetchone()

        self.storeObsArray(pg_cur, histo_o)
        nb_histo_inserted = len(histo_o)
        histo_o = None

        if nb_new_obs_master > 0:
            t.myTools.logInfo('obs inserted, last id: ' + str(obs_new_id) + ", local time: " + str(a_q['args'][1]), my_span, {"svc": "migrate", "meteor":  work_item['meteor']})
            my_span.add_event('obs', str(nb_new_obs_master) + ' rows inserted (with deca == 0), total rows: ' + str(nb_new_obs_all))
            my_span.add_event('histo', str(nb_histo_inserted) + ' rows inserted')
        else:
            t.myTools.logInfo('no new obs inserted', my_span, {"svc": "migrate", "meteor":  work_item['meteor']})
            my_span.add_event('obs', 'no row inserted')
            my_span.add_event('histo', 'no row inserted')

        process_length = datetime.now() - start_time
        my_span.add_event('maxmin_step1', 'mesures ajoutées en cache: ' + str(nb_record_cached))
        my_span.add_event('insert_obs_minmax_from_weewx', 'processing: ' + str(process_length.microseconds/1000) + ' ms')
        return new_records

    # ------------------------------------
    # generate max/min from WeeWX records
    # ------------------------------------
    def load_maxmin_from_weewx(self, meteor, new_records, start_dt, end_dt, my_span):
        # check: nico use: last_in_db for insert-update or insert..
        start_time = datetime.now()
        myconn = self.getMSQLConnection(meteor)
        try:
            for a_mesure in self.measures:
                nb_record_added = 0
                mid = a_mesure['id']
                my_cur = myconn.cursor()
                try:
                    mesure_cache_item = new_records['m_' + str(mid)]

                    # get table name, fix for wind table
                    table_name = a_mesure['col']
                    if a_mesure['table'] is not None:
                        table_name = a_mesure['table']

                    # We need to use mintime/maxtime as the date of the record
                    # the mintime and maxtime can be on two different days...
                    if a_mesure['iswind'] is False:
                        my_query = \
                            'select mintime + 4 * 3600 as dateTime, min, mintime, null as max, null as maxtime, null as max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= '" + str(t.myTools.ToReunionTS(start_dt)) + "'" +\
                            " and dateTime < '" + str(t.myTools.ToReunionTS(end_dt)) + "'" +\
                            ' union ' + \
                            'select maxtime + 4 * 3600 as dateTime, null as min, null as mintime, max, maxtime, null as max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= '" + str(t.myTools.ToReunionTS(start_dt)) + "'" +\
                            " and dateTime < '" + str(t.myTools.ToReunionTS(end_dt)) + "'" +\
                            ' order by dateTime'
                    else:
                        my_query = \
                            'select mintime + 4 * 3600 as dateTime, min, mintime, null as max, null as maxtime, null as max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= '" + str(t.myTools.ToReunionTS(start_dt)) + "'" +\
                            " and dateTime < '" + str(t.myTools.ToReunionTS(end_dt)) + "'" +\
                            ' union ' + \
                            'select maxtime + 4 * 3600 as dateTime, null as min, null as mintime, max, maxtime, max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            " where dateTime >= '" + str(t.myTools.ToReunionTS(start_dt)) + "'" +\
                            " and dateTime < '" + str(t.myTools.ToReunionTS(end_dt)) + "'" +\
                            ' order by dateTime'

                    my_cur.execute(my_query)
                    row = my_cur.fetchone()
                    while row is not None:
                        if row[self.row_extreme_max] is not None or row[self.row_extreme_min] is not None:
                            nb_record_added += 1
                            self.load_min_max_from_extreme_row(a_mesure, row, mesure_cache_item)
                        row = my_cur.fetchone()
                finally:
                    my_cur.close()
                    if nb_record_added > 0:
                        process_length = datetime.now() - start_time
                        my_span.add_event('maxmin_from_weewx', str((nb_record_added - 1) / 2) + " nouveaux 'records' en cache pour " + a_mesure['field'] + ' en ' + str(process_length/1000) + ' ms')

        finally:
            myconn.close()

    # ----------------------------------
    # flush our cache into our database
    # ----------------------------------
    def loadExistingRecordsAndFlush(self, pg_cur, work_item, new_records, start_dt, end_dt, last_ts_in_extreme, my_span):
        # Add data from record tables
        self.load_maxmin_from_weewx(
            work_item['meteor'],
            new_records,
            self.roundDateTimeToAnExactDay(start_dt),
            self.roundDateTimeToAnExactDay(end_dt),
            my_span)

        # Build a global
        x_to_update = self.buildSortedGlobalArray(new_records, my_span)

        # Compact our global list
        self.compactCacheData(x_to_update, my_span)

        # Merge list in db
        self.mergeListInDB(pg_cur,  work_item['pid'], x_to_update, last_ts_in_extreme, my_span)

        x_to_update = []

    def buildSortedGlobalArray(self, new_records, my_span):
        # check: nico use: last_in_db for insert-update or insert..
        x_to_update = []
        start_dt = datetime.now()
        last_dt_in_cache = 0

        for a_mesure in self.measures:
            mesure_cached = new_records['m_' + str(a_mesure['id'])]
            if mesure_cached['last_in_db'] > last_dt_in_cache:
                last_dt_in_cache = mesure_cached['last_in_db']

            x_to_update += mesure_cached['cache']
            mesure_cached['cache'] = []             # free memory
        step1_length = datetime.now() - start_dt
        my_span.add_event('write_x_to_update', 'build x_to_update: length:' + str(len(x_to_update)) + ', time: ' + str(step1_length / 1000) + ' ms')

        # do a global sort
        start_dt = datetime.now()
        x_to_update.sort(key=lambda x: (x[self.row_cache_datetime], x[self.row_cache_mid]))
        sort_length = datetime.now() - start_dt
        my_span.add_event('x_to_update_sort', 'sort time:' + str(sort_length/1000) + ' ms')
        return x_to_update

    def compactCacheData(self, x_to_update, my_span):
        # compact our cache with same date, same measure_id
        start_dt = datetime.now()

        nb_active_row = 0
        last_item = None
        for an_item in x_to_update:
            # Different date/measure_id
            if last_item is None or \
                last_item[self.row_cache_datetime] != an_item[self.row_cache_datetime] or\
                    last_item[self.row_cache_mid] != an_item[self.row_cache_mid]:
                nb_active_row += 1
            else:
                # check min
                if an_item[self.row_cache_min] is None or (last_item[self.row_cache_min] is not None and last_item[self.row_cache_min] > an_item[self.row_cache_min]):
                    an_item[self.row_cache_min] = last_item[self.row_cache_min]
                    an_item[self.row_cache_mintime] = last_item[self.row_cache_mintime]
                    an_item[self.row_cache_obsid_min] = last_item[self.row_cache_obsid_min]
                # check max
                if an_item[self.row_cache_max] is None or (last_item[self.row_cache_max] is not None and last_item[self.row_cache_max] < an_item[self.row_cache_max]):
                    an_item[self.row_cache_max] = last_item[self.row_cache_max]
                    an_item[self.row_cache_maxtime] = last_item[self.row_cache_maxtime]
                    an_item[self.row_cache_maxdir] = last_item[self.row_cache_maxdir]
                    an_item[self.row_cache_obsid_max] = last_item[self.row_cache_obsid_max]
                # desactivate last_item
                last_item[self.row_cache_datetime] = None
            last_item = an_item

        compact_ms = datetime.now() - start_dt
        my_span.add_event('x_to_update_compact', 'size: ' + str(nb_active_row) + ', time: ' + str(compact_ms.seconds * 1000 + compact_ms.microseconds/1000) + ' ms')

    def mergeListInDB(self, pg_cur, pid, x_to_update, last_dt_in_cache, my_span):
        # check: nico use: last_in_db for insert-update or insert..
        insert_cde = "insert into extremes(date_local, poste_id, mesure_id, min, min_time, max, max_time, max_dir) values "
        nb_extremes_inserted = nb_extremes_updated = 0
        histo_x = []
        start_dt = datetime.now()

        for an_item in x_to_update:
            # skip compacted item
            if an_item[self.row_cache_datetime] is None:
                continue

            if an_item[self.row_cache_datetime] > last_dt_in_cache:
                # update data if already one extreme record exist for this date/poste/mid
                _, nb_upd = self.insertUpdateExtremes(pid, an_item, histo_x)
                if nb_upd > 0:
                    nb_extremes_updated += nb_upd
                    continue

            # Inserting a new row
            insert_sql = insert_cde + "("
            insert_sql += "'" + str(t.myTools.DateFromReuTS(an_item[self.row_cache_datetime])) + "', " + str(pid) + ", "
            insert_sql += "null, " if an_item[self.row_cache_mid] is None else (str(an_item[self.row_cache_mid]) + ", ")

            if an_item[self.row_cache_min] is None or an_item[self.row_cache_mintime] is None:
                insert_sql += "null, null, "
            else:
                insert_sql += str(an_item[self.row_cache_min]) + ", '" + str(t.myTools.DateFromReuTS(an_item[self.row_cache_mintime])) + "', "

            if an_item[self.row_cache_max] is None or an_item[self.row_cache_maxtime] is None:
                insert_sql += "null, null, null "
            else:
                insert_sql += str(an_item[self.row_cache_max]) + ", '" + str(t.myTools.DateFromReuTS(an_item[self.row_cache_maxtime])) + "', "
                if an_item[self.row_cache_maxdir] is None:
                    insert_sql += 'null '
                else:
                    insert_sql += str(an_item[self.row_cache_maxdir]) + " "

            insert_sql += ") returning id"

            pg_cur.execute(insert_sql)
            insert_sql = ""
            nb_extremes_inserted += 1
            x_id = pg_cur.fetchone()[0]

            if an_item[self.row_cache_obsid_min] is not None:
                histo_x.append([an_item[self.row_cache_obsid_min], x_id])
            if an_item[self.row_cache_obsid_max] is not None and an_item[self.row_cache_obsid_min] != an_item[self.row_cache_obsid_max]:
                histo_x.append([an_item[self.row_cache_obsid_max], x_id])

        sort_length = datetime.now() - start_dt
        sort_len = sort_length.seconds * 1000 + sort_length.microseconds/1000
        my_span.add_event('extremes', str(nb_extremes_inserted) + ' rows inserted, ' + str(nb_extremes_updated) + ' updated, time: ' + str(sort_len) + ' ms')

        # now insert/update histo extremes
        start_dt = datetime.now()
        self.storeHistoExtremeArray(pg_cur, histo_x)
        histo_x_length = datetime.now() - start_dt
        my_span.add_event(
            'histo_extreme',
            str(len(histo_x)) + ' rows inserted, time: ' + str(histo_x_length.seconds * 1000 + histo_x_length.microseconds/1000) + ' milliseconds')
        histo_x = []

    # -----------------------------------------------
    # create a virtual row from an weewx.archive row
    # -----------------------------------------------
    def load_min_max_from_archive_row(self, a_mesure, mesure_value, dir_value, dt, obs_id, mesure_cached_item):
        virtual_row = [
            self.roundTimeStampToAnExactDay(dt + a_mesure['mindk'] * 3600),
            mesure_value,
            None if mesure_value is None else dt,
            self.roundTimeStampToAnExactDay(dt + a_mesure['maxdk'] * 3600),
            mesure_value,
            None if mesure_value is None else dt,
            None if mesure_value is None else dir_value,
            a_mesure['id'],
            obs_id
        ]
        self.load_min_max(a_mesure, virtual_row, mesure_cached_item)

    # ----------------------------------------------
    # create a virtual row from an weewx record row
    # ----------------------------------------------
    def load_min_max_from_extreme_row(self, a_mesure, row, mesure_cached_item):
        row_virtual = [
            None if row[self.row_extreme_mintime] is None else self.roundTimeStampToAnExactDay(row[self.row_extreme_mintime] + a_mesure['mindk'] * 3600),
            row[self.row_extreme_min],
            None if row[self.row_extreme_min] is None else row[self.row_extreme_mintime],
            None if row[self.row_extreme_maxtime] is None else self.roundTimeStampToAnExactDay(row[self.row_extreme_maxtime] + a_mesure['maxdk'] * 3600),
            row[self.row_extreme_max],
            None if row[self.row_extreme_max] is None else row[self.row_extreme_maxtime],
            None if row[self.row_extreme_max] is None else row[self.row_extreme_maxdir],
            row[self.row_extreme_mid],
            -1
        ]
        self.load_min_max(a_mesure, row_virtual, mesure_cached_item)

    # -----------------------------------------
    # update cached extreme from a virtual row
    # -----------------------------------------
    def load_min_max(self, a_mesure, row, mesure_cached_item):
        if a_mesure['min'] is True and (row[self.row_virtual_min] is not None and row[self.row_virtual_mintime] is not None):
            cached_extreme = self.getCachedItem(mesure_cached_item, row[self.row_virtual_mindt], row[self.row_virtual_mid])
            if cached_extreme[self.row_cache_min] is None or row[self.row_virtual_min] < cached_extreme[self.row_cache_min]:
                cached_extreme[self.row_cache_min] = row[self.row_virtual_min]
                cached_extreme[self.row_cache_mintime] = row[self.row_virtual_mintime]
                cached_extreme[self.row_cache_obsid_min] = row[self.row_virtual_obsid]
                if row[self.row_virtual_obsid] is not None and row[self.row_virtual_mindt] > mesure_cached_item['last_in_db']:
                    mesure_cached_item['last_in_db'] = row[self.row_virtual_mindt]

        if a_mesure['max'] is True and (row[self.row_virtual_max] is not None and row[self.row_virtual_maxtime] is not None):
            cached_extreme = self.getCachedItem(mesure_cached_item, row[self.row_virtual_maxdt], row[self.row_virtual_mid])
            if cached_extreme[self.row_cache_max] is None or row[self.row_virtual_max] > cached_extreme[self.row_cache_max]:
                cached_extreme[self.row_cache_max] = row[self.row_virtual_max]
                cached_extreme[self.row_cache_maxtime] = row[self.row_virtual_maxtime]
                cached_extreme[self.row_cache_maxdir] = row[self.row_virtual_maxdir]
                cached_extreme[self.row_cache_obsid_max] = row[self.row_virtual_obsid]
                if row[self.row_virtual_obsid] is not None and row[self.row_virtual_maxdt] > mesure_cached_item['last_in_db']:
                    mesure_cached_item['last_in_db'] = row[self.row_virtual_maxdt]

    # --------------------------
    # return the extreme cached
    # --------------------------
    def getCachedItem(self, mesure_cached_item, dt, mid):
        # dt => self.roundTimeStampToAnExactDay
        # if  dt > mesure_cached_item['last'] => add new + mesure_cached_item['last'] = dt
        # if dt == mesure_cached_item['last'] => return mesure_cached_item['cache'][len(mesure_cached_item['last'] - 1)]
        pure_dt = self.roundTimeStampToAnExactDay(dt)

        # lucky the last one is asked..
        if pure_dt == mesure_cached_item['last']:
            return mesure_cached_item['cache'][len(mesure_cached_item['cache']) - 1]

        # Lookup in our cache in reverse order
        if pure_dt < mesure_cached_item['last']:
            for an_item in reversed(mesure_cached_item['cache']):
                if an_item[0] == pure_dt:
                    return an_item

        # add new cache item
        new_item = [pure_dt, mid, None, None, None, None, None, None, None]
        mesure_cached_item['cache'].append(new_item)
        mesure_cached_item['last'] = pure_dt
        return new_item

    # --------------------------------
    # return the sql select statement
    # --------------------------------
    def getWeewxSelectSql(self, work_item):
        query_my = "select dateTime, usUnits, `interval`"

        # load an array of query args, one for each valdk, update sql statement
        for a_mesure in self.measures:
            # add field name into our select statement for weewx
            query_my += ', ' + a_mesure['col']

        # finalize sql statements
        query_my += " from archive where dateTime >= " + str(work_item['start_ts'])
        query_my += " and dateTime < " + str(work_item['end_ts'])

        # query_my += " order by dateTime"""
        query_my += " order by dateTime"
        return query_my

    # -----------------------------------
    # prepare an array of sql to execute
    # -----------------------------------
    def prepareSqlInsertStructure(self):
        query_args = []
        query_pg1 = "insert into obs(poste_id, dt_local, dt_utc, duration"
        query_pg2 = ") values ( %s, %s, %s, %s"      # id_obs has to be the last

        # load an array of query args, one for each valdk, update sql statement
        for a_mesure in self.measures:
            b_found = False
            for a_deca in query_args:
                if a_deca['valdk'] == a_mesure['valdk']:
                    b_found = True
                    break
            if b_found is False:
                query_args.append({'valdk': a_mesure['valdk'], 'dirty': False, 'args': []})

            # add field name into our insert statements for pg
            query_pg1 += ", " + a_mesure['field']
            query_pg2 += ', %s'

        # finalize sql statements
        query_pg = query_pg1 + query_pg2 + ") returning id;"""
        return query_pg, query_args

    # -----------------------
    # misc utility functions
    # -----------------------
    def get_min_valdk(self):
        min_valdk = 0
        for a_m in self.measures:
            if a_m['mindk'] < min_valdk:
                min_valdk = a_m['mindk']
            if a_m['maxdk'] < min_valdk:
                min_valdk = a_m['maxdk']
        return min_valdk

    # -------------------------
    # insert or update extreme
    # -------------------------
    def insertUpdateExtremes(self, pid, an_item, histo_x):
        nb_insert = 0
        nb_update = 0

        x_dt = t.myTools.DateFromReuTS(an_item[self.row_cache_datetime]).date()
        current_x = ExtremeMeteor.get_extreme(pid, an_item[self.row_cache_mid], x_dt)
        x_dirty = x_min = x_max = False

        if an_item[self.row_cache_min] is not None:
            if current_x.data.min is None or an_item[self.row_cache_min] < current_x.data.min:
                current_x.data.min = an_item[self.row_cache_min]
                current_x.data.min_time = t.myTools.DateFromReuTS(an_item[self.row_cache_mintime])
                x_dirty = True
                x_min = True

        if an_item[self.row_cache_max] is not None:
            if current_x.data.max is None or an_item[self.row_cache_max] < current_x.data.max:
                current_x.data.max = an_item[self.row_cache_max]
                current_x.data.max_time = t.myTools.DateFromReuTS(an_item[self.row_cache_maxtime])
                current_x.data.max_dir = an_item[self.row_cache_maxdir]
                x_dirty = True
                x_max = True

        if x_dirty is True:
            if current_x.data.id is None:
                current_x.save()
                nb_insert += 1
            else:
                current_x.save()
                nb_update += 1

            if x_min is True and an_item[self.row_cache_obsid_min] is not None:
                histo_x.append([an_item[self.row_cache_obsid_min], current_x.data.id])
            if x_max is True and (x_min is None or an_item[self.row_cache_obsid_max != an_item[self.row_cache_obsid_min]]):
                if an_item[self.row_cache_obsid_max] is not None:
                    histo_x.append([an_item[self.row_cache_obsid_max], current_x.data.id])
        return nb_insert, nb_update

    def get_poste_info(self, meteor, my_span):
        pgconn = None
        poste_id = None
        last_obs_ts = None
        last_x_ts = None

        try:
            pgconn = self.getPGConnexion()
            pg_cur = pgconn.cursor()
            pg_cur.execute("select id, last_obs_date, last_extremes_date, load_json from postes where meteor = '" + meteor + "'")
            row = pg_cur.fetchone()
            if row is not None:
                poste_id = row[0]
                last_obs_ts = datetime.now() if row[1] is None else row[1]
                last_x_ts = datetime.now() if row[2] is None else row[2]
                load_json = row[3]
            # my_span.set_attribute('meteor', meteor)
            my_span.set_attribute('last_obs_ts', t.myTools.ToLocalTS(last_obs_ts) if last_obs_ts is not None else 'None')
            my_span.set_attribute('last_extremes_ts', t.myTools.ToLocalTS(last_x_ts) if last_x_ts is not None else 'None')

        finally:
            pg_cur.close()
            pgconn.close()
            return poste_id, last_obs_ts, last_x_ts, load_json

    def getMeasures(self, pgconn):
        mesures = []
        pg_query = "select id, archive_col, archive_table, field_dir, json_input, val_deca, min, min_deca, max, max_deca, is_avg, is_wind, allow_zero, omm_link from mesures order by id"

        pg_cur = pgconn.cursor()
        pg_cur.execute(pg_query)
        row = pg_cur.fetchone()
        while row is not None:
            one_mesure = {
                'id': row[0],
                'col': row[1],
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
                    dir_idx += 1
        return mesures

    def get_omm_link(self):
        omm_link = []
        m_idx = 0

        while m_idx < len(self.measures):
            if self.measures[m_idx]['ommidx'] is not None:
                my_mesure_data = None
                my_omm_mesure = self.measures[m_idx]
                my_mesure = self.measures[my_omm_mesure['ommidx']]
                for an_omm_link in omm_link:
                    if an_omm_link['base_idx'] == my_omm_mesure['ommidx']:
                        my_mesure_data = an_omm_link
                if my_mesure_data is None:
                    my_mesure_data = {'base_idx': my_omm_mesure['ommidx'], 'col': my_mesure['col'], 'ins_idx': -1, 'omms': []}
                    omm_link.append(my_mesure_data)
                my_mesure_data['omms'].append({'ommidx': m_idx, 'col': my_omm_mesure['col'], 'decas': [my_omm_mesure['valdk'], my_omm_mesure['maxdk'], my_omm_mesure['mindk']], 'ins_idx': 0})
            m_idx += 1

        return omm_link

    def storeObsArray(self, pg_cur, data):
        if len(data) == 0:
            return
        sql_str = "insert into histo_obs (src_obs_id, target_obs_id) values "
        b_hasdata = False
        data.sort(key=lambda x: (x[0], x[1]))
        d0 = d1 = -1
        for an_item in data:
            if len(an_item) != 2 or an_item[0] is None or an_item[1] is None:
                continue
            if an_item[1] <= 0 or an_item[0] <= 0 or (d0 == an_item[0] and d1 == an_item[1]):
                continue
            sql_str += '(' + str(an_item[0]) + ', ' + str(an_item[1]) + '), '
            d0 = an_item[0]
            d1 = an_item[1]
            b_hasdata = True
        if b_hasdata is True:
            pg_cur.execute(sql_str[0:-2])

    def storeHistoExtremeArray(self, pg_cur, data):
        if len(data) == 0:
            return
        sql_str = "insert into histo_extreme (src_obs_id, target_x_id) values "
        b_hasdata = False
        data.sort(key=lambda x: (x[0], x[1]))
        d0 = d1 = -1
        for an_item in data:
            if len(an_item) != 2 or an_item[0] is None or an_item[1] is None:
                continue
            if an_item[1] <= 0 or an_item[0] <= 0 or (d0 == an_item[0] and d1 == an_item[1]):
                continue
            sql_str += '(' + str(an_item[0]) + ', ' + str(an_item[1]) + '), '
            d0 = an_item[0]
            d1 = an_item[1]
            b_hasdata = True
        if b_hasdata is True:
            pg_cur.execute(sql_str[0:-2])

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

    def roundTimeStampToAnExactDay(self, ts):
        return ts - (ts % 86400)

    def roundDateTimeToAnExactDay(self, dt):
        return datetime(dt.year, dt.month, dt.day)

    def loadSelfVariables(self):
        pgconn = None
        try:
            pgconn = self.getPGConnexion()

            # load mesures definition in memory
            self.measures = self.getMeasures(pgconn)

            # load omm link array, between base mesures and linked omm mesures
            self.omm_link = self.get_omm_link()

            # row_id for select from archive data, first 4 fields
            self.row_archive_dt_utc = 0
            self.row_archive_usunits = 1
            self.row_archive_interval = 2

            # row_id for extreme data
            self.row_extreme_datetime = 0
            self.row_extreme_min = 1
            self.row_extreme_mintime = 2
            self.row_extreme_max = 3
            self.row_extreme_maxtime = 4
            self.row_extreme_maxdir = 5
            self.row_extreme_mid = 6
            self.row_extreme_id = 7

            # row_id for virtual data
            self.row_virtual_mindt = 0
            self.row_virtual_min = 1
            self.row_virtual_mintime = 2
            self.row_virtual_maxdt = 3
            self.row_virtual_max = 4
            self.row_virtual_maxtime = 5
            self.row_virtual_maxdir = 6
            self.row_virtual_mid = 7
            self.row_virtual_obsid = 8

            self.row_cache_datetime = 0
            self.row_cache_mid = 1
            self.row_cache_min = 2
            self.row_cache_mintime = 3
            self.row_cache_obsid_min = 4
            self.row_cache_max = 5
            self.row_cache_maxtime = 6
            self.row_cache_maxdir = 7
            self.row_cache_obsid_max = 8

        finally:
            if pgconn is not None:
                pgconn.close()
