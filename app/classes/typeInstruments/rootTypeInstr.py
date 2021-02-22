from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.processMeasure import ProcessMeasure
from app.classes.metier.processAll import ProcessAll
import json


class RootTypeInstrument:
    """ typeInstrument root object"""

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data
        self.processJson = ProcessMeasure()

    def mapping(self):
        """return current mapping"""
        return self.mapping

<<<<<<< Updated upstream
    def processJson(self, poste_meteor: PosteMetier, measures: json, measure_idx: int, obs_meteor: ObsMeteor, agg_Array: json, flag: bool) -> json:
        """
            process_json
        """
        try:
            for amesure in self.mesures:
                process_obj = ProcessAll().get(amesure['agg'])
                # begin ttx
                process_obj.updateObsAndGetDelta(
                    poste_meteor,
                    amesure,
                    measures,
                    measure_idx,
                    obs_meteor,
                    flag)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
=======
    def process_observation(self, poste_meteor: PosteMeteor, json_obs: json, obs_dataset: ObsMeteor, flag: bool) -> json:
        """
            process_observation
            parameters:
                poste_meteor: PosteMeteor
                json_obs: json of the new mesure to process
            data into obs_dataset. flag is True for insert, False for delete

        """

    def process_aggregation(self, poste_meteor: PosteMeteor, json_obs: json, agg_all_dataset, extreme_recalc: json, flag: bool) -> json:
        """
            process_aggregation, aggregate measur data

            poste_meteor
            json_obs. is {} when flag is False
            agg_all_dataset: List[0...6] of aggregations
            extreme_recalc: json for a later computation of min/max needed (only when flag is False)
            flag: True for insert, False for delete
        """

        # is there any new measure
        b_donnee_elementaire = json_obs.__contains__(ClimConstants.JSON_CURRENT) and json_obs[ClimConstants.JSON_CURRENT] != {
        } and json_obs[ClimConstants.JSON_CURRENT] != []

        # is there anty aggregated data
        b_donnee_aggregee = json_obs.__contains__(ClimConstants.JSON_AGGREGATE) and json_obs[ClimConstants.JSON_AGGREGATE] != {
        } and json_obs[ClimConstants.JSON_AGGREGATE] != []

        # delta value to aggregate into upper levels
        delta_agg = {}

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

    def process_extreme(self, poste_meteor, json_obs, agg_all_dataset, flag):
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
>>>>>>> Stashed changes
