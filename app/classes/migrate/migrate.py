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
from app.classes.data_loader.dl_weewx import DlWeewx
import mysql.connector
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime


# --------------------------------------
# our class is called by worker service
#    need some methods...
# --------------------------------------
class MigrateDB:
    def __init__(self):
        self._meteors_to_process = []
        self._bulk_dl = DlWeewx()
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
        # refresh our materialized view
        pgconn = self.getPGConnexion()
        pgconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pg_cur = pgconn.cursor()

        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_hour')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_month')))

        pg_cur.close()
        pgconn.commit()
        pgconn.close()
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
            current_ts = datetime.now().timestamp() + 1
            my_cur = None
            meteor = work_item['meteor']
            cur_poste = PosteMeteor(meteor)
            if cur_poste.data.id is None:
                raise Exception('station ' + meteor + ' not found')

            if (cur_poste.data.load_type & PosteMeteor.Load_Type.LOAD_FROM_DUMP.value) == 0:
                t.logInfo(meteor, {'status': 'Migration stopped, station load_dump is False'})
                return

            work_item['pid'] = cur_poste.data.id
            work_item['tz'] = cur_poste.data.delta_timezone
            work_item['stop_date_utc'] = cur_poste.data.stop_date if cur_poste.data.stop_date is None else AsTimezone(cur_poste.data.stop_date, 0)

            self.getNewDateBracket(cur_poste, work_item)

            # loop per year
            while work_item['start_ts_archive_utc'] < current_ts:

                start_dt = datetime.now()

                # Load obs, records from archive
                query_my = self.getWeewxSelectSql(work_item)

                # get a cursor to our archive db
                myconn = self.getMSQLConnection(work_item['meteor'])
                my_cur = myconn.cursor()
                query_my = self.getWeewxSelectSql(work_item)

                # execute the select statement
                my_cur.execute(query_my)

                self._bulk_dl.bulkLoad(cur_poste, my_cur, False)

                my_cur.close()
                my_cur = None

                print("     Done in : " + str(datetime.now() - start_dt) + " for " + str(work_item['start_dt_archive_utc']))
                self.getNewDateBracket(cur_poste, work_item)

        finally:
            if my_cur is not None:
                my_cur.close()

    # ---------------------------------------
    # other methods specific to this service
    # ---------------------------------------
    def getNewDateBracket(self, cur_poste, work_item):

        """Get start_dt/end_dt from postes, and archive table"""
        myconn = self.getMSQLConnection(work_item['meteor'])
        my_cur = myconn.cursor()

        work_item['old_load_raw_data'] = False

        # 1/1/2100 00:00 UTC
        max_date = AsTimezone(datetime(2100, 1, 1, 4), 0)
        max_ts = int(max_date.timestamp())

        try:
            # Get scan limit
            if work_item.get('start_ts_utc_limit') is None:
                my_cur.execute('select min(dateTime), max(dateTime) from archive')
                row = my_cur.fetchone()
                my_cur.close()
                if row is None or len(row) == 0 or row[0] is None or row[1] is None:
                    work_item['start_ts_archive_utc'] = max_ts
                    return
                ts_poste_obs_date_utc = int(cur_poste.data.last_obs_date.timestamp() - work_item['tz'] * 3600) if cur_poste.data.last_obs_date is not None else 0
                work_item['start_ts_utc_limit'] = max(row[0], ts_poste_obs_date_utc)
                work_item['end_ts_utc_limit'] = row[1] + 1
                if cur_poste.data.stop_date is not None:
                    # cur_poste.data.stop_date is in local time
                    work_item['end_ts_utc_limit'] = min(work_item['end_ts_utc_limit'], (ts_poste_obs_date_utc + 1) if ts_poste_obs_date_utc > 0 else max_ts)

            # Get start_dt/start_ts_archive_utc
            if work_item.get('end_ts_archive_utc') is None:
                # First pass
                # now we only use last_obs_date for both obs and x_min/max
                if cur_poste.data.last_obs_date is None:
                    work_item['start_ts_archive_utc'] = work_item['start_ts_utc_limit']
                else:
                    # cur_poste.data.last_obs_date is in local time
                    work_item['start_ts_archive_utc'] = int(cur_poste.data.last_obs_date.timestamp() - work_item['tz'] * 3600) + 1
            else:
                work_item['start_ts_archive_utc'] = work_item['end_ts_archive_utc'] + 1

            # if start_ts_archive_utc greater than end_ts_utc_limit -> exit
            if work_item['start_ts_archive_utc'] > work_item['end_ts_utc_limit']:
                work_item['start_ts_archive_utc'] = max_ts
                return

            # tz is needed to get the first day of next month in local time
            work_item['end_ts_archive_utc'] = int(GetFirstDayNextMonthFromTs(work_item['start_ts_archive_utc'], work_item['tz']).timestamp())

            t.myTools.logInfo(
                'ts_archive (ts utc)    from: ' + str(work_item['start_ts_archive_utc']) + ' to ' + str(work_item['end_ts_archive_utc']),
                {"svc": "migrate", "meteor":  work_item['meteor']})

            print('-------------------------------------------------')
            print('Meteor: ' + work_item['meteor'])
            work_item['start_dt_archive_utc'] = FromTimestampToDateTime(work_item['start_ts_archive_utc'])
            print('Archive (dt utc)       from: ' + str(work_item['start_dt_archive_utc']) + ' to ' + str(FromTimestampToDateTime(work_item['end_ts_archive_utc'])))
            print('ts_archive (ts utc)    from: ' + str(work_item['start_ts_archive_utc']) + ' to ' + str(work_item['end_ts_archive_utc']))
            print('-------------------------------------------------')

            return

        except Exception as ex:
            print("exception: " + str(ex))
            raise ex

        finally:
            myconn.close()

    # --------------------------------
    # return the sql select statement
    # --------------------------------
    def getWeewxSelectSql(self, work_item):
        query_my = "select dateTime, usUnits, `interval`"

        # load an array of query args
        for a_mesure in self._bulk_dl.getMeasures():
            # add field name into our select statement for weewx
            query_my += ', ' + a_mesure['archive_col']

        # finalize sql statements
        query_my += " from archive where dateTime >= " + str(work_item['start_ts_archive_utc'])
        query_my += " and dateTime < " + str(work_item['end_ts_archive_utc'])

        # query_my += " order by dateTime"""
        query_my += " order by dateTime"
        return query_my

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
