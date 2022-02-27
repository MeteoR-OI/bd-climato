from app.tools.aggTools import getAggDuration
import datetime
import dateutil
import json


def checkJson(j_arr: json, pid: int = -1, filename: str = "???") -> str:
    """
    checkJson
        Check Json integrity

    Parameter:
        Json data
    """
    ret = None
    stop_dat_list = []
    idx = 0
    meteor = j_arr[idx]["meteor"]

    while idx < j_arr.__len__() and ret is None:
        j = j_arr[idx]

        ret = _checkJsonOneItem(j, pid, meteor, stop_dat_list)

        if ret is not None:
            return "file: " + filename + ", item " + str(idx) + " error =>" + ret
        idx += 1
    return None


def _checkJsonOneItem(j: json, pid: int, meteor: str, stop_dat_list: list) -> str:
    idx = 0
    valeurs_to_add = []
    extremes_to_add = []
    new_val = {}
    new_val_xtreme = {}
    stop_dat_list = []
    start_dat_list = []

    # add this key used in app
    j["poste_id"] = pid

    # check meteor code
    if j.__contains__("meteor") is False or j["meteor"].__len__() == 0:
        return "missing or invalid code meteor"

    if j["meteor"] != meteor:
        return "different code meteor: " + meteor + "/" + j["meteor"]

    # check info
    if j.get("info") is None:
        return "no info key"
    j_info = j["info"]
    if j.get("info") is None or j_info["version"] != 1:
        return "unsupported version number: " + str(j_info.get("version"))

    json_type = j_info.get("json_type")
    if str(json_type) not in ["O", "C", "H", "D", "M", "Y", "A"]:
        return "invalid json_type: " + str(json_type)

    # check data, loop for each item
    while idx < j["data"].__len__():
        a_data_item = j["data"][idx]

        # check dates
        if json_type in ["O", "C"]:
            if a_data_item.get("stop_dat") is None:
                return "missing stop_dat !"

            tmp_stop_dat = a_data_item.get("stop_dat")
            if str(tmp_stop_dat) in stop_dat_list:
                return "stop_dat: " + str(tmp_stop_dat) + " present twice"
            stop_dat_list.append(str(tmp_stop_dat))

            if a_data_item.get("start_dat") is not None:
                return "remove start_dat for json_type " + json_type

            if a_data_item.get("duration") is None:
                return "missing duration"
            # measure_duration = a_data_item.get("duration")
        else:
            if a_data_item.get("start_dat") is None:
                return "missing start_dat !"

            if a_data_item.get("stop_dat") is not None:
                return "remove stop_dat for json_type " + json_type

            tmp_start_dat = a_data_item.get("start_dat")
            if str(tmp_start_dat) in start_dat_list:
                return "start_dat: " + str(tmp_start_dat) + " present twice"
            start_dat_list.append(str(tmp_start_dat))

            if a_data_item.get("duration") is not None:
                return "remove duration for json_type " + json_type

            agg_duration = getAggDuration(json_type, datetime.datetime(tmp_start_dat))

        if a_data_item.get("current") is not None:
            return "remove current key"

        if a_data_item.get("valeurs") is None:
            return "missing valeurs"
        j_valeurs = a_data_item.get("valeurs")

        # loop in all keys
        for key in j_valeurs.__iter__():
            j_value = j_valeurs.get(key)
            if json_type in ["O", "C"]:
                # check obs data
                if str(key).endswith("_max") or str(key).endswith("_min"):
                    # add a time entry if not present
                    if j_valeurs.__contains__(key + "_time") is False:
                        new_val = {
                            "k": key + "_time",
                            "v": tmp_stop_dat,
                            "idx": idx,
                            "k2": "valeurs",
                        }
                        valeurs_to_add.append(new_val)
                    else:
                        try:
                            dateutil.parser.parse(j_value)
                        except Exception:
                            return "Invalid date format for key " + key + " => " + str(j_value)
                    if isinstance(j_valeurs[key], float) is False:
                        return "key " + key + " should be a float. current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

                # change xxx_sum into xxx_s
                if str(key).endswith("_sum"):
                    new_val = {
                        "k": str(key).replace("_sum", "_s"),
                        "v": j_valeurs[key],
                        "idx": idx,
                        "k2": "valeurs",
                    }
                    valeurs_to_add.append(new_val)

                # change xx_duration into xxx_d
                if str(key).endswith("_duration"):
                    new_val = {
                        "k": str(key).replace("_duration", "_d"),
                        "v": j_valeurs[key],
                        "idx": idx,
                        "k2": "valeurs",
                    }
                    valeurs_to_add.append(new_val)
                    if isinstance(j_valeurs[key], int) is False:
                        return "key " + key + " should be an integer. Current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

            else:
                # check pre_aggregated data
                if str(key).endswith("_max") or str(key).endswith("_min"):
                    if j_valeurs.__contains__(key + "_time") is False:
                        return "key: " + key + " have no key " + key + "_time"

                # check that xxx_s has a xxx_d
                if str(key).endswith("_s") and j_valeurs.get(str(key).replace("_s", "_d")) is None:
                    new_val = {
                        "k": str(key).replace("_s", "_d"),
                        "v": agg_duration,
                        "idx": idx,
                        "k2": "valeurs",
                    }
                    valeurs_to_add.append(new_val)
                    if isinstance(j_valeurs[key], float) is False and isinstance(j_valeurs[key], int) is False:
                        return "key " + key + " should be a float or an integer. Current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

                # check that xxx_avg has a xxx_d
                if str(key).endswith("_avg") and j_valeurs.get(str(key).replace("_avg", "_d")) is None:
                    new_val = {
                        "k": str(key).replace("_avg", "_d"),
                        "v": agg_duration,
                        "idx": idx,
                        "k2": "valeurs",
                    }
                    valeurs_to_add.append(new_val)
                    if isinstance(j_valeurs[key], float) is False and isinstance(j_valeurs[key], int) is False:
                        return "key " + key + " should be a float or an integer. Current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

            # for all json_type
            if str(key).endswith("_s") or str(key).endswith("_avg") or str(key).endswith("_max") or str(key).endswith("_min"):
                if isinstance(j_valeurs[key], float) is False and isinstance(j_valeurs[key], int) is False:
                    return "key " + key + " should be a float or an integer. Current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

            # check date format
            if key.endswith("_time"):
                try:
                    dateutil.parser.parse(j_value)
                except Exception:
                    return "Invalid date format for key " + key + " => " + str(j_value)

    # extremes check
    an_extreme = j.get("extremes")
    if an_extreme is not None:
        if an_extreme.get("level"):
            return "extreme should have a level key"

        if an_extreme["level"] != "D":
            return "only level=D supported in this version"

        for key in an_extreme.__iter__():

            # rename _sum into _s
            if str(key).endswith("_sum"):
                if str(key).endswith("_s") is False:
                    new_val_xtreme = {
                        "k": str(key).replace("_sum", "_s"),
                        "v": an_extreme[key],
                    }
                    extremes_to_add.append(new_val_xtreme)

            # a xxx_time is required with xxx_max/xxx_min values
            if str(key).endswith("_max") or str(key).endswith("_min"):
                if an_extreme.__contains__(key + "_time") is False:
                    return "max/min for " + key + " does not have a " + key + "_time key"

            # check number format
            if str(key).endswith("_s") or str(key).endswith("_avg") or str(key).endswith("_max") or str(key).endswith("_min"):
                if isinstance(j_valeurs[key], float) is False and isinstance(j_valeurs[key], int) is False:
                    return "key " + key + " should be a float or an integer. Current value: " + str(j_valeurs[key]) + ", type: " + str(type(j_valeurs[key]))

            # check date format
            if key.endswith("_time"):
                try:
                    dateutil.parser.parse(j_value)
                except Exception:
                    return "Invalid date format for key " + key + " => " + str(j_value)

    # add missing key/value
    for my_val in valeurs_to_add:
        my_data = j["data"][my_val["idx"]]
        if my_val.get("k2") is None:
            my_data[my_val["k"]] = my_val["v"]
        else:
            my_data[my_val["k2"]][my_val["k"]] = my_val["v"]

    for my_val in extremes_to_add:
        my_aggregations = j["extremes"]
        my_aggregations[my_val["k"]] = my_val["v"]

    # check ok
    return None
