import mysql.connector
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings

def getPGConnexion():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Funiculi",
        database=settings.PG_DATABASE
    )

def getMSQLConnection(meteor):
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

def refreshMV():
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
