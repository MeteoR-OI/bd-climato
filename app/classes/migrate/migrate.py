# migrate process
#   addNewWorkItem(self, work_item)
#       add a db in the todo list
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item):
#       Process the work item
#   succeedWorkItem(work_item):
#       Mark the work_item as processed
#   failWorkItem(work_item, exc):
#       mark the work_item as failed

# ---------------
# more info on wind vs windGust: https://github-wiki-see.page/m/weewx/weewx/wiki/windgust
# ---------------
import app.tools as t
from app.tools.myTools import FromTimestampToDateTime, AsTimezone, GetFirstDayNextMonthFromTs
from app.classes.repository.posteMeteor import PosteMeteor
from app.models import Load_Type
from app.classes.migrate.bulk_data_loader import BulkDataLoader
from app.tools.dbTools import getMSQLConnection, refreshMV
from datetime import datetime, timedelta
# import cProfile
# import pstats


# --------------------------------------
# our class is called by worker service
#    need some methods...
# --------------------------------------
class MigrateDB:
    def __init__(self):
        self._meteors_to_process = []
        self.stopRequested = False

    # -----------------------------------
    # add an item in the list to execute
    # -----------------------------------
    def addNewWorkItem(self, meteor):
        self._meteors_to_process.append({
            'meteor': meteor,
            'info': "Migration du dump de " + meteor,
            'bd': meteor,
            'spanID': 'Start ' + meteor + ' migration'
        })
        return meteor

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
    def succeedWorkItem(self, work_item):
        refreshMV()
        return

    # ---------------
    # process failed
    # ---------------
    def failWorkItem(self, work_item, exc):
        return

    # -----------------
    # process our item
    # -----------------
    def processWorkItem(self, work_item):
        try:
            # profiler = cProfile.Profile()
            # profiler.enable()

            current_ts = datetime.now().timestamp() + 1
            my_cur = None
            meteor = work_item['meteor']
            cur_poste = PosteMeteor(meteor)
            if cur_poste.data.id is None:
                raise Exception('station ' + meteor + ' not found')

            if (cur_poste.data.load_type & Load_Type.LOAD_FROM_DUMP.value) == 0:
                t.logInfo(meteor, {'status': 'Migration stopped, station load_dump is False'})
                return

            work_item['pid'] = cur_poste.data.id
            work_item['tz'] = cur_poste.data.delta_timezone

            self.getNewDateBracket(cur_poste, work_item)

            # get a cursor to our archive db
            myconn = getMSQLConnection(work_item['meteor'])
            my_cur = myconn.cursor()

            self._bulk_dl = BulkDataLoader()

            # loop per year
            while work_item['archive_first_ts'] < current_ts:
                start_dt = datetime.now()

                # load records data from weewx
                minmax = self.loadMinMaxFromWeeWX( work_item)

                # create an iterator to get the data
                query_my = self.getWeewxSelectSql(work_item)
                my_cur.execute(query_my)

                self._bulk_dl.bulkLoad(cur_poste, my_cur, minmax)

                print("     Done in : " + str(datetime.now() - start_dt) + " for " + str(work_item['start_dt_archive_utc']))
                self.getNewDateBracket(cur_poste, work_item)

        finally:
            if my_cur is not None:
                my_cur.close()

            self._bulk_dl = None

            # profiler.disable()
            # stats = pstats.Stats(profiler)
            # stats.sort_stats(pstats.SortKey.TIME)
            # stats.print_stats()

    # ---------------------------------------
    # other methods specific to this service
    # ---------------------------------------
    def getNewDateBracket(self, cur_poste, work_item):

        """Get start_dt/end_dt from postes, and archive table"""
        myconn = getMSQLConnection(work_item['meteor'])
        my_cur = myconn.cursor()

        work_item['old_load_raw_data'] = False

        # 1/1/2100 00:00 UTC
        max_date = AsTimezone(datetime(2100, 1, 1, 4), 0)
        max_ts = int(max_date.timestamp())

        try:
            print('-------------------------------------------------')
            print('Meteor: ' + work_item['meteor'])

            # Get scan limit
            if work_item.get('global_first_ts') is None:
                my_cur.execute('select min(dateTime), max(dateTime) from archive')
                row = my_cur.fetchone()
                my_cur.close()
                if row is None or len(row) == 0 or row[0] is None or row[1] is None:
                    work_item['archive_first_ts'] = max_ts
                    return
                ts_poste_obs_date_utc = int(cur_poste.data.last_obs_date_local.timestamp() - work_item['tz'] * 3600) if cur_poste.data.last_obs_date_local is not None else 0
                work_item['global_first_ts'] = max(row[0], ts_poste_obs_date_utc)
                work_item['global_last_ts'] = row[1] + 1
                if cur_poste.data.stop_date is not None:
                    # cur_poste.data.stop_date is in local time
                    stop_ts_utc = (cur_poste.data.stop_date.timestamp() + 1)  - work_item['tz'] * 3600
                    # stop to scan at stop_date if exists
                    work_item['global_last_ts'] = min(work_item['global_last_ts'], stop_ts_utc)
                print('Global (ts utc)     from: ' + str(work_item['global_first_ts']) + ' to ' + str(work_item['global_last_ts']))
                print('Global (-> dt utc)  from: ' + str(FromTimestampToDateTime(work_item['global_first_ts'])) + ' to ' + str(FromTimestampToDateTime(work_item['global_last_ts'])))

            # Get start_dt/archive_first_ts
            if work_item.get('archive_last_ts') is None:
                # First pass
                work_item['archive_first_ts'] = work_item['global_first_ts']
            else:
                work_item['archive_first_ts'] = work_item['archive_last_ts'] + 1

            # if archive_first_ts greater than global_last_ts -> exit
            if work_item['archive_first_ts'] > work_item['global_last_ts']:
                work_item['archive_first_ts'] = max_ts
                return
            
            # tz is needed to get the first day of next month in local time
            work_item['archive_last_ts'] = int(GetFirstDayNextMonthFromTs(work_item['archive_first_ts'], work_item['tz']).timestamp())

            work_item['minmax_first_ts'] = (FromTimestampToDateTime(work_item['archive_first_ts']) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            work_item['minmax_last_ts'] = (FromTimestampToDateTime(work_item['archive_last_ts']) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            
            t.myTools.logInfo(
                'ts_archive (ts utc)    from: ' + str(work_item['archive_first_ts']) + ' to ' + str(work_item['archive_last_ts']),
                {"svc": "migrate", "meteor":  work_item['meteor']})

            work_item['start_dt_archive_utc'] = FromTimestampToDateTime(work_item['archive_first_ts'])
            print('Archive (ts utc)    from: ' + str(work_item['archive_first_ts']) + ' to ' + str(work_item['archive_last_ts']))
            print('Archive (=> dt utc) from: ' + str(FromTimestampToDateTime(work_item['archive_first_ts'])) + ' to ' + str(FromTimestampToDateTime(work_item['archive_last_ts'])))
            print('MinMax (ts utc)     from: ' + str(work_item['minmax_first_ts']) + ' to ' + str(work_item['minmax_last_ts']))
            print('MinMax (=> dt utc)  from: ' + str(FromTimestampToDateTime(work_item['minmax_first_ts'])) + ' to ' + str(FromTimestampToDateTime(work_item['minmax_last_ts'])))
            print('-------------------------------------------------')

            return

        except Exception as ex:
            print("exception: " + str(ex))
            raise ex

        finally:
            myconn.close()
# ------------------------------------
    # generate max/min from WeeWX records
    # ------------------------------------
    def loadMinMaxFromWeeWX(self, work_item):
        min_max = []
        myconn = getMSQLConnection(work_item['meteor'])
        my_cur = None
        try:
            pass
            # for a_mesure in self.measures:
            #     # debug
            #     # if a_mesure['id'] in (74,):
            #     #     pass
            #     # else:
            #     #     continue
            #     if a_mesure.get('table') == 'skip':
            #         continue
            #     nb_record_processed = 0
            #     mid = a_mesure['id']
            #     my_cur = myconn.cursor()
                # try:
            #         # get cached_mesure
            #         if new_records.get('m_' + str(mid)) is None:
            #             new_records['m_' + str(mid)] = {'mid': mid, 'cache': []}

            #         mesure_cache_item = new_records['m_' + str(mid)]

            #         # get table name, fix for wind table
            #         table_name = a_mesure['col']
            #         if a_mesure['table'] is not None:
            #             table_name = a_mesure['table']

            #         # We need to use mintime/maxtime as the date of the record
            #         # the mintime and maxtime can be on two different days...
            #         if a_mesure['iswind'] is False:
            #             my_query = \
            #                 'select min, mintime, max, maxtime, null as max_dir, ' + str(mid) + ' as mid, dateTime ' + \
            #                 ' from archive_day_' + table_name +\
            #                 " where dateTime >= " + str(work_item['minmax_first_ts']) +\
            #                 " and dateTime < " + str(work_item['minmax_last_ts']) +\
            #                 " order by dateTime"
            #         else:
            #             my_query = \
            #                 'select min, mintime, max, maxtime, max_dir, ' + str(mid) + ' as mid, dateTime ' + \
            #                 ' from archive_day_' + table_name +\
            #                 " where dateTime >= " + str(work_item['minmax_first_ts']) +\
            #                 " and dateTime < " + str(work_item['minmax_last_ts']) +\
            #                 " order by dateTime"

            #         my_cur.execute(my_query)
            #         row = my_cur.fetchone()
            #         while row is not None:
            #             if row[self.row_extreme_max] is not None or row[self.row_extreme_min] is not None:
            #                 nb_record_processed += 1
            #                 self.loadMinMaxFromExtremeRow(work_item, a_mesure, row, mesure_cache_item)

            #             if a_mesure['iswind'] is True:
            #                 min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
            #                                      'date_max': date_max, 'max_dir': max_dir, 'mid': a_mesure['id'], 'obs_id': -1})
            #             else:
            #                 min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
            #                                      'date_max': date_max, 'mid': a_mesure['id'], 'obs_id': -1})
                            
            #             row = my_cur.fetchone()
                # finally:
                #     my_cur.close()
                    # if nb_record_processed > 0:
                    #     process_length = datetime.now() - start_time
                    #     t.myTools.logInfo(
                    #         'weewx.archive_day_' + str(table_name) + " new records: " + str(nb_record_processed) + ' en ' + str(process_length/1000) + ' ms',
                    #         my_span,
                    #         {"svc": "migrate", "meteor":  work_item['meteor']})

        finally:
            myconn.close()
            return min_max

    # --------------------------------
    # return the sql select statement
    # --------------------------------
    def getWeewxSelectSql(self, work_item):
        query_my = "select dateTime, usUnits, `interval`"

        # load an array of query args
        for a_mesure in self._bulk_dl.getMeasures():
            if a_mesure['field'] == 'rain_utc':
                pass
            if a_mesure['archive_col'] is not None:
                # add field name into our select statement for weewx
                query_my += ', ' + a_mesure['archive_col']

        # finalize sql statements
        query_my += " from archive where dateTime >= " + str(work_item['archive_first_ts'])
        query_my += " and dateTime < " + str(work_item['archive_last_ts'])

        # query_my += " order by dateTime"""
        query_my += " order by dateTime"
        return query_my
