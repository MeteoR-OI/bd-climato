from app.models import Exclusion
import datetime
from datetime import timedelta
import json


class ExcluMeteor():
    """
        ExcluMeteor

        gere les objets Observation metier

        o=ExcluMeteor(poste, dat)
        o.data -> Observation object (data, methods...)

        value is a json with:
            key = measure name (ie. 'out_temp')
            value =
                'value' => keep the value from the json file
                'null'  => measure is invalid
                data    => force this data in the measure (numeric)
    """

    def __init__(self, exclu_id: int):
        """Init a new ExcluMeteor object"""

        if Exclusion.objects.filter(id=exclu_id).exists():
            self.data = Exclusion.objects.filter(id=exclu_id).first()
        else:
            self.data = Exclusion()

    @staticmethod
    def getExclusForAPoste(
        poste_id: int,
        measure_start_dat: datetime = datetime.datetime.now(),
        measure_stop_dat: datetime = datetime.datetime(2100, 12, 31, 23, 59, 59)
    ) -> json:
        tmp_exlus = Exclusion.objects.filter(poste_id=poste_id).filter(start_dat__gte=measure_start_dat).filter(stop_dat__lt=measure_stop_dat).order_by('start_dat').first()
        return tmp_exlus

    def save(self, auto_close=False):
        """ save Exclusions, and check it is a new date range """
        exclus_count_left = Exclusion.objects.filter(poste_id=self.data.poste_id).filter(stop_dat__lt=self.data.stop_dat).filter(stop_dat__gt=self.data.start_dat).count()
        exclus_count_right = Exclusion.objects \
            .filter(poste_id=self.data.poste_id) \
            .filter(start_dat__gt=self.data.start_dat) \
            .filter(start_dat__lt=self.data.stop_dat) \
            .filter(stop_dat__gte=self.data.stop_dat) \
            .count()
        exclus_count_bigger = Exclusion.objects.filter(poste_id=self.data.poste_id).filter(start_dat__lt=self.data.start_dat).filter(stop_dat__gte=self.data.stop_dat).count()
        print('left: ' + str(exclus_count_left) + ', right: ' + str(exclus_count_right) + ', big: ' + str(exclus_count_bigger))

        if (exclus_count_left + exclus_count_right + exclus_count_bigger) > 0:
            if auto_close is False:
                raise Exception('Already an exclusion for the period')
            else:
                if (exclus_count_left + exclus_count_right + exclus_count_bigger) > 1:
                    raise Exception('More than one exclusion is covering the period')
                if exclus_count_right > 0:
                    raise Exception('An exclusion is starting in the period')
                exclus_to_close = None
                if exclus_count_left > 0:
                    exclus_to_close = Exclusion.objects \
                        .filter(poste_id=self.data.poste_id) \
                        .filter(start_dat__gt=self.data.start_dat) \
                        .filter(start_dat__lt=self.data.stop_dat) \
                        .filter(stop_dat__gte=self.data.stop_dat) \
                        .first()
                    if exclus_to_close.stop_dat.year != 2100:
                        raise Exception('The inner exclusion has a closing date, id: ' + str(exclus_to_close.id))
                    if exclus_to_close.start_dat > self.data.start_dat:
                        raise Exception('Cannot fix an inner exclusion, id: ' + str(exclus_to_close.id))
                if exclus_count_bigger > 0:
                    exclus_to_close = Exclusion.objects.filter(poste_id=self.data.poste_id).filter(start_dat__lt=self.data.start_dat).filter(stop_dat__gte=self.data.stop_dat).first()

                if exclus_to_close is not None:
                    print(str(exclus_to_close))
                    exclus_to_close.stop_dat = self.data.start_dat - timedelta(seconds=1)
                    print(str(exclus_to_close))
                    exclus_to_close.save()

        print(str(self.data))
        self.data.save()

    def delete(self):
        """ save Poste and Exclusions """
        self.data.delete()

    def __str__(self):
        """print myself"""
        return "ExcluMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste.id) + ", start_dat: " + str(self.data.start_dat) + ", stop_dat: " + str(self.data.stop_dat)
