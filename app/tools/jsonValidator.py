from app.classes.repository.posteMeteor import PosteMeteor
import datetime
import json
import sys


def checkJson(j_arr: json) -> str:
    """
    checkJson
        Check Json integrity

    Parameter:
        Json data
    """
    try:
        if j_arr[0].__contains__("meteor") is False or j_arr[0]["meteor"].__len__() == 0:
            return "missing or invalid code meteor"

        pid = PosteMeteor.getPosteIdByMeteor(j_arr[0]["meteor"])
        if pid is None:
            return "code meteor inconnu: " + j_arr[0]["meteor"]

        idx = 0
        while idx < j_arr.__len__():
            j = j_arr[idx]
            ret = _checkJsonOneItem(j, pid, j_arr[0]["meteor"])
            if ret is not None:
                return "Error in item " + str(idx) + ": " + ret
            idx += 1
    except Exception as e:
        if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            exception_info = e.__repr__()
            filename = exception_traceback.tb_frame.f_code.co_filename
            funcname = exception_traceback.tb_frame.f_code.co_name
            line_number = exception_traceback.tb_lineno
            e.info = {
                "i": str(exception_info),
                "n": funcname,
                "f": filename,
                "l": line_number,
            }
            e.done = True
        raise e


def _checkJsonOneItem(j: json, pid: int, meteor: str) -> str:
    try:
        idx = 0
        val_to_add = []
        val_to_add_agg = []
        val_to_add_val = []

        j["poste_id"] = pid

        if j.__contains__("meteor") is False or j["meteor"].__len__() == 0:
            return "missing or invalid code meteor"

        if j["meteor"] != meteor:
            return "different code meteor: " + meteor + "/" + j["meteor"]

        while idx < j["data"].__len__():
            new_val = {}
            new_val_agg = {}
            new_val_val = {}
            a_current = j["data"][idx].get("current")

            tmp_stop_dat = None
            if j["data"][idx].__contains__("stop_dat") is True:
                tmp_stop_dat = j["data"][idx]["stop_dat"]

            if a_current is None:
                if (
                    j["data"][idx].__contains__("aggregations") is False
                    and j["data"][idx].__contains__("validation") is False
                ):
                    return (
                        "no current/aggregations/validation key in j.data[" + str(idx) + "]"
                    )
            else:
                # check current key
                if a_current.__contains__("duration") is False:
                    return "no duration in j.data[" + str(idx) + "].current"
                measure_duration = a_current["duration"]

                tmp_stop_dat = None
                if j["data"][idx].__contains__("stop_dat") is False:
                    if j["data"][idx].__contains__("start_dat") is False:
                        return "no start and stop_dat in j.data[" + str(idx) + "].current"
                    measure_duration = datetime.timedelta(
                        minutes=int(a_current["duration"])
                    )
                    new_val = {
                        "k": "stop_dat",
                        "v": j["data"][idx]["start_dat"] + measure_duration,
                        "idx": idx,
                    }
                    val_to_add.append(new_val)
                    tmp_stop_dat = new_val["stop_dat"]
                else:
                    tmp_stop_dat = j["data"][idx]["stop_dat"]

                if j["data"][idx].__contains__("start_dat") is False:
                    measure_duration = datetime.timedelta(
                        minutes=int(a_current["duration"])
                    )
                    new_val = {
                        "k": "start_dat",
                        "v": j["data"][idx]["stop_dat"],
                        "idx": idx,
                    }
                    val_to_add.append(new_val)

                for key in a_current.__iter__():
                    if str(key).endswith("_max") or str(key).endswith("_min"):
                        if a_current.__contains__(key + "time") is True and a_current.__contains__(key + "_time") is False:
                            a_current[key + "_time"] = a_current[key + "time"]
                            new_val = {
                                "k": key + "_time",
                                "v": a_current[key + "time"],
                                "idx": idx,
                                "k2": "current",
                            }
                            val_to_add.append(new_val)

                        if a_current.__contains__(key + "_time") is False:
                            new_val = {
                                "k": key + "_time",
                                "v": j["data"][idx]["stop_dat"],
                                "idx": idx,
                                "k2": "current",
                            }
                            val_to_add.append(new_val)
                    if str(key).endswith("_sum"):
                        new_val = {
                            "k": str(key).replace("_sum", "_s"),
                            "v": a_current[key],
                            "idx": idx,
                            "k2": "current",
                        }
                        val_to_add.append(new_val)

                    if (str(key).endswith("_s") and a_current.__contains__(key[:-4] + "_duration") is False):
                        new_val = {
                            "k": key[:-4] + "_duration",
                            "v": measure_duration,
                            "idx": idx,
                            "k2": "current",
                        }
                        val_to_add.append(new_val)

                # old specification...
                if j["data"][idx]["current"].__contains__("aggregations"):
                    return "aggregations is under the key current, should be at same level"

            if tmp_stop_dat is None:
                return "no stop_dat, and no way to compute it"

            all_aggreg = j["data"][idx].get("aggregations")
            if all_aggreg is not None:
                idx2 = 0
                while idx2 < all_aggreg.__len__():
                    a_aggreg = j["data"][idx]["aggregations"][idx2]
                    if a_aggreg.__contains__("level") is False:
                        return (
                            "no level in data["
                            + str(idx)
                            + "].aggregations["
                            + str(idx2)
                            + "]"
                        )
                    lvl = a_aggreg["level"]
                    if (
                        lvl != "H"
                        and lvl != "D"
                        and lvl != "M"
                        and lvl != "Y"
                        and lvl != "A"
                    ):
                        return (
                            lvl
                            + " is invalid level in data["
                            + str(idx)
                            + "].aggregations["
                            + str(idx2)
                            + "]"
                        )
                    for key in a_aggreg.__iter__():
                        if str(key).endswith("_sum") and str(key).endswith("_s") is False:
                            new_val_agg = {
                                "k": str(key).replace("_sum", "_s"),
                                "v": a_aggreg[key],
                                "idx": idx,
                                "idx2": idx2,
                            }
                            val_to_add_agg.append(new_val_agg)

                        if str(key).endswith("_max") or str(key).endswith("_min"):
                            if all_aggreg.__contains__(key + "_time") is False:
                                new_val_agg = {
                                    "k": key + "_time",
                                    "v": j["data"][idx]["stop_dat"],
                                    "idx": idx,
                                    "idx2": idx2,
                                }
                                val_to_add_agg.append(new_val_agg)
                    idx2 += 1

            all_validations = j["data"][idx].get("validation")
            if all_validations is not None:
                idx2 = 0
                while idx2 < all_validations.__len__():
                    a_aggreg = j["data"][idx]["validation"][idx2]

                    if a_aggreg.__contains__("level") is False:
                        return (
                            "no level in data["
                            + str(idx)
                            + "].validation["
                            + str(idx2)
                            + "]"
                        )
                    lvl = a_aggreg["level"]
                    if (
                        lvl != "H"
                        and lvl != "D"
                        and lvl != "M"
                        and lvl != "Y"
                        and lvl != "A"
                    ):
                        return (
                            lvl
                            + " is invalid level in data["
                            + str(idx)
                            + "].validation["
                            + str(idx2)
                            + "]"
                        )
                    for key in all_validations[idx2].__iter__():
                        # if str(key) == 'out_temp_omm_min':
                        #     key = 'out_temp_omm_min'
                        if str(key).endswith("time") and str(key).endswith("_time") is False:
                            new_val_val = {
                                "k": str(key).replace("time", "_time"),
                                "v": all_validations[idx2][key],
                                "idx2": idx2,
                                "idx": idx,
                            }
                            val_to_add_val.append(new_val_val)

                        # fix XX_sum -> XX_s
                        if str(key).endswith("_sum") and str(key).endswith("_s") is False:
                            new_val_val = {
                                "k": str(key).replace("_sum", "_s"),
                                "v": all_validations[idx2][key],
                                "idx2": idx2,
                                "idx": idx,
                            }
                            val_to_add_val.append(new_val_val)

                        if str(key).endswith("_max") or str(key).endswith("_min"):
                            if all_validations[idx2].__contains__(key + "time") is True and all_validations[idx2].__contains__(key + "_time") is False:
                                new_val_val = {
                                    "k": key + '_time',
                                    "v": all_validations[idx2][key],
                                    "idx2": idx2,
                                    "idx": idx,
                                }
                                val_to_add_val.append(new_val_val)

                            if all_validations[idx2].__contains__(key + "_time") is False:
                                new_val_val = {
                                    "k": key + "_time",
                                    "v": j["data"][idx]["stop_dat"],
                                    "idx2": idx2,
                                    "idx": idx,
                                }
                                val_to_add_val.append(new_val_val)

                    idx2 += 1
            idx += 1

        # add missing key/value
        for my_val in val_to_add:
            my_data = j["data"][my_val["idx"]]
            if my_val.get("k2") is None:
                my_data[my_val["k"]] = my_val["v"]
            else:
                my_data[my_val["k2"]][my_val["k"]] = my_val["v"]

        for my_val in val_to_add_agg:
            my_aggregations = j["data"][my_val["idx"]]["aggregations"]
            my_aggregations[my_val["idx2"]][my_val["k"]] = my_val["v"]

        for my_val in val_to_add_val:
            my_validation = j["data"][my_val["idx"]]["validation"]
            my_validation[my_val["idx2"]][my_val["k"]] = my_val["v"]
        return None
    except Exception as e:
        if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            exception_info = e.__repr__()
            filename = exception_traceback.tb_frame.f_code.co_filename
            funcname = exception_traceback.tb_frame.f_code.co_name
            line_number = exception_traceback.tb_lineno
            e.info = {
                "i": str(exception_info),
                "n": funcname,
                "f": filename,
                "l": line_number,
            }
            e.done = True
        raise e
