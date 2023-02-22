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

    def __str__(self):
        """print myself"""
        ret = "HistoExtreme"
        return ret
