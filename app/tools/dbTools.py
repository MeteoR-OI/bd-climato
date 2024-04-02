import mysql.connector
import psycopg2
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
