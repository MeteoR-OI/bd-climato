from django.core.management.base import BaseCommand
from app.tools.dateTools import str_to_date
from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.posteMeteor import PosteMeteor
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pid', type=str, nargs='?', default='*', help='filename with extension (should be in data/json_not_in_git')
        parser.add_argument('--from', action='store_true', help='beginning of start_date included')
        parser.add_argument('--to', action='store_true', help='end of start_dat included')
        parser.add_argument('--details', action='store_true', help='dump all, including matching values')
        parser.add_argument('--hour', action='store_true', help='Check only hour aggregations')
        parser.add_argument('--day', action='store_true', help='Check only day aggregations')
        parser.add_argument('--month', action='store_true', help='Check only month aggregations')
        parser.add_argument('--year', action='store_true', help='Check only year aggregations')
        parser.add_argument('--all', action='store_true', help='Check only all aggregations')

    def handle(self, *args, **options):
        if options['pid']:
            poste_id = int(options['pid'])
        else:
            raise Exception("compAgg", "missing poste_id")

        from_dt = datetime.datetime(1900, 1, 1)
        if options['from']:
            from_dt = str_to_date(options['from'])

        to_dt = datetime.datetime(2900, 1, 1)
        if options['to']:
            to_dt = str_to_date(options['to'])

        disp_details = False
        if options['details']:
            disp_details = True

        level = "*"

        if options['hour']:
            level = "H"

        if options['day']:
            level = "D"

        if options['month']:
            level = "M"

        if options['year']:
            level = "Y"

        if options['all']:
            level = "A"

        analyseAggreg(poste_id, from_dt, to_dt, disp_details, level)


def analyseAggreg(poste_id: int, from_dt: datetime, to_dt: datetime, disp_details: bool, disp_level: str):
    p = PosteMeteor(poste_id)
    agg_done = tmp_agg_done = False
    for level in ['H', 'D', 'M', 'Y', 'A']:
        if disp_level == '*' or disp_level == level:
            display('Poste ' + p.data.meteor + ' level: ' + disp_level)

            tmp_agg_obj = AggMeteor.GetAggObj(level + 'T')
            agg_obj = AggMeteor.GetAggObj(level)

            all_agg = agg_obj.objects.filter(poste_id_id=poste_id).order_by("start_dat").all()
            all_tmp_agg = tmp_agg_obj.objects.filter(poste_id_id=poste_id).order_by("start_dat").all()

            idx = idx_tmp = 0
            max_idx = max(all_agg.count(), all_tmp_agg.count())
            while (max(idx, idx_tmp) < max_idx):
                my_agg = all_agg[idx]
                my_tmp_agg = all_tmp_agg[idx_tmp]

                if str(my_agg.start_dat) < str(from_dt):
                    idx += 1
                    continue
                if str(my_agg.start_dat) > str(to_dt):
                    agg_done = True

                if str(my_tmp_agg.start_dat) < str(from_dt):
                    idx_tmp += 1
                    continue
                if str(my_tmp_agg.start_dat) > str(to_dt):
                    tmp_agg_done = True

                if tmp_agg_done is True or str(my_agg.start_dat) < str(my_tmp_agg.start_dat):
                    display_missing_tmp_agg(my_agg, disp_details)
                    idx += 1
                    continue

                if agg_done is True or str(my_agg.start_dat) > str(my_tmp_agg.start_dat):
                    display_missing_agg(my_tmp_agg, disp_details)
                    idx_tmp += 1
                    continue

                if agg_done is True and tmp_agg_done is True:
                    break

                k_processed = []
                data_output = []

                # process values in agg
                for k, v in my_tmp_agg.j.items():
                    k_processed.append(k)
                    if str(v) == str(my_agg.j.get(k)):
                        continue
                    cols = []
                    cols.append(k)
                    cols.append(str(v))
                    if my_agg.j.get(k) is None:
                        cols.append('')
                    else:
                        cols.append(str(my_agg.j.get(k)))
                    data_output.append(cols)

                # ad values in agg, not in tmp_agg
                for k, v in my_agg.j.items():
                    if k not in k_processed:
                        cols = []
                        cols.append(k)
                        cols.append('')
                        cols.append(str(v))
                        data_output.append(cols)
                if data_output.__len__() > 0:
                    display_hdr(my_tmp_agg.start_dat, my_agg.start_dat)
                    # data_sorted = data_output.sort(key=lambda x: x[0])
                    for line in data_output:
                        display_line('   ' + line[0], line[1], line[2])
                # else:
                #     display_line('start_dat', my_agg.start_dat, ' ** OK **')

                idx += 1
                idx_tmp += 1


def display(msg: str):
    print(msg)


def display_missing_tmp_agg(one_agg: AggMeteor, disp_details: bool):
    # display('')
    display_hdr('           ?????', one_agg.start_dat)
    # if disp_details is True:
    #     for k, v in one_agg.j.items():
    #         display_line('   ' + k, str(v), '')


def display_missing_agg(one_agg: AggMeteor, disp_details: bool):
    display_hdr(one_agg.start_dat, '           ?????')
    # if disp_details is True:
    #     for k, v in one_agg.j.items():
    #         display_line('   ' + k, '', str(v))


def display_line(key, left, right):
    print("{:<20}".format(str(key))[0:20] + " I " + "{:<30}".format(str(left))[0:30] + " I " + "{:<30}".format(str(right))[0:30])


def display_hdr(tmp_agg_data, agg_data):
    tirets = '---------------------------------------------------------------------------------'
    display_line(tirets, tirets, tirets)
    display_line('      key', '      tmp_agg_xxx', '     agg_xxx')
    display_line(tirets, tirets, tirets)
    display_line('start_dat', str(tmp_agg_data), str(agg_data))
    