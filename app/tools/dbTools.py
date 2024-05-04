import mysql.connector
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings
import app.tools.myTools as t
from django.conf import settings

def getPGConnexion():
    try:
        return psycopg2.connect(
            host=settings.PG_ADDON_HOST,
            user=settings.PG_ADDON_USER,
            password=settings.PG_ADDON_PASSWORD,
            port=settings.PG_ADDON_PORT,
            database=settings.PG_DATABASE
        )
    except Exception as e:
        t.logException("Error durinf postgres connection: %s" % e)
        raise e

def getMSQLConnection(meteor):
    try:
        db_name = settings.MS_SQL_DB if settings.MS_SQL_DB != '??' else meteor
        myconn = mysql.connector.connect(
            host=settings.MS_SQL_HOST,
            user=settings.MS_SQL_USER,
            password=settings.MS_SQL_PASS,
            port=settings.MS_SQL_PORT,
            database=settings.MS_SQL_DB
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
    except Exception as e:
         t.logException("Error durinf mySql connection: %s" % e)
         raise e

def refreshMV():
    try:
        # refresh our materialized view
        pgconn = getPGConnexion()
        pgconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pg_cur = pgconn.cursor()

        # if materialized view exist, refresh all of them
        pg_cur.execute("SELECT count(*) FROM pg_views where schemaname = 'public' and viewname ='obs_hour'")
        if pg_cur.fetchone()[0] == 1:
            pg_cur.close()
            pg_cur = pgconn.cursor()
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('obs_hour')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('obs_day')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('obs_month')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('x_min_day')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('x_min_month')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('x_max_day')))
            pg_cur.execute(psycopg2.sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(psycopg2.sql.Identifier('x_max_month')))

        pg_cur.close()
        pgconn.commit()
        pgconn.close()

    except Exception as e:
         t.logException("Error during refreshMV: %s" % e)
         raise e
