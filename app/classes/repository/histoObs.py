# from app.models import HistoObs


class HistoObsMeteor():
    """
        HistoObsMeteor

        obj.data -> datarow
    """

    def __init__(self, id: int):
        pass

    @staticmethod
    def store(pgconn, an_item):
        if an_item[0] <= 0:
            return
        pg_cur = pgconn.cursor()
        sql_str = "insert into histo_obs (src_obs_id, target_obs_id) values "
        sql_str += '(' + str(an_item[0]) + ', ' + str(an_item[1]) + ')'
        pg_cur.execute(sql_str)

    def __str__(self):
        """print myself"""
        ret = "HistoObsMeteor"
        return ret
