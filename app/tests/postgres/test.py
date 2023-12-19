import psycopg2


def main():
    pgconn = getPGConnexion()
    pg_cur = pgconn.cursor()
    pg_cur.execute("insert into obs(poste_id, date_utc, date_local, mesure_id, duration, value) values(1, '2021-01-01 00:00:00', '2021-01-01 01:00:00', 1, 60, 1021.0), (1, '2021-01-01 00:00:00', '2021-01-01 01:00:00', 4, 60, 1024.0) returning id;")
    all_ids = pg_cur.fetchall()
    for an in all_ids:
        print(str(an[0]))

    print(str(all_ids))

    pg_cur.execute("select id, meteor from postes")
    row = pg_cur.fetchone()
    while row is not None:
        print(row)
        row = pg_cur.fetchone()
    print("2nd pass")
    while row is not None:
        print(row)
        row = pg_cur.fetchone()
    pg_cur.close()
    pgconn.close()


def getPGConnexion():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Funiculi",
        database="climato"
    )


if __name__ == "__main__":
    main()
    