from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object
import datetime


class root_type_instr:

    def process_observation(self, poste_obj: Poste, json_obs: json, obs_dataset: Observation, flag: bool):
        """process observation data into obs_dataset. flag is True for insert, False for delete"""
        # dans le cas de suppression, le obs_dataset va etre supprime, il faut juste ajuster les agg/extremes
        if flag is False:
            return

        # Si existe json_obs['context']
        #   load values si definie dans json

    def process_aggregation(self, poste_obj: Poste, json_obs: json, agg_all_dataset, flag: bool):
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

Cas 1 : Avec les données élémentaires, avec le futur plugin WeeWX
Cas 2 : Agrégés par heure/jour/mois (par jour pour WeeWX sans plug-in). Ce niveau d’agrégation est appelé « agrégation minimale de l’extrême »
Cas 3 : Non fournies, ce qui sera le de nouvelles données corrigeant une observation supprimée
