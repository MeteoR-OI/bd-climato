![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.    Format Fichier JSON de test calculus](#2----format-fichier-json-de-test-calculus)
- [3.    Clé name](#3----clé-name)
- [4.    Clé data](#4----clé-data)
- [5.    Clé results](#5----clé-results)
- [5a.](#5a)

<!-- /code_chunk_output -->

**Doc v 0.52**

# 1.	Historique mises à jour
- V0.5 : 26/03/2021. Version initiale

# 2.    Format Fichier JSON de test calculus
Clés name, data, results

# 3.    Clé name
Correspond a la string passée en paramêtre lors de l'appel de la fonction self.t_engine.run_test dans test_calculus.py

# 4.    Clé data
Clause [data] du fichier json

# 5.    Clé results
Contient un tableau des checks du resultat a faire

Il y a deux parties:
# 5a.   
[
    {  "name": "1_simple_agg_hour",
        "data": [
            {"current": {"stop_dat": "2021-02-11T13:10:00", "duration": 5, "out_temp": 20}}
        ],
        "results":[
            {"t": "O", "dat": "2021-02-11T13:10:00", "idx": 0, "out_temp": 20},
            {"t": "O", "dat": "2021-02-11T13:10:00", "idx": 0, "count": 1},
            {"t": "H", "dat": "2021-02-11T14:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "H", "dat": "2021-02-11T14:00:00", "idx": 0, "count": 1},
            {"t": "H", "dat": "2021-02-11T14:00:00", "idx": 0, "count": 1, "dat_mask": "13:00"},
            {"t": "D", "dat": "2021-02-11T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "M", "dat": "2021-02-11T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "Y", "dat": "2021-02-01T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "A", "out_temp_sum": 100, "out_temp_duration": 5}
        ]
    },{  "name": "1_simple_agg_hour_round_hour",
        "data": [
            {"current": {"stop_dat": "2021-02-11T13:00:00", "duration": 5, "out_temp": 20}}
        ],
        "results":[
            {"t": "O", "dat": "2021-02-11T13:00:00", "idx": 0, "out_temp": 20},
            {"t": "O", "dat": "2021-02-11T13:00:00", "idx": 0, "count": 1},
            {"t": "H", "dat": "2021-02-11T13:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "H", "dat": "2021-02-11T13:00:00", "idx": 0, "count": 1},
            {"t": "H", "dat": "2021-02-11T13:00:00", "idx": 0, "count": 1, "dat_mask": "13:00"},
            {"t": "D", "dat": "2021-02-11T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "M", "dat": "2021-02-11T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "Y", "dat": "2021-02-01T00:00:00", "idx": 0, "out_temp_sum": 100, "out_temp_duration": 5},
            {"t": "A", "out_temp_sum": 100, "out_temp_duration": 5}
        ]
    },{ "name": "2_max_min_agg_same_day",
        "data":
        [
            {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
            {"current" : {"stop_dat" : "2021-02-11T13:06:00", "duration" : 5, "out_temp" : 10}},
            {"current" : {"stop_dat" : "2021-02-11T13:35:00", "duration" : 5, "out_temp" : 30}}
        ],
        "results": [
            {"t": "O", "dat": "2021-02-11T13:30:00", "out_temp": 20},
            {"t": "O", "dat": "2021-02-11T13:06:00", "out_temp": 10},
            {"t": "O", "dat": "2021-02-11T13:35:00", "out_temp": 30},
            {"t": "H", "idx": 0, "out_temp_max": 30, "out_temp_max_time": "2021-02-11T13:35:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:06:00"},
            {"t": "A", "out_temp_max": 30, "out_temp_max_time": "2021-02-11T13:35:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:06:00"}
        ]
    },{ "name": "3_max_min_date_agg_different_days",
        "data":
        [
            {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
            {"current" : {"stop_dat" : "2021-02-11T13:35:00", "duration" : 5, "out_temp" : 10}},
            {"current" : {"stop_dat" : "2021-02-12T13:40:00", "duration" : 5, "out_temp" : 30}}
        ],
        "results": [
            {"t": "O", "dat": "2021-02-11T13:30:00", "out_temp": 20},
            {"t": "H", "dat": "2021-02-11T14:00:00", "out_temp_max": 20, "out_temp_max_time": "2021-02-11T13:30:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
            {"t": "H", "dat": "2021-02-12T14:00:00", "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 30, "out_temp_min_time": "2021-02-12T13:40:00"},
            {"t": "D", "dat": "2021-02-11T00:00:00", "out_temp_max": 20, "out_temp_max_time": "2021-02-11T13:30:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
            {"t": "D", "dat": "2021-02-12T00:00:00", "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 30, "out_temp_min_time": "2021-02-12T13:40:00"},
            {"t": "M", "dat": "2021-02-01T00:00:00", "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
            {"t": "Y", "idx": 0, "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
            {"t": "A", "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"}
        ]
        },{ "name": "4_simple_omm_agg",
            "data":
            [
                {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"stop_dat" : "2021-02-11T13:10:00", "duration" : 5, "out_temp" : 10}},
                {"current" : {"stop_dat" : "2021-02-11T13:35:00", "duration" : 5, "out_temp" : 30}}
            ],
            "results": [
                {"t": "O", "dat": "2021-02-11T13:35:00", "idx": 0, "out_temp": 10},
                {"t": "H", "dat": "2021-02-11T13:00:00", "idx": 0, "out_temp_omm_sum": 500, "out_temp_omm_duration": 5},
                {"t": "D", "dat": "2021-02-11T00:00:00", "idx": 0, "out_temp_omm_sum": 500, "out_temp_omm_duration": 5},
                {"t": "M", "dat": "2021-02-01T00:00:00", "idx": 0, "out_temp_omm_sum": 500, "out_temp_omm_duration": 5},
                {"t": "Y", "dat": "2021-01-01T00:00:00", "idx": 0, "out_temp_omm_sum": 500, "out_temp_omm_duration": 5},
                {"t": "A", "out_temp_omm_sum": 500, "out_temp_omm_duration": 5}
            ]
        },{ "name": "5_simple_omm_agg_same_day",
            "data":
            [
                {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"stop_dat" : "2021-02-11T13:10:00", "duration" : 5, "out_temp" : 10}},
                {"current" : {"stop_dat" : "2021-02-11T13:35:00", "duration" : 5, "out_temp" : 30}}
            ],
            "results": [
                {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp": 20},
                {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 1, "out_temp": 10},
                {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 2, "out_temp": 30},
                {"t": "H", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                {"t": "D", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                {"t": "M", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                {"t": "Y", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                {"t": "A", "out_temp_omm": 10}
            ]
            },{ "name": "6_simple_omm_agg_different_days",
                "data":
                [
                    {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
                    {"current" : {"stop_dat" : "2021-02-11T13:10:00", "duration" : 5, "out_temp" : 10}},
                    {"current" : {"stop_dat" : "2021-02-12T13:35:00", "duration" : 5, "out_temp" : 30}}
                ],
                "results": [
                    {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp": 20},
                    {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 1, "out_temp": 10},
                    {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 2, "out_temp": 30},
                    {"t": "H", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                    {"t": "H", "dat": "1900-12-31T00:00:00", "idx": 2, "out_temp_omm": 30},
                    {"t": "D", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                    {"t": "M", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                    {"t": "Y", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_omm": 10},
                    {"t": "A", "out_temp_omm": 10}
                ]
            },{ "name": "7_max_min_omm_agg_different_days",
            "data":
            [
                {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"stop_dat" : "2021-02-12T13:06:00", "duration" : 5, "out_temp" : 10}},
                {"current" : {"stop_dat" : "2021-02-12T13:35:00", "duration" : 5, "out_temp" : 30}}
            ],
            "results": [
                {"t": "O", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp": 20},
                {"t": "H", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_max": 20, "out_temp_max_time": "2021-02-11T13:30:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
                {"t": "H", "dat": "1900-12-31T00:00:00", "idx": 2, "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 30, "out_temp_min_time": "2021-02-12T13:40:00"},
                {"t": "D", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_max": 20, "out_temp_max_time": "2021-02-11T13:30:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
                {"t": "D", "dat": "1900-12-31T00:00:00", "idx": 2, "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 30, "out_temp_min_time": "2021-02-12T13:40:00"},
                {"t": "M", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
                {"t": "Y", "dat": "1900-12-31T00:00:00", "idx": 0, "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"},
                {"t": "A", "out_temp_max": 30, "out_temp_max_time": "2021-02-12T13:40:00",  "out_temp_min": 10, "out_temp_min_time": "2021-02-11T13:35:00"}
                ]
        },{ "name": "8_max_min_omm_agg_regen",
            "data":
            [
                {"current" : {"stop_dat" : "2021-02-11T13:10:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"stop_dat" : "2021-02-12T13:30:00", "duration" : 5, "out_temp" : 10}},
                {"current" : {"stop_dat" : "2021-02-12T13:10:00", "duration" : 5, "out_temp" : 30}}
            ],
            "results": [
            ]
        },{ "name": "9_max_min_simple_replace",
            "data":
            [
                {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 20}},
                {"current" : {"stop_dat" : "2021-02-11T13:30:00", "duration" : 5, "out_temp" : 10}}
            ],
            "results": [
            ]
        }
]
