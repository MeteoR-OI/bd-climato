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
from datetime import datetime
from app.classes.repository.extremeMeteor import ExtremeMeteor
from app.classes.repository.histoObs import HistoObsMeteor
from app.classes.repository.histoExtreme import HistoExtreme
from app.tools.myTools import logException


# --------------------------------------
# our class is called by worker service
#    need some methods...
# --------------------------------------
class MigrateDB:
    def __init__(self):
        self._meteors_to_process = []
        self.load_self_variables()

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

        t.logInfo("New work item added in queue", None, {"svc": "migrate", "meteor": meteor, "work_item": self._meteors_to_process[len(self._meteors_to_process) - 1]})

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
    def processWorkItem(self, work_item, my_span, op_tracer):
        try:
            meteor = work_item['meteor']
            work_item['pid'], str_last_obs_ts, str_last_x_ts, load_json = self.get_poste_info(meteor, my_span)
            if work_item['pid'] is None:
                raise Exception('station ' + meteor + ' not found')

            work_item['last_obs_ts'] = str_last_obs_ts.timestamp() if str_last_obs_ts is not None else 0
            work_item['last_x_ts'] = str_last_x_ts.timestamp() if str_last_x_ts is not None else 0

            # skipping postes with active updates
            if load_json is True:
                my_span.add_event('migrate', 'load_json is active, skipping')
                return

            cached_data = {}
            with op_tracer.start_as_current_span('ecritures des obs + caching min-max') as my_span:
                self.insert_obs_minmax_from_weewx(work_item, cached_data, my_span)

            with op_tracer.start_as_current_span('mise en cache des records WeeWX') as my_span:
                self.load_maxmin_from_weewx(work_item, cached_data, my_span)

            with op_tracer.start_as_current_span('ecritures des records') as my_span:
                self.write_extreme_rows(work_item, cached_data, my_span)

            # work_item['cur_year'] = 2000 if str_last_x_ts is None else str_last_x_ts.year()
            # work_item['max_year'] = datetime.datetime.today().year

            # # process year per year, to decrease memory pressure
            # while work_item['cur_year'] <= work_item['max_year']:
            #     # cached_data = {}    # [{m_<id>: mesure_id, {'mid': mid, 'cache': [], 'last': 0, 'last_in_db': 0}}]
            #     work_item['end_ts'] = datetime.datetime(work_item['cur_year'], 12, 31, 23, 59, 59, 59).timestamp() + 4 * 3600 + 1

            #     # with op_tracer.start_as_current_span('year ' + str(work_item['cur_year'])):
            #     #     with op_tracer.start_as_current_span('generation des records a partir des mesures ') as my_span:
            #     #         self.load_maxmin_from_mesures(work_item, cached_data, mapping_rowno_obsid, my_span)

            #     with op_tracer.start_as_current_span('mise en cache des records WeeWX') as my_span:
            #         self.load_maxmin_from_weewx(work_item, cached_data, my_span)

            #     with op_tracer.start_as_current_span('ecritures des records') as my_span:
            #         self.write_extreme_rows(work_item, cached_data, my_span)

            #     # adjust our next starting timestamp
            #     work_item['last_x_ts'] = datetime.datetime(work_item['cur_year'], 12, 31, 23, 59, 59).timestamp()
            #     work_item['cur_year'] += 1

        except Exception as e:
            t.logException(e)
            raise (e)

    # ---------------------------------------
    # other methods specific to this service
    # ---------------------------------------

    # ---------------------------------------------------
    # insert mesures from weewx archive in our obs table
    # ---------------------------------------------------
    def insert_obs_minmax_from_weewx(self, work_item, cached_data, my_span):
        start_time = datetime.now()

        last_ts_in_obs = work_item['last_obs_ts']
        pid = work_item['pid']
        meteor = work_item['meteor']
        histo_o = []

        if last_ts_in_obs > 0:
            str_date = datetime.utcfromtimestamp(last_ts_in_obs).strftime('%Y-%m-%d %H:%M:%S')
            my_span.add_event('migrate', 'starting migration from archive with timestamp: ' + str(last_ts_in_obs) + ' (' + str(str_date) + ')')
        else:
            my_span.add_event('migrate', 'starting a full migration from all archives')

        last_ts_in_extreme = work_item['last_x_ts']
        if last_ts_in_extreme > 0:
            str_date = datetime.utcfromtimestamp(last_ts_in_extreme).strftime('%Y-%m-%d %H:%M:%S')
            my_span.add_event('maxmin_begin', 'mise en cache des max/min depuis: ' + str(last_ts_in_extreme) + ' (' + str(str_date) + ')')
        else:
            my_span.add_event('maxmin_begin', 'mise en cache de tous les max/min')

        query_my = self.get_weewx_select_sql(last_ts_in_obs, None)
        query_pg, query_args = self.prepare_sql_insert_structure()

        # get our cursors
        pgconn = self.getPGConnexion()
        pg_cur = pgconn.cursor()

        myconn = self.getMSQLConnection(meteor)
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

        nb_obs_inserted = 0
        nb_histo_inserted = 0
        nb_new_obs = 0
        last_obs_id = -1

        while row2 is not None:
            if row2[self.row_archive_usunits] != 16:
                raise Exception('bad usUnits: ' + str(row2[self.row_archive_usunits]) + ', dateTime: ' + str(row2[self.row_archive_datetime_dt]))

            # reset dirty flag
            for a_q in query_args:
                a_q['dirty'] = False
                str_date = datetime.utcfromtimestamp(row2[self.row_archive_datetime_dt] + a_q['valdk'] * 3600).strftime('%Y-%m-%d %H:%M:%S')
                a_q['args'] = [
                    str(pid),
                    str_date,
                    str(row2[self.row_archive_interval] if a_q['valdk'] == 0 else 0)
                ]

            # load mesure values in our sql queries
            idx = 0
            while idx < len(self.mesures):
                a_mesure = self.mesures[idx]
                row_mesure_value = row2[idx + 4]         # row values are in same order as self.mesures

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
                    histo_o.append([id_obs_main, obs_new_id])
                    nb_obs_inserted += 1
                    if a_q['valdk'] == 0:
                        # Only count main obs (ie. obs with val_deca = 0)
                        nb_new_obs += 1
                    if id_obs_main == 0 and a_q['args'][2] != 0:
                        id_obs_main = obs_new_id
            # mapping_rowno_obsid.append(id_obs_main if id_obs_main > 0 else -1)

            # message for first insert
            if last_obs_id == -1 and id_obs_main != 0:
                last_obs_id = id_obs_main
                t.logInfo("first archive inserted, id: " + str(last_obs_id) + ", from date: " + str(a_q['args'][1]), my_span, {"svc": "migrate", "meteor": meteor})

            # message if first data did not insert a 'main' obs
            if last_obs_id == -1 and pg_cur.rowcount > 0:
                last_obs_id = pg_cur.fetchone()[0]
                t.logInfo("first archive-0 inserted, id: " + str(last_obs_id) + ", from date: " + str(a_q['args'][1]), my_span, {"svc": "migrate", "meteor": meteor})

            # store min/max in our cache
            for a_mesure in self.mesures:
                mid = a_mesure['id']
                if a_mesure['ommidx'] is None:
                    mesure_value = row2[col_mapping[a_mesure['col']]]
                else:
                    mesure_value = row2[col_mapping[self.mesures[a_mesure['ommidx']]['col']]]

                # get cached_mesure
                if cached_data.get('m_' + str(mid)) is None:
                    cached_data['m_' + str(mid)] = {'mid': mid, 'cache': [], 'last': 0, 'last_in_db': last_ts_in_extreme}
                mesure_cached_item = cached_data['m_' + str(mid)]

                # cache mesure as max/min
                nb_record_cached += 1
                mesure_dir = None if a_mesure['diridx'] is None else row2[a_mesure['diridx']]
                self.load_min_max_from_archive_row(a_mesure, mesure_value, mesure_dir, row2[self.row_archive_datetime], id_obs_main, mesure_cached_item)

            # commit every 10 000 rows
            if nb_obs_inserted > 10000:
                pgconn.commit()
                pg_cur.close()
                pg_cur = pgconn.cursor()
                nb_obs_inserted = 0
                HistoObsMeteor.storeArray(pgconn, histo_o)
                pgconn.commit()
                nb_histo_inserted += len(histo_o)
                histo_o = []

            row2 = my_cur.fetchone()

        pgconn.commit()
        pg_cur.close()
        HistoObsMeteor.storeArray(pgconn, histo_o)
        pgconn.commit()
        nb_histo_inserted += len(histo_o)
        histo_o = []
        pgconn.close()

        if nb_new_obs > 0:
            t.logInfo('obs inserted, last id: ' + str(obs_new_id) + ", date: " + str(a_q['args'][1]), my_span, {"svc": "migrate", "meteor": meteor})
            my_span.add_event('obs', str(nb_new_obs) + ' rows inserted (with deca == 0)')
            my_span.add_event('histo', str(nb_histo_inserted) + ' rows inserted')
        else:
            t.logInfo('no new obs inserted', my_span, {"svc": "migrate", "meteor": meteor})
            my_span.add_event('obs', 'no row inserted')
            my_span.add_event('histo', 'no row inserted')

        process_length = datetime.now() - start_time
        my_span.add_event('maxmin_step1', 'mesures ajoutées en cache: ' + str(nb_record_cached))
        my_span.add_event('insert_obs_minmax_from_weewx', 'processing: ' + str(process_length.microseconds/1000) + ' ms')

    # ------------------------------------
    # generate max/min from WeeWX records
    # ------------------------------------
    def load_maxmin_from_weewx(self, work_item, cached_data, my_span):
        start_time = datetime.now()
        last_ts_in_extremes = work_item['last_x_ts']
        myconn = self.getMSQLConnection(work_item['meteor'])
        try:
            for a_mesure in self.mesures:
                nb_record_added = 0
                mid = a_mesure['id']
                my_cur = myconn.cursor()
                try:
                    # get cached_mesure
                    if cached_data.get('m_' + str(mid)) is None:
                        cached_data['m_' + str(mid)] = {'mid': mid, 'cache': [], 'last': 0, 'last_in_db': last_ts_in_extremes}
                    mesure_cache_item = cached_data['m_' + str(mid)]

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
                            ' where dateTime > ' + str(last_ts_in_extremes - 4 * 3600) +\
                            ' union ' + \
                            'select maxtime + 4 * 3600 as dateTime, null as min, null as mintime, max, maxtime, null as max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            ' where dateTime > ' + str(last_ts_in_extremes - 4 * 3600) +\
                            ' order by dateTime'
                    else:
                        my_query = \
                            'select mintime + 4 * 3600 as dateTime, min, mintime, null as max, null as maxtime, null as max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            ' where dateTime > ' + str(last_ts_in_extremes - 4 * 3600) +\
                            ' union ' + \
                            'select maxtime + 4 * 3600 as dateTime, null as min, null as mintime, max, maxtime, max_dir, ' + str(mid) + ' as mid ' + \
                            ' from archive_day_' + table_name +\
                            ' where dateTime > ' + str(last_ts_in_extremes - 4 * 3600) +\
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

        except Exception as e:
            logException(e)
            raise e

        finally:
            myconn.close()

    # ----------------------------------
    # flush our cache into our database
    # ----------------------------------
    def write_extreme_rows(self, work_item, cached_data, my_span):
        pid = work_item['pid']
        x_to_update = []
        insert_cde = "insert into extremes (date, poste_id, mesure_id, min, min_time, max, max_time, max_dir) values "

        pgconn = self.getPGConnexion()
        pg_cur = pgconn.cursor()

        start_dt = datetime.now()
        last_dt_in_cache = 0
        for a_mesure in self.mesures:
            mesure_cached = cached_data['m_' + str(a_mesure['id'])]
            if mesure_cached['last_in_db'] > last_dt_in_cache:
                last_dt_in_cache = mesure_cached['last_in_db']
            for an_item in mesure_cached['cache']:
                x_to_update.append(an_item)
            mesure_cached['cache'] = []             # free memory
        step1_length = datetime.now() - start_dt
        my_span.add_event('write_x_array', 'build global array: length:' + str(len(x_to_update)) + ', time: ' + str(step1_length / 1000) + ' ms')

        # do a global sort
        start_dt = datetime.now()
        x_to_update.sort(key=lambda x: (x[self.row_cache_datetime], x[self.row_cache_mid]))
        sort_length = datetime.now() - start_dt
        my_span.add_event('write_x_sort', 'sort time:' + str(sort_length/1000) + ' ms')

        # compact our cache with same date, same measure_id
        start_dt = datetime.now()

        main_row = []
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

                if main_row[self.row_cache_min] is None or (an_item[self.row_cache_min] is not None and an_item[self.row_cache_min] < main_row[self.row_cache_min]):
                    main_row[self.row_cache_min] = an_item[self.row_cache_min]
                    main_row[self.row_cache_mintime] = an_item[self.row_cache_mintime]
                    main_row[self.row_cache_obsid_min] = an_item[self.row_cache_obsid_min]
                if main_row[self.row_cache_max] is None or (an_item[self.row_cache_max] is not None and an_item[self.row_cache_max] > main_row[self.row_cache_max]):
                    main_row[self.row_cache_max] = an_item[self.row_cache_max]
                    main_row[self.row_cache_maxtime] = an_item[self.row_cache_maxtime]
                    main_row[self.row_cache_maxdir] = an_item[self.row_cache_maxdir]
                    main_row[self.row_cache_obsid_max] = an_item[self.row_cache_obsid_max]
                an_item[self.row_cache_datetime] = None
            last_item = an_item

        # process last in our array
        if len(main_row) > 0 and \
            last_item is not None and\
            main_row[self.row_cache_datetime] == last_item[self.row_cache_datetime] and\
                main_row[self.row_cache_mid] == last_item[self.row_cache_mid]:

            if main_row[self.row_cache_min] is None or (last_item[self.row_cache_min] is not None and last_item[self.row_cache_min] < main_row[self.row_cache_min]):
                main_row[self.row_cache_min] = last_item[self.row_cache_min]
                main_row[self.row_cache_mintime] = last_item[self.row_cache_mintime]
                main_row[self.row_cache_obsid_min] = an_item[self.row_cache_obsid_min]
            if main_row[self.row_cache_max] is None or (last_item[self.row_cache_max] is not None and last_item[self.row_cache_max] > main_row[self.row_cache_max]):
                main_row[self.row_cache_max] = last_item[self.row_cache_max]
                main_row[self.row_cache_maxtime] = last_item[self.row_cache_maxtime]
                main_row[self.row_cache_maxdir] = last_item[self.row_cache_maxdir]
                main_row[self.row_cache_obsid_max] = an_item[self.row_cache_obsid_max]
            last_item[self.row_cache_datetime] = None

        sort_length = datetime.now() - start_dt
        # my_span.add_event('compacting length: ' + str(nb_active_row) + ', time: ' + str(sort_length.seconds * 1000 + sort_length.microseconds/1000) + ' milliseconds')

        # now insert/update extremes from our compacted array
        start_dt = datetime.now()

        nb_extremes_inserted = nb_extremes_updated = 0
        histo_x = []

        for an_item in x_to_update:
            # skip compacted item
            if an_item[self.row_cache_datetime] is None:
                continue

            if an_item[self.row_cache_datetime] >= last_dt_in_cache:
                insert_sql = insert_cde + "("
                insert_sql += "'" + str(datetime.fromtimestamp(an_item[self.row_cache_datetime])) + "', " + str(pid) + ", "
                insert_sql += "null, " if an_item[self.row_cache_mid] is None else (str(an_item[self.row_cache_mid]) + ", ")

                if an_item[self.row_cache_min] is None or an_item[self.row_cache_mintime] is None:
                    insert_sql += "null, null, "
                else:
                    insert_sql += str(an_item[self.row_cache_min]) + ", '" + str(datetime.fromtimestamp(an_item[self.row_cache_mintime])) + "', "

                if an_item[self.row_cache_max] is None or an_item[self.row_cache_maxtime] is None:
                    insert_sql += "null, null, null "
                else:
                    insert_sql += str(an_item[self.row_cache_max]) + ", '" + str(datetime.fromtimestamp(an_item[self.row_cache_maxtime])) + "', "
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
            else:
                nb_ins, nb_upd = self.insert_update_extremes(work_item, an_item, histo_x)
                nb_extremes_inserted += nb_ins
                nb_extremes_updated += nb_upd

        sort_length = datetime.now() - start_dt
        sort_len = sort_length.seconds * 1000 + sort_length.microseconds/1000
        my_span.add_event('extremes', str(nb_extremes_inserted) + ' rows extremes inserted, ' + str(nb_extremes_updated) + ' updated, time: ' + str(sort_len) + ' milliseconds')

        # now insert/update histo extremes
        start_dt = datetime.now()

        HistoExtreme.storeArray(pgconn, histo_x)
        histo_x_length = datetime.now() - start_dt
        my_span.add_event(
            'histo_extreme',
            str(len(histo_x)) + ' rows inserted, time: ' + str(histo_x_length.seconds * 1000 + histo_x_length.microseconds/1000) + ' milliseconds')
        histo_x = []
        x_to_update = []
        pgconn.commit()
        pgconn.close()

    # -----------------------------------------------
    # create a virtual row from an weewx.archive row
    # -----------------------------------------------
    def load_min_max_from_archive_row(self, a_mesure, mesure_value, dir_value, dt, obs_id, mesure_cached_item):
        virtual_row = [
            self.round_ts_to_an_exact_day(dt + a_mesure['mindk'] * 3600),
            mesure_value,
            None if mesure_value is None else dt,
            self.round_ts_to_an_exact_day(dt + a_mesure['maxdk'] * 3600),
            mesure_value,
            None if mesure_value is None else dt,
            None if mesure_value is None else dir_value,
            a_mesure['id'],
            obs_id
        ]

        if self.round_ts_to_an_exact_day(dt + a_mesure['mindk'] * 3600) in ('2022-02-02', '2022-02-03') and a_mesure['field'] == 'gust':
            print('day to check - wind 98.1702280006065')
        self.load_min_max(a_mesure, virtual_row, mesure_cached_item)

    # ----------------------------------------------
    # create a virtual row from an weewx record row
    # ----------------------------------------------
    def load_min_max_from_extreme_row(self, a_mesure, row, mesure_cached_item):
        row_virtual = [
            None if row[self.row_extreme_mintime] is None else self.round_ts_to_an_exact_day(row[self.row_extreme_mintime] + a_mesure['mindk'] * 3600),
            row[self.row_extreme_min],
            None if row[self.row_extreme_min] is None else row[self.row_extreme_mintime],
            None if row[self.row_extreme_maxtime] is None else self.round_ts_to_an_exact_day(row[self.row_extreme_maxtime] + a_mesure['maxdk'] * 3600),
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
            cached_extreme = self.get_cached_item(mesure_cached_item, row[self.row_virtual_mindt], row[self.row_virtual_mid])
            if cached_extreme[self.row_cache_min] is None or row[self.row_virtual_min] < cached_extreme[self.row_cache_min]:
                cached_extreme[self.row_cache_min] = row[self.row_virtual_min]
                cached_extreme[self.row_cache_mintime] = row[self.row_virtual_mintime]
                cached_extreme[self.row_cache_obsid_min] = row[self.row_virtual_obsid]
                if row[self.row_virtual_obsid] is not None and row[self.row_virtual_mindt] > mesure_cached_item['last_in_db']:
                    mesure_cached_item['last_in_db'] = row[self.row_virtual_mindt]

        if a_mesure['max'] is True and (row[self.row_virtual_max] is not None and row[self.row_virtual_maxtime] is not None):
            cached_extreme = self.get_cached_item(mesure_cached_item, row[self.row_virtual_maxdt], row[self.row_virtual_mid])
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
    def get_cached_item(self, mesure_cached_item, dt, mid):
        # dt => self.round_ts_to_an_exact_day
        # if  dt > mesure_cached_item['last'] => add new + mesure_cached_item['last'] = dt
        # if dt == mesure_cached_item['last'] => return mesure_cached_item['cache'][len(mesure_cached_item['last'] - 1)]
        pure_dt = self.round_ts_to_an_exact_day(dt)
        if pure_dt < mesure_cached_item['last']:
            for an_item in reversed(mesure_cached_item['cache']):
                if an_item[0] == pure_dt:
                    return an_item
        else:
            if pure_dt == mesure_cached_item['last']:
                return mesure_cached_item['cache'][len(mesure_cached_item['cache']) - 1]
        # add new cache item
        new_item = [pure_dt, mid, None, None, None, None, None, None, None]
        mesure_cached_item['cache'].append(new_item)
        return new_item

    # --------------------------------
    # return the sql select statement
    # --------------------------------
    def get_weewx_select_sql(self, last_ts_in_obs, end_ts=None):
        query_my = "select dateTime, dateTime + (4 * 3600), usUnits, `interval`"

        # load an array of query args, one for each valdk, update sql statement
        for a_mesure in self.mesures:
            # add field name into our select statement for weewx
            query_my += ', ' + a_mesure['col']

        # finalize sql statements
        query_my += " from archive where dateTime > " + str(last_ts_in_obs)
        if end_ts is not None:
            query_my += " and dateTime < " + str(end_ts)
        # query_my += " order by dateTime"""
        query_my += " order by dateTime"
        return query_my

    # -----------------------------------
    # prepare an array of sql to execute
    # -----------------------------------
    def prepare_sql_insert_structure(self):
        query_args = []
        query_pg1 = "insert into obs(poste_id, time, duration"
        query_pg2 = ") values ( %s, %s, %s"      # id_obs has to be the last

        # load an array of query args, one for each valdk, update sql statement
        for a_mesure in self.mesures:
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
        for a_m in self.mesures:
            if a_m['mindk'] < min_valdk:
                min_valdk = a_m['mindk']
            if a_m['maxdk'] < min_valdk:
                min_valdk = a_m['maxdk']
        return min_valdk

    # -------------------------
    # insert or update extreme
    # -------------------------
    def insert_update_extremes(self, work_item, an_item, histo_x):
        pid = work_item['pid']
        nb_insert = 0
        nb_update = 0
        # self.row_cache_datetime = 0
        # self.row_cache_mid = 1
        # self.row_cache_min = 2
        # self.row_cache_mintime = 3
        # self.row_cache_obsid_min = 4
        # self.row_cache_max = 5
        # self.row_cache_maxtime = 6
        # self.row_cache_maxdir = 7
        # self.row_cache_obsid_max = 8

        x_dt = datetime.fromtimestamp(an_item[self.row_cache_datetime]).date()
        current_x = ExtremeMeteor.get_extreme(pid, an_item[self.row_cache_mid], x_dt)
        x_dirty = x_min = x_max = False

        if an_item[self.row_cache_min] is not None:
            if current_x.data.min is None or an_item[self.row_cache_min] < current_x.data.min:
                current_x.data.min = an_item[self.row_cache_min]
                current_x.data.min_time = datetime.fromtimestamp(an_item[self.row_cache_mintime])
                x_dirty = True
                x_min = True

        if an_item[self.row_cache_max] is not None:
            if current_x.data.max is None or an_item[self.row_cache_max] < current_x.data.max:
                current_x.data.max = an_item[self.row_cache_max]
                current_x.data.max_time = datetime.fromtimestamp(an_item[self.row_cache_maxtime])
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
                last_obs_ts = None if row[1] is None else row[1]
                last_x_ts = None if row[2] is None else row[2]
                load_json = row[3]
            # my_span.set_attribute('meteor', meteor)
            my_span.set_attribute('last_obs_ts', last_obs_ts.timestamp() if last_obs_ts is not None else 'None')
            my_span.set_attribute('last_extremes_ts', last_x_ts.timestamp() if last_x_ts is not None else 'None')

        except Exception as e:
            t.logException(e, my_span)
            poste_id = None

        finally:
            pg_cur.close()
            pgconn.close()
            return poste_id, last_obs_ts, last_x_ts, load_json

    def get_mesures(self, pgconn):
        mesures = []
        pg_query = "select id, archive_col, archive_table, field_dir, json_input, val_deca, min, min_deca, max, max_deca, is_avg, is_wind, allow_zero, omm_link from mesures"

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
        my_cur.execute("set time_zone = '+00:00'")
        myconn.commit()
        my_cur.close()

        return myconn

    def round_ts_to_an_exact_day(self, timestamp):
        return timestamp - (timestamp % 86400)

    def load_self_variables(self):
        pgconn = None
        try:
            pgconn = self.getPGConnexion()

            # load mesures definition in memory
            self.mesures = self.get_mesures(pgconn)
            # load omm link array, between base mesures and linked omm mesures
            self.omm_link = self.get_omm_link()

            # row_id for archive data
            self.row_archive_datetime = 0
            self.row_archive_datetime_dt = 1
            self.row_archive_usunits = 2
            self.row_archive_interval = 3

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
            # self.row_virtual_datetime_min = 0
            # self.row_virtual_min = 1
            # self.row_virtual_mintime = 2
            # self.row_virtual_datetime_max = 3
            # self.row_virtual_max = 4
            # self.row_virtual_maxtime = 5
            # self.row_virtual_maxdir = 6
            # self.row_virtual_obsid_min = 7
            # self.row_virtual_mid = 8
            # self.row_virtual_id = 9

            self.row_cache_datetime = 0
            self.row_cache_mid = 1
            self.row_cache_min = 2
            self.row_cache_mintime = 3
            self.row_cache_obsid_min = 4
            self.row_cache_max = 5
            self.row_cache_maxtime = 6
            self.row_cache_maxdir = 7
            self.row_cache_obsid_max = 8

        except Exception as e:
            logException(e)

        finally:
            if pgconn is not None:
                pgconn.close()
