from app.classes.calcul.avgCompute import avgCompute


class ProcessAll():
    """
        ProcessAll

        Manage all compute objects

    """
    process_type = [
        {"agg": "avg", "object": avgCompute()}
    ]

    def get(self, agg: str):
        """ get a type_process instance """
        for aprocess in self.process_type:
            if aprocess['agg'] == agg:
                return aprocess['object']
        raise Exception("ProcessAll.get", "agg with no compute module: " + agg)
