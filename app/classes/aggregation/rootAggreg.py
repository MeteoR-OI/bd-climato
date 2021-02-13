

class RootAggreg:

    # {'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def run(self, json_obs: json, measure_def: json, agg_ds: list[models.Model], level: flag: bool):
        if measure_def.max:

