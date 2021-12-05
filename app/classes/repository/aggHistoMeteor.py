from app.tools.modelTools import getAggHistoTable, isTmpLevel, doesObservationExist, doesAggExist


class AggHistoMeteor():
    """
        AggHistoMeteor

        gere les objets AggHisto metier

        o=AggHistoMeteor(obs_id, agg_id, agg_level)
        o.data -> Aggregation Histo object (data, methods...)

    """

    def __init__(self, obs_id: int, agg_id: int, agg_level: str):
        """
            Init a new AggHisto object

            obs_id: observation/tmpObservation id
            agg_level: 'H','D', 'M', 'Y', 'A', 'HT, 'DT', 'MT', 'YT,' 'AT'
            agg_id: agregation id in appropriate table
        """
        self.is_tmp = isTmpLevel(agg_level)
        agg_histo_object = getAggHistoTable(agg_level)
        if agg_histo_object.objects.filter(obs_id=obs_id).exists():
            self.data = agg_histo_object.objects.filter(obs_id=obs_id).first()
        else:
            # check that observation and agregation exist
            if doesObservationExist(obs_id, self.is_tmp) is False:
                raise Exception("Observation id: " + str(obs_id) + ', is_tmp: ' + str(self.is_tmp) + ' does not exist')
            if doesAggExist(agg_id, agg_level) is False:
                raise Exception("Aggregation id " + str(agg_id) + ", level: " + agg_level + " does not exist")
            # insert our new agg_histo row
            self.data = agg_histo_object(obs_id=obs_id, agg_id=agg_id, agg_level=agg_level, delta_duration=0, j={})

    def save(self):
        """ save Poste and Exclusions """
        self.data.save()

    def countKeys(self) -> int:
        # return count of aggregations
        return self.j.data.j.keys().__len__()

    def __str__(self):
        """print myself"""
        if self.is_tmp is True:
            return "AggHisto obs_id: " + str(self.data.obs_id) + ", agg_id: " + str(self.data.agg_id) + ", level: " + self.data.agg_level
        return "TmpAggHisto obs_id: " + str(self.data.obs_id) + ", agg_id: " + str(self.data.agg_id) + ", level: " + self.data.agg_level
