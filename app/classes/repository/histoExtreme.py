# from app.models import HistoObs


class HistoExtreme():
    """
        HistoExtreme

        obj.data -> datarow
    """

    def __init__(self, id: int):
        pass

    @staticmethod
    def store(pgconn, an_item):
        pg_cur = pgconn.cursor()
        sql_str = "insert into histo_extreme (src_obs_id, target_x_id) values "
        sql_str += '(' + str(an_item[0]) + ', ' + str(an_item[1]) + ')'
        pg_cur.execute(sql_str)

    @staticmethod
    def storeArray(pgconn, data):
        if len(data) == 0:
            return
        pg_cur = pgconn.cursor()
        sql_str = "insert into histo_extreme (src_obs_id, target_x_id) values "
        data.sort(key=lambda x: (x[0], x[1]))
        d0 = d1 = -1
        for an_item in data:
            if an_item[1] <= 0 or an_item[0] <= 0 or (d0 == an_item[0] and d1 == an_item[1]):
                continue
            sql_str += '(' + str(an_item[0]) + ', ' + str(an_item[1]) + '), '
            d0 = an_item[0]
            d1 = an_item[1]
        pg_cur.execute(sql_str[0:-2])

    def __str__(self):
        """print myself"""
        ret = "HistoExtreme"
        return ret
