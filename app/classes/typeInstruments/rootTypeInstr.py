from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object, convert_relative_hour
from app.tools.climConstant import ClimConstants, AggLevelConstant
import datetime
import json


class RootTypeInstrument:
    """ typeInstrument root object"""

    def __init(self):
        self.me = TypeInstrument.objects.get(id=self.my_type_instr_id)

    def process_observation(self, poste_obj: poste_meteor, json_obs: json, obs_dataset: Observation, flag: bool) -> json:
        """
            process_observation
            parameters:
                poste_object -
            data into obs_dataset. flag is True for insert, False for delete"""

        # dans le cas de suppression, le obs_dataset va etre supprime, il faut juste ajuster les agg/extremes
        if flag is False:
            return

        # if not key ClimConstants.JSON_CURRENT, just return
        b_donnee_elementaire = json_obs.__contains__(ClimConstants.JSON_CURRENT) and json_obs[ClimConstants.JSON_CURRENT] != {
        } and json_obs[ClimConstants.JSON_CURRENT] != []
        if b_donnee_elementaire is False:
            return

        # get exclusion
        exclusion = poste_obj.get_exclusion(self.my_type_instr_id)

        for aMap in self.mapping:
            if exclusion == {}:

                # todo filtre en entree et trigger

                # no exclusion, load the value
                if aMap.key in json_obs:
                    obs_dataset.__setattr__[aMap.field] = json_obs[aMap.key]
            else:
                # get the exclusion value if specified, and not the string 'null'
                if exclusion.__contains__ is True and exclusion[aMap.field] != 'null':
                    obs_dataset.__setattr__[aMap.field] = exclusion[aMap.field]

    def process_aggregation(self, poste_obj: Poste, json_obs: json, agg_all_dataset, flag: bool) -> None:
        """process observation data into al aggregation dataset. flag is True for insert, False for delete"""

        b_donnee_elementaire = json_obs.__contains__(ClimConstants.JSON_CURRENT) and json_obs[ClimConstants.JSON_CURRENT] != {
        } and json_obs[ClimConstants.JSON_CURRENT] != []
        b_donnee_aggregee = json_obs.__contains__(ClimConstants.JSON_AGGREGATE) and json_obs[ClimConstants.JSON_AGGREGATE] != {
        } and json_obs[ClimConstants.JSON_AGGREGATE] != []
        if b_donnee_aggregee:
            # get niveau_agg_json
            if json_obs[ClimConstants.JSON_AGGREGATE].__contains__(ClimConstants.JSON_AGGREGATE) is False:
                raise Exception("Instrument_calculator.process_aggregation",
                                "no " + ClimConstants.JSON_AGGREGATE + " key")
            niveau_agg_json = json_obs[ClimConstants.JSON_AGGREGATE]['agregation']
            if niveau_agg_json in AggLevelConstant is False:
                raise Exception("Instrument_calculator.process_aggregation",
                                "invalid value in " + ClimConstants.JSON_AGGREGATE + ": " + niveau_agg_json)
        else:
            # no aggregation data
            niveau_agg_json = "?"

        # si bDonnesElementaires && !bDonneesAggregaton
        #   calcule delta agregation par heure

        # si bDonnesElementaires && !bDonneesAggregaton
        #   calcule delta agregation par heure

        # pour chaque niveau par ordre
        #    for aMap in self.mapping:

        #   si !bDonneesAggregaton && miniNiveauAggregation > niveauCourant
        #       continue
        #   si bDonneesAggregaton && miniNiveauAggregation = niveauCourant
        #       met a jour agg_xxx
        #   else
        #       applique le delta aggregation du niveau -1
        #   garde le delta aggregation
        # applique le delta aggregation au global
        #

        # si hour_deca != 0 -> ajoute "field"_duration_non_gmt dans les tables d'agregation, car la duration de la
        #    field est different de la duration de l'agregation basee sur TU
        # comment limiter le besoin de lire les records next pour agregation jour/mois/an

    def process_extreme(self, poste_obj, json_obs, agg_all_dataset, flag):
        """process observation data into al aggregation dataset. flag is True for insert, False for delete"""

        # bDonnesElementaires si existe donnees elementaires
        # bDonneesAggregaton si existe donnees aggration (hour ou +)
        # miniNiveauAggregation = mini agregation dans json (seulement si bDonneesAggregaton=true)

        # si bDonnesElementaires && !bDonneesAggregaton
        #   calcule delta agregation par heure

        # si bDonnesElementaires && !bDonneesAggregaton
        #   calcule delta agregation par heure

        # pour chaque niveau par ordre
        #   si !bDonneesAggregaton && miniNiveauAggregation > niveauCourant
        #       continue
        #   si bDonneesAggregaton && miniNiveauAggregation = niveauCourant
        #       met a jour agg_xxx
        #   else
        #       applique le delta aggregation du niveau -1
        #   garde le delta aggregation
        # applique le delta aggregation au global
        #

# Cas 1 : Avec les données élémentaires, avec le futur plugin WeeWX
# Cas 2 : Agrégés par heure/jour/mois (par jour pour WeeWX sans plug-in). Ce niveau d’agrégation est appelé « agrégation minimale de l’extrême »
# Cas 3 : Non fournies, ce qui sera le de nouvelles données corrigeant une observation supprimée
