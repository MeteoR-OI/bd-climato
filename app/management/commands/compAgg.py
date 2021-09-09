from django.core.management.base import BaseCommand
from app.tools.dateTools import str_to_date
from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.posteMeteor import PosteMeteor
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
import sys
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("pid", type=str, nargs="?", default="*", help="poste_id")
        parser.add_argument(
            "--from", action="store_true", help="beginning of start_date included"
        )
        parser.add_argument(
            "--to", action="store_true", help="end of start_dat included"
        )
        parser.add_argument(
            "--details", action="store_true", help="dump all, including matching values"
        )
        parser.add_argument(
            "--hour", action="store_true", help="Check only hour aggregations"
        )
        parser.add_argument(
            "--day", action="store_true", help="Check only day aggregations"
        )
        parser.add_argument(
            "--month", action="store_true", help="Check only month aggregations"
        )
        parser.add_argument(
            "--year", action="store_true", help="Check only year aggregations"
        )
        parser.add_argument(
            "--all", action="store_true", help="Check only all aggregations"
        )

    def handle(self, *args, **options):
        try:
            if options["pid"]:
                poste_id = int(options["pid"])
            else:
                raise Exception("compAgg", "missing poste_id")

            from_dt = datetime.datetime(1900, 1, 1)
            if options["from"]:
                from_dt = str_to_date(options["from"])

            to_dt = datetime.datetime(2900, 1, 1)
            if options["to"]:
                to_dt = str_to_date(options["to"])

            disp_details = False
            if options["details"]:
                disp_details = True

            level = "*"

            if options["hour"]:
                level = "H"

            if options["day"]:
                level = "D"

            if options["month"]:
                level = "M"

            if options["year"]:
                level = "Y"

            if options["all"]:
                level = "A"

            self.analyseAggreg(poste_id, from_dt, to_dt, disp_details, level)
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            errMsg = t.LogCritical(e, None, {}, True)
            print(errMsg)
            exit(0)

    def analyseAggreg(
        self,
        poste_id: int,
        from_dt: datetime,
        to_dt: datetime,
        disp_details: bool,
        disp_level: str,
    ):
        try:
            p = PosteMeteor(poste_id)
            agg_done = tmp_agg_done = False
            for level in ["H", "D", "M", "Y", "A"]:
                if disp_level == "*" or disp_level == level:
                    self.display("Poste " + p.data.meteor + " level: " + disp_level)

                    tmp_agg_obj = AggMeteor.GetAggObj(level + "T")
                    agg_obj = AggMeteor.GetAggObj(level)

                    all_agg = (
                        agg_obj.objects.filter(poste_id_id=poste_id)
                        .order_by("start_dat")
                        .all()
                    )
                    all_tmp_agg = (
                        tmp_agg_obj.objects.filter(poste_id_id=poste_id)
                        .order_by("start_dat")
                        .all()
                    )

                    idx = idx_tmp = 0
                    nb_agg = all_agg.count()
                    nb_tmp_agg = all_tmp_agg.count()
                    max_idx = max(nb_agg, nb_tmp_agg)
                    my_agg = my_tmp_agg = None
                    while max(idx, idx_tmp) < max_idx:
                        if idx >= nb_agg:
                            agg_done = True
                            my_agg = None
                        else:
                            my_agg = all_agg[idx]

                        if idx_tmp >= nb_tmp_agg:
                            tmp_agg_done = True
                            my_tmp_agg = None
                        else:
                            my_tmp_agg = all_tmp_agg[idx_tmp]

                        # if my_agg is None:
                        #     print("my_agg: None")
                        # else:
                        #     print("my_agg: " + str(my_agg.start_dat))

                        # if my_tmp_agg is None:
                        #     print("my_tmp_agg: None")
                        # else:
                        #     print("my_tmp_agg: " + str(my_tmp_agg.start_dat))

                        if str(my_agg is not None and my_agg.start_dat) < str(from_dt):
                            idx += 1
                            continue
                        if str(my_agg is not None and my_agg.start_dat) > str(to_dt):
                            my_agg = None
                            agg_done = True

                        if str(my_tmp_agg is not None and my_tmp_agg.start_dat) < str(from_dt):
                            idx_tmp += 1
                            continue
                        if str(my_tmp_agg is not None and my_tmp_agg.start_dat) > str(to_dt):
                            tmp_agg_done = True
                            my_tmp_agg = None

                        if agg_done is True and tmp_agg_done is True:
                            print("stop")
                            break

                        if my_agg is None and my_tmp_agg is None:
                            t.LogError("both aggregations can't be None!!!")
                            break

                        if my_tmp_agg is None or str(my_agg.start_dat) < str(my_tmp_agg.start_dat):
                            my_tmp_agg = None
                        elif my_agg is None or str(my_agg.start_dat) > str(my_tmp_agg.start_dat):
                            my_agg = None

                        k_processed = []
                        data_output = []

                        # process values in agg
                        if my_tmp_agg is not None:
                            for k, v in my_tmp_agg.j.items():
                                if "_omm_max" in k or "_omm_min" in k:
                                    continue
                                if k not in k_processed:
                                    k_processed.append(k)
                                    cols = []
                                    cols.append(k)
                                    if my_agg is None or agg_done or my_agg.j.get(k) is None:
                                        cols.append("")
                                    else:
                                        if k == 'rx_avg':
                                            my_value = 1
                                        my_value = self.fix_s(my_agg, my_tmp_agg, k)
                                        cols.append(str(my_value))
                                    cols.append(str(v))
                                    data_output.append(cols)

                        if my_agg is not None:
                            # ad values in agg, not in tmp_agg
                            for k, v in my_agg.j.items():
                                if "_omm_max" in k or "_omm_min" in k:
                                    continue
                                if k not in k_processed:
                                    cols = []
                                    cols.append(k)
                                    cols.append(str(v))
                                    cols.append("")
                                    data_output.append(cols)

                        if data_output.__len__() > 0:
                            self.display_hdr(
                                my_agg.start_dat if my_agg is not None else "",
                                my_tmp_agg.start_dat if my_tmp_agg is not None else "",
                                level,
                            )
                            # data_sorted = data_output.sort(key=lambda x: x[0])
                            data_sorted = sorted(data_output, key=lambda x: x[0])
                            for line in data_sorted:
                                # if str(line[0]).endswith('_s'):
                                #     continue
                                # if str(line[0]).endswith('_duration'):
                                #     continue
                                tmp_f1 = self.is_float_try(line[1])
                                tmp_prec = 0
                                bIsFloat = True
                                if line[0] == "barometer_avg":
                                    line[0] = "barometer_avg"
                                if tmp_f1 is None:
                                    bIsFloat = False
                                    tmp_f1 = line[1]
                                tmp_f2 = self.is_float_try(line[2])
                                if tmp_f2 is None:
                                    bIsFloat = False
                                    tmp_f2 = line[2]
                                if bIsFloat is True and tmp_f1 != 0:
                                    tmp_delta = tmp_f1 - tmp_f2
                                    tmp_prec = abs((tmp_delta / tmp_f1) * 100)
                                    tmp_prec = int(tmp_prec * 10000) / 10000
                                if tmp_prec > 0 and tmp_prec < 1:
                                    self.display_line("   " + line[0], "  ", "  ", str(tmp_f1) + ' (@' + str(tmp_prec) + '%)')
                                else:
                                    if str(tmp_f1) == str(tmp_f2):
                                        self.display_line("   " + line[0], "  ", "  ", str(tmp_f1))
                                    else:
                                        self.display_line("   " + line[0], str(tmp_f1), str(tmp_f2))

                        if my_agg is not None:
                            idx += 1
                        if my_tmp_agg is not None:
                            idx_tmp += 1

        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def fix_s(self, my_agg, my_tmp_agg, k: str):
        """
        """
        try:
            my_value = my_agg.j.get(k)
            if str(k).endswith('_s'):
                k_root = str(k).replace('_s', '')
                my_agg_avg = my_agg.j.get(k_root + '_avg')
                my_agg_duration = my_agg.j.get(k_root + '_duration')
                my_tmp_agg_avg = my_tmp_agg.j.get(k_root + '_avg')
                my_tmp_agg_duration = my_tmp_agg.j.get(k_root + '_duration')
                if my_agg_avg is None or my_agg_duration is None:
                    return my_value
                if int(my_agg_avg * 10) == int(my_tmp_agg_avg * 10) and my_agg_duration == my_tmp_agg_duration:
                    my_value = my_tmp_agg.j[k]
            return my_value

        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def is_float_try(self, str):
        try:
            if str == "":
                return None
            f = float(str)
            return int(f * 1000) / 1000
        except ValueError:
            return None

    def display(self, msg: str):
        print(msg)

    def display_missing_tmp_agg(
        self, one_agg: AggMeteor, level: str, disp_details: bool
    ):
        # display('')
        self.display_hdr(one_agg.start_dat, "           None", level)
        # if disp_details is True:
        #     for k, v in one_agg.j.items():
        #         display_line('   ' + k, str(v), '')

    def display_missing_agg(self, tmp_agg: AggMeteor, level: str, disp_details: bool):
        self.display_hdr("           None", tmp_agg.start_dat, level)

        # if disp_details is True:
        #     for k, v in one_agg.j.items():
        #         display_line('   ' + k, '', str(v))

    def display_line(self, key, agg_val, tmp_agg_val, tmp_common: str = ""):
        """
        display_line
            disply a line of text
        """
        try:
            self.display(
                "{:<30}".format(str(key))[0:30]
                + " I "
                + "{:<30}".format(str(agg_val))[0:30]
                + " I "
                + "{:<30}".format(str(tmp_common))[0:30]
                + " I "
                + "{:<30}".format(str(tmp_agg_val))[0:30]
            )

        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def display_hdr(self, agg_data, tmp_agg_data, level: str = "xxxx"):
        try:
            # level = my_agg.getLevel()
            tirets = "---------------------------------------------------------------------------------"
            self.display_line(tirets, tirets, tirets, tirets)
            self.display_line(
                "        key",
                "         agg_" + level + " only",
                "       tmp_agg_" + level + " only",
                "       both",
            )
            self.display_line(tirets, tirets, tirets, tirets)
            if str(agg_data) == str(tmp_agg_data):
                self.display_line("start_dat", " ", " ", str(tmp_agg_data))
            else:
                self.display_line("start_dat", str(agg_data), str(tmp_agg_data))
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e
