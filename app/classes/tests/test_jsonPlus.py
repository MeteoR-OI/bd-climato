from app.tools.JsonPlus import JsonPlus
import pytest
import datetime
import json


def test_date_is_datetime(jp_loads):
    '''
    Test qui vérifiera que les clefs censées être des datetime le sont réellement.
    '''
    errors = []
    list_of_tuple_jploads = list_of_tuple_loads(jp_loads)
    # Liste des clefs censées contenir des dates (si elle est souvent utilisée, on pourra l'ajouter en fixture)
    list_of_dates = ['dat', 'last_dat_rec', 'max_out_temp_time']

    for tuples in list_of_tuple_jploads:
        data, val = tuples[0], tuples[1]
        if data in list_of_dates and not isinstance(val, datetime.datetime):
            errors += [data]

    assert len(errors) == 0


def test_date_is_string(jp_dumps):
    '''
    Test qui vérifiera que les clefs définis dans list_of_dates ne sont pas de type autre que str.
    '''

    errors = []
    list_of_dates = ['dat', 'last_dat_rec', 'max_out_temp_time']
    # On dump grâce au module json (et pas JsonPlus)
    json_dump = json.loads(jp_dumps)
    list_of_tuple_json = list_of_tuple_loads(json_dump)

    for tuples in list_of_tuple_json:
        data, val = tuples[0], tuples[1]
        if data in list_of_dates and not isinstance(val, str):
            errors += [data]

    assert len(errors) == 0


def test_compare_dump_load(jp_loads, jp_dumps):
    '''
    On va tester si on a pas de perte d'infos en passant d'un json --> str --> json
    '''
    # On load le str en json grâce à JsonPlus
    json_loadJsonPlus = jp_loads
    decomp_JsonPlus = list_of_tuple_loads(json_loadJsonPlus)

    # On dump le json en str grâce à JsonPlus
    json_dumpJsonPlus = jp_dumps
    json_loadJson = JsonPlus().loads(json_dumpJsonPlus)
    decomp_json = list_of_tuple_loads(json_loadJson)

    # On regarde l'unicité
    #uniq = set(decomp_JsonPlus+decomp_json)

    # La longueur des 2 doit être la même
    assert len(decomp_JsonPlus) == len(decomp_json)


# -----------------------------------------------------Quelques utilitaires qu'on pourrait aussi tester----------------------------------

def decomp_json(json):
    """Fonction récursive qui décompose le json en 2 listes : une de toutes les clefs et une autre de toutes les valeurs
    data et value seront dans le même ordre"""
    keys, values = [], []

    for k, v in json.items():
        if isinstance(v, dict):
            iter_key, iter_val = decomp_json(v)
            keys += iter_key
            values += iter_val
        elif isinstance(v, list):
            for v_decomp in v:
                iter_key, iter_val = decomp_json(v_decomp)
                keys += iter_key
                values += iter_val
        else:
            keys += [k]
            values += [v]

    return keys, values


def list_of_tuple_loads(json):
    '''
    Retourne une liste de couple (data,value) chargée à partir de jp_loads
    L'avantage est qu'on aura pas à parser récursivement le json pour chaque test
    '''
    keys, values = decomp_json(json)

    return list(zip(keys, values))
