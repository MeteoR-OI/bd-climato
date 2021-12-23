![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

**Rest API**


- [1. historique-mises-à-jour](#1-historique-mises-à-jour)
- [2. Poste API](#2-poste-api)
- [3. Get Station Data](#3-get-station-data)
- [4. Get all stations data](#4-get-all-stations-data)
- [5. Get detail Observation data](#5-get-detail-observation-data)
- [5.1 Get range observation for a given key prefix](#51-get-range-observation-for-a-given-key-prefix)
- [5.2 Get range observation for all keys](#52-get-range-observation-for-all-keys)
- [5.3 Get all data from last observation](#53-get-all-data-from-last-observation)
- [5.4 Get data from a given key prefix from the last observation](#54-get-data-from-a-given-key-prefix-from-the-last-observation)
- [6. Aggregation data](#6-aggregation-data)
- [6.1 Get Aggregated data for a range and a key prefix](#61-get-aggregated-data-for-a-range-and-a-key-prefix)
- [6.2 Get Aggregated data for a date range for all keys](#62-get-aggregated-data-for-a-date-range-for-all-keys)
- [6.3 Get the n last aggregated data with a key prefix](#63-get-the-n-last-aggregated-data-with-a-key-prefix)
- [6.4 get the last n aggregated data for all keys](#64-get-the-last-n-aggregated-data-for-all-keys)

# 1. historique-mises-à-jour
- 22/12/2021: Version initiale

# 2. Poste API

- Get all stations:
    http://localhost:8000/app/api/stationlist
 return:
 ```json
 [
  {
    "meteor": "BBF015",
    "fuseau": 4,
    "meteofr": "MF",
    "lock_calculus": 0,
    "title": "Bain Boeuf - MRU",
    "owner": "Nicolas",
    "email": "nicolas@cuvillier.net",
    "phone": "+230",
    "address": "CP B1",
    "zip": "33701",
    "city": "BB",
    "country": "MRU",
    "latitude": -20,
    "longitude": -57,
    "start_dat": "2021-02-09T10:42:18",
    "stop_dat": "2021-06-11T10:43:31",
    "comment": "Hello"
  }, ... ]
```
  NB: The fields returned are all the poste fields in the database

# 3. Get Station Data

Return the last agregated data at each level. Only return agregated data with a non null duration

API: http://localhost:8000/app/api/stationdata/MTG320
return:
```json
{
  "station": {
    "id": 2,
    "meteor": "MTG320",
    "fuseau": 4,
    "meteofr": "MF",
    "owner": "Nicolas",
    "phone": "+230",
    "email": "nicolas@cuvillier.net",
    "address": "CP B1",
    "zip": "33701",
    "city": "BB",
    "country": "MRU",
    "latitude": -20,
    "longitude": -57
  },
  "data": {
    "hour": {
      "start_dat": "2021-07-01 07:00:00+04:00",
      "duration_sum": 15,
      "duration_max": 60,
      "data": {
          all hour aggregated data
      },
    },
    "day": {
      "start_dat": "2021-07-01 00:00:00+04:00",
      "duration_sum": 435,
      "duration_max": 1440,
      "data": {
          // all day aggregated data
      }
    },
    "month": {
      "start_dat": "2021-07-01 00:00:00+04:00",
      "duration_sum": 435,
      "duration_max": 44640,
      "data": {
          all month aggregated data
      }
    },
    "year": {
      "start_dat": "2021-01-01 00:00:00+04:00",
      "duration_sum": 47940,
      "duration_max": 525600,
      "data": {
          all year aggregated data
      }
    },
    "all": {
      "start_dat": "1900-01-01 00:00:00+04:00",
      "duration_sum": 47940,
      "duration_max": 52560000,
      "data": {
          all station data agregated
      }
    }
  }
}
```

# 4. Get all stations data

API: http://localhost:8000/app/api/stationdata

return an array of the previous data, for each existing station

# 5. Get detail Observation data

# 5.1 Get range observation for a given key prefix

API: http://localhost:8000/app/obs/2/out_temp/2021-07-01T00:00/2021-07-02T00:00
   get all out_tempXXX data from 1st July 2021 to 2nd July 2021
   If not end date is given, the range is up to the last observation in the database
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "obs": [
    {
      "id": 48866,
      "stop_dat": "2021-07-01 00:00:00+04:00",
      "duration": 5,
      "obs": {
        "out_temp": 19.7976453274,
        "out_temp_max": 19.8888888889,
        "out_temp_min": 19.7222222222,
        "out_temp_omm": 19.7777777778,
        "out_temp_omm_max": 19.8888888889,
        "out_temp_omm_min": 19.7222222222,
        "out_temp_max_time": "2021-06-30T23:55:01",
        "out_temp_min_time": "2021-06-30T23:59:25",
        "out_temp_omm_max_time": "2021-06-30T23:55:01",
        "out_temp_omm_min_time": "2021-06-30T23:59:25"
      },
      "pre_agg": [
        {
          "level": "H",
          "start_dat": "2021-06-30T23:00:00"
        }
      ]
    }, ... obs for other stop_dat
```

# 5.2 Get range observation for all keys

NB: This can be huge...

API: http://localhost:8000/app/obs/2/*/2021-07-01T00:00/2021-07-02T00:00
   get all observation data from 1st July 2021 to 2nd 
   If not end date is given, the range is up to the last observation in the database


Json API for aggregations

parameters:
period: H, D, M, Y, A
start_dt: start date for lookup (included). format: '2021-12-31 00:00:00+04'
end_dt: end date for lookup (included). format: '2021-12-31 00:00:00+04'

return:
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "obs": [
    {
      "id": 48866,
      "stop_dat": "2021-07-01 00:00:00+04:00",
      "duration": 5,
      "obs": {
        "rx": 99.9375,
        "rain": 0,
        "wind": 1.34112333441,
        "rx_max": 99.9375,
        "rx_min": 99.9375,
        "in_temp": 24.6666666667,
        "voltage": 4.59,
        "humidity": 75,
        "out_temp": 19.7976453274,
        "rain_omm": 0,
        "wind_dir": 202.5,
        "wind_max": 2.68224666883,
        "barometer": 1022.14807465,
        "rain_rate": 0,
        "in_humidity": 61,
        "in_temp_max": 24.6666666667,
        "in_temp_min": 24.6666666667,
        "rx_max_time": "2021-07-01T00:00:00",
        "rx_min_time": "2021-07-01T00:00:00",
        "voltage_max": 4.59,
        "voltage_min": 4.59,
        "dewpoint_max": 15.3214190075,
        "dewpoint_min": 15.1606086362,
        "humidity_max": 75,
        "humidity_min": 75,
        "humidity_omm": 75,
        "out_temp_max": 19.8888888889,
        "out_temp_min": 19.7222222222,
        "out_temp_omm": 19.7777777778,
        "pressure_max": 985.71869159,
        "pressure_min": 985.518697111,
        "rain_omm_max": 0,
        "wind_max_dir": 157.5,
        "barometer_max": 1022.2489935,
        "barometer_min": 1022.11353798,
        "barometer_omm": 1022.11353798,
        "heatindex_max": 19.8888888889,
        "rain_rate_max": 0,
        "wind_max_time": "2021-06-30T23:55:43",
        "windchill_min": 19.7222222222,
        "in_humidity_max": 61,
        "in_humidity_min": 61,
        "humidity_omm_max": 75,
        "humidity_omm_min": 75,
        "in_temp_max_time": "2021-06-30T23:55:01",
        "in_temp_min_time": "2021-06-30T23:55:01",
        "out_temp_omm_max": 19.8888888889,
        "out_temp_omm_min": 19.7222222222,
        "voltage_max_time": "2021-07-01T00:00:00",
        "voltage_min_time": "2021-06-30T23:55:01",
        "barometer_omm_max": 1022.2489935,
        "barometer_omm_min": 1022.11353798,
        "dewpoint_max_time": "2021-06-30T23:55:01",
        "dewpoint_min_time": "2021-06-30T23:59:25",
        "humidity_max_time": "2021-06-30T23:55:01",
        "humidity_min_time": "2021-06-30T23:55:01",
        "out_temp_max_time": "2021-06-30T23:55:01",
        "out_temp_min_time": "2021-06-30T23:59:25",
        "pressure_max_time": "2021-06-30T23:55:01",
        "pressure_min_time": "2021-06-30T23:59:25",
        "rain_omm_max_time": "2021-07-01T00:00:00",
        "barometer_max_time": "2021-06-30T23:55:01",
        "barometer_min_time": "2021-06-30T23:56:01",
        "heatindex_max_time": "2021-06-30T23:55:01",
        "rain_rate_max_time": "2021-06-30T23:55:01",
        "windchill_min_time": "2021-06-30T23:59:25",
        "in_humidity_max_time": "2021-06-30T23:55:01",
        "in_humidity_min_time": "2021-06-30T23:55:01",
        "humidity_omm_max_time": "2021-06-30T23:55:01",
        "humidity_omm_min_time": "2021-06-30T23:55:01",
        "out_temp_omm_max_time": "2021-06-30T23:55:01",
        "out_temp_omm_min_time": "2021-06-30T23:59:25",
        "barometer_omm_max_time": "2021-06-30T23:55:01",
        "barometer_omm_min_time": "2021-06-30T23:56:01"
      },
      "pre_agg": [
        {
          "level": "H",
          "start_dat": "2021-06-30T23:00:00"
        }
      ]
    },
    {
      "id": 48867,
      "stop_dat": "2021-07-01 00:05:00+04:00",
      "duration": 5,
      "obs": {
        "rx": 99.0833333333,
        "rain": 0,
        "wind": 1.34112333441,
        "rx_max": 99.0833333333,
        "rx_min": 99.0833333333,
```

# 5.3 Get all data from last observation
API: http://localhost:8000/app/obs/2/*

return:
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "obs": [
    {
      "id": 48953,
      "stop_dat": "2021-07-01 07:15:00+04:00",
      "duration": 5,
      "obs": {
        "rx": 99.9375,
        "rain": 0,
        "wind": 3.57632889177,
        "rx_max": 99.9375,
        "rx_min": 99.9375,
        "in_temp": 23.7777777778,
        "voltage": 4.59,
        "humidity": 87.2450331126,
        "out_temp": 19.3833701251,
        "wind_dir": 112.5,
        "wind_max": 6.70561667207,
        "barometer": 1022.11308945,
        "rain_rate": 0,
        "in_humidity": 63,
        "in_temp_max": 23.7777777778,
        "in_temp_min": 23.7777777778,
        "rx_max_time": "2021-07-01T07:15:00",
        "rx_min_time": "2021-07-01T07:15:00",
        "voltage_max": 4.59,
        "voltage_min": 4.59,
        "dewpoint_max": 17.3470273098,
        "dewpoint_min": 17.111457836,
        "humidity_max": 88,
        "humidity_min": 87,
        "out_temp_max": 19.3888888889,
        "out_temp_min": 19.3333333333,
        "pressure_max": 985.349905202,
        "pressure_min": 985.215234229,
        "wind_max_dir": 112.5,
        "barometer_max": 1022.18126574,
        "barometer_min": 1022.04581021,
        "heatindex_max": 19.3888888889,
        "rain_rate_max": 0,
        "wind_max_time": "2021-07-01T07:10:01",
        "windchill_min": 19.3333333333,
        "in_humidity_max": 63,
        "in_humidity_min": 63,
        "in_temp_max_time": "2021-07-01T07:10:01",
        "in_temp_min_time": "2021-07-01T07:10:01",
        "voltage_max_time": "2021-07-01T07:15:00",
        "voltage_min_time": "2021-07-01T07:10:01",
        "dewpoint_max_time": "2021-07-01T07:13:47",
        "dewpoint_min_time": "2021-07-01T07:11:57",
        "humidity_max_time": "2021-07-01T07:13:47",
        "humidity_min_time": "2021-07-01T07:10:01",
        "out_temp_max_time": "2021-07-01T07:10:01",
        "out_temp_min_time": "2021-07-01T07:11:57",
        "pressure_max_time": "2021-07-01T07:13:59",
        "pressure_min_time": "2021-07-01T07:11:59",
        "barometer_max_time": "2021-07-01T07:13:59",
        "barometer_min_time": "2021-07-01T07:11:59",
        "heatindex_max_time": "2021-07-01T07:10:01",
        "rain_rate_max_time": "2021-07-01T07:10:01",
        "windchill_min_time": "2021-07-01T07:11:57",
        "in_humidity_max_time": "2021-07-01T07:10:01",
        "in_humidity_min_time": "2021-07-01T07:10:01"
      },
      "pre_agg": []
    }
  ]
}
```

# 5.4 Get data from a given key prefix from the last observation

API:http://localhost:8000/app/obs/2/out_temp
return
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "obs": [
    {
      "id": 48953,
      "stop_dat": "2021-07-01 07:15:00+04:00",
      "duration": 5,
      "obs": {
        "out_temp": 19.3833701251,
        "out_temp_max": 19.3888888889,
        "out_temp_min": 19.3333333333,
        "out_temp_max_time": "2021-07-01T07:10:01",
        "out_temp_min_time": "2021-07-01T07:11:57"
      },
      "pre_agg": []
    }
  ]
}
```

# 6. Aggregation data

General format are:
```code
<srv_name:port>/app/<period>/<poste_id>/<key_prefix>/<start_dt>/<end_dt>
where
    <srv_name:port>: server name + port
    <period>: H, D, M, Y or A
    <poste_id>: station Id
    <key_prefix>: key_prefix, or * for all
    <start_dt>: start Date (yyyy-mm-ddThh:mn:ss)
    <end_dt>: end date (if not specified up to now)
```

```code
<srv_name:port>/app/<period>/<key_prefix>/last/<nb_items>
where
    <srv_name:port>: server name + port
    <period>: H, D, M, Y or A
    <poste_id>: station Id
    <key_prefix>: key_prefix, or * for all
    <nb_items>: returns the <nb_items> last non null aggregated record(s)
```


# 6.1 Get Aggregated data for a range and a key prefix
API: http://localhost:8000/app/agg/H/2/out_temp/2021-07-01T00:00/2021-07-02T00:00

If the end date is not given, the range is up to the last aggregated data. Note that aggregated data with a null duration, are generated for post observation datetime omm data.

return:
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "level": "H",
  "aggregations": [
    {
      "id": 1879,
      "start_dat": "2021-07-01T00:00:00",
      "duration_sum": 60,
      "duration %": 100,
      "keys": {
        "out_temp_s": 1171.4563164024999,
        "out_temp_avg": 19.524271940041665,
        "out_temp_max": 19.7777777778,
        "out_temp_min": 19.3888888889,
        "out_temp_omm_s": 1166.6666666639999,
        "out_temp_omm_avg": 19.4444444444,
        "out_temp_omm_max": 19.7777777778,
        "out_temp_omm_min": 21.0555555556,
        "out_temp_duration": 60,
        "out_temp_max_time": "2021-07-01T00:00:03",
        "out_temp_min_time": "2021-07-01T00:32:52",
        "out_temp_omm_duration": 60,
        "out_temp_omm_max_time": "2021-07-01T05:59:51",
        "out_temp_omm_min_time": "2021-06-30T17:59:38"
      }
    },
    {
      "id": 1880,
       ... for all aggregated data
    },
    {
      "id": 1892,
      "start_dat": "2021-07-01T13:00:00",
      "duration_sum": 0,
      "duration %": 0,
      "keys": {
        "out_temp_omm_min": 19.4444444444,
        "out_temp_omm_min_time": "2021-07-01T06:58:57"
      }
    }
  ]
}
```

# 6.2 Get Aggregated data for a date range for all keys
API: http://localhost:8000/app/agg/H/2/*/2021-07-01T00:00/2021-07-02T00:00

If the end date is not given, the range is up to the last aggregated data. Note that aggregated data with a null duration, are generated for post observation datetime omm data.

return the same as previous request, with all aggregated data

# 6.3 Get the n last aggregated data with a key prefix

API: http://localhost:8000/app/agg/H/2/out_temp/last/2
return:
```json
{
  "poste_id": 2,
  "meteor": "MTG320",
  "level": "H",
  "aggregations": [
    {
      "id": 1885,
      "start_dat": "2021-07-01T06:00:00",
      "duration_sum": 60,
      "duration %": 100,
      "keys": {
        "out_temp_s": 1186.5268579830001,
        "out_temp_avg": 19.775447633050003,
        "out_temp_max": 20,
        "out_temp_min": 19.4444444444,
        "out_temp_omm_s": 1166.6666666639999,
        "out_temp_omm_avg": 19.4444444444,
        "out_temp_omm_min": 19.7222222222,
        "out_temp_duration": 60,
        "out_temp_max_time": "2021-07-01T06:08:03",
        "out_temp_min_time": "2021-07-01T06:58:57",
        "out_temp_omm_duration": 60,
        "out_temp_omm_min_time": "2021-06-30T23:59:25"
      }
    },
    {
      "id": 1886,
      "start_dat": "2021-07-01T07:00:00",
      "duration_sum": 15,
      "duration %": 25,
      "keys": {
        "out_temp_s": 290.92899190549997,
        "out_temp_avg": 19.39526612703333,
        "out_temp_max": 19.4444444444,
        "out_temp_min": 19.3333333333,
        "out_temp_omm_min": 19.4444444444,
        "out_temp_duration": 15,
        "out_temp_max_time": "2021-07-01T07:00:01",
        "out_temp_min_time": "2021-07-01T07:08:11",
        "out_temp_omm_min_time": "2021-07-01T00:56:48"
      }
    }
  ]
}
```

# 6.4 get the last n aggregated data for all keys
Same as #6.3, but use * as key_prefix
