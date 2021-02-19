from app.tools.jsonPlus import jsonPlus
import pytest

# On définit un json string qui sera disponible dans tous les tests
# on aura juste à passer json_string en argument d'une fonction de test


@pytest.fixture()
def json_string():
    json = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {
                    "current":
                        {
                            "dat" : "2021-02-11T13:09:30+00:00",
                            "duration" : 300,
                            "out_temp" : 29.5
                        },
                    "aggregations": [
                        {
                            "level" : "H",
                            "out_temp_avg" : 32.75
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                },
                {
                    "current" :
                        {
                            "dat" : "2021-02-11T13:09:40+00:00",
                            "duration" : 300,
                            "out_temp" : 30
                        },
                    "aggregations" : [
                        {
                            "level" : "H",
                            "out_temp_avg" : 33
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                }
            ]
        }"""

    return json

# On définit une nouvelle fixture qui utilisera la méthode loads de jsonPlus


@pytest.fixture()
def jp_loads(json_string):
    jp = jsonPlus()
    return jp.loads(json_string)

# On définit une nouvelle fixture qui tentera de reconvertir jp_loads en string


@pytest.fixture()
def jp_dumps(jp_loads):
    jp = jsonPlus()
    return jp.dumps(jp_loads)


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


@pytest.fixture()
def list_of_tuple_jploads(jp_loads):
    '''
    Retourne une liste de couple (data,value) chargée à partir de jp_loads
    L'avantage est qu'on aura pas à parser récursivement le json pour chaque test
    '''
    keys, values = decomp_json(jp_loads)

    return list(zip(keys, values))
