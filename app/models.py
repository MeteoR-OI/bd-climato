from django.db import models
from django.utils import timezone
 

class Poste(models.Model):
    GESTION_EXTREME = (
        ('0', 'Unconnu'),
        ('1', 'Auto dans observation'),
        ('2', 'Auto dans agrégation'),
        ('3', 'Manuel'),
    )
    NIVEAU_AGGREGATION = (
        ('', 'not set'),
        ('H', 'Heure'),
        ('D', 'Day'),
        ('M', 'Month'),
        ('Y', 'Year'),
        ('A', 'Global'),
    )
# timezone.now
#    id = models.AutoField(primary_key=True)
    meteor = models.CharField(max_length=10, verbose_name="Code MeteoR.OI")
    meteofr = models.CharField(null=True, max_length=10, verbose_name="Code Meteo France")
    title = models.CharField(max_length=50, verbose_name="Nom clair de la station")
    cas_gestion_extreme = models.CharField(default='0', max_length=1, choices=GESTION_EXTREME, verbose_name="Gestion des extrêmes")
    agg_min_extreme = models.CharField(null=True, max_length=1, default='', choices=NIVEAU_AGGREGATION, verbose_name="Niveau Agregation, Auto dans agregation")
    owner = models.CharField(max_length=50, verbose_name="Station Owner Name")
    email = models.CharField(max_length=50, verbose_name="E-Mail")
    phone = models.CharField(max_length=50, verbose_name="Phone")
    address = models.CharField(max_length=50, verbose_name="Address")
    zip = models.CharField(default="", max_length=10, verbose_name="Zip")
    city = models.CharField(max_length=50, default="", verbose_name="City")
    country = models.CharField(max_length=50, default="", verbose_name="Country")

    latitude = models.FloatField(default=0, verbose_name="Latitude")
    longitude = models.FloatField(default=0, verbose_name="Longitude")
    start = models.DateTimeField(default=timezone.now, verbose_name="Date d'entrée dans le réseau")
    end = models.DateTimeField(null=True, verbose_name="Date de sortie du réseau")
    comment = models.TextField(null=True, default=None)

    def __str__(self):
        return self.meteor + ", id: " + str(self.id)

    class Meta:
        db_table = "poste"


class TypeInstrument(models.Model):
    name = models.CharField(max_length=10, verbose_name="Type de Donnees")
    model_value = models.JSONField(verbose_name="JsonB")

    def __str__(self):
        return "type_instrument id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "type_instrument"


class Exclusion(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    type_instrument = models.ForeignKey(to="TypeInstrument", on_delete=models.CASCADE)
    start_x = models.DateTimeField(default=timezone.now)
    end_x = models.DateTimeField(default=timezone.datetime(2100, 12, 21))
    value = models.JSONField(verbose_name="JsonB")
 
    def __str__(self):
        return "observation id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "exclusion"


class Observation(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)

    out_temp = models.DecimalField(max_digits=3, decimal_places=1, null=True, verbose_name="out temp")
    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True, verbose_name="out temp max")
    out_temp_max_time = models.DateTimeField(null=True, verbose_name="out temp max time")
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)
    in_temp = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    heat_index = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    dewpoint = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    humidity = models.SmallIntegerField(null=True)
    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)
    inHumidity = models.SmallIntegerField(null=True)
    barometer = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)
    pressure = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_dir = models.SmallIntegerField(null=True)
    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)
    rain_sum = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    # rain_sum_1h...24h ??? to e decided...
    soil_temp = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_min_time = models.DateTimeField(null=True)
    uv = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_indixe = models.SmallIntegerField(null=True)
    etp = models.DecimalField(max_digits=5, decimal_places=3, null=True)    # check datatype
    solar_radiation = models.SmallIntegerField(null=True)  # check data type
    insolation_duration = models.SmallIntegerField(null=True)  # check data type, and what is that measure...
    rx = models.SmallIntegerField(null=True)
    voltage = models.SmallIntegerField(null=True)

    def __str__(self):
        return "observation id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "obs"
        unique_together = (("poste_id", "dat"))


class Agg_hour(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration")
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)
    
    out_temp_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_sum = models.IntegerField(null=True)
    out_temp_duration = models.IntegerField(null=True)

    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_max_time = models.DateTimeField(null=True)
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)

    in_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_max_time = models.DateTimeField(null=True)
    in_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_min_time = models.DateTimeField(null=True)
    
    heat_index_max = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    heat_index_max_time = models.DateTimeField(null=True)

    windchill_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_max_time = models.DateTimeField(null=True)
    windchill_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_min_time = models.DateTimeField(null=True)

    dewpoint_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_max_time = models.DateTimeField(null=True)
    dewpoint_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_min_time = models.DateTimeField(null=True)

    # humidity_sum/humidity_duration ???

    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)

    in_humidity_max = models.SmallIntegerField(null=True)
    in_humidity_max_time = models.DateTimeField(null=True)
    in_humidity_min = models.SmallIntegerField(null=True)
    in_humidity_min_time = models.SmallIntegerField(null=True)

    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_in_time = models.DateTimeField(null=True)

    barometer_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_sum = models.IntegerField(null=True)
    barometer_duration = models.IntegerField(null=True)

    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)

    rain_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_sum = models.IntegerField(null=True)  # ok to use int here instead of n(5,1) or 6,1 ?
    rain_duration = models.IntegerField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)

    # rain_sum_1h...24h ??? to be decided...

    wind_speed_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_speed_sum = models.IntegerField(null=True)
    win_speed_duration = models.IntegerField(null=True)

    wind_dir_avg = models.SmallIntegerField(null=True)
    wind_dir_sum = models.IntegerField(null=True)
    wind_dir_duration = models.IntegerField(null=True)

    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)

    # windRms windVecAvg, windVerDir ????

    uv_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_max_time = models.DateTimeField(null=True)
    uv_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_min_time = models.DateTimeField(null=True)

    # uv_indixe = models.SmallIntegerField(null=True)
    etp_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_max_time = models.DateTimeField(null=True)
    etp_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_min_time = models.DateTimeField(null=True)

    rx_avg = models.SmallIntegerField(null=True)
    rx_sum = models.IntegerField(null=True)
    rx_duration = models.IntegerField(null=True)
    rx_max = models.SmallIntegerField(null=True)
    rx_max_time = models.DateTimeField(null=True)
    rx_min = models.SmallIntegerField(null=True)
    rx_min_time = models.DateTimeField(null=True)

    voltage_avg = models.SmallIntegerField(null=True)
    voltage_sum = models.IntegerField(null=True)
    voltage_duration = models.IntegerField(null=True)
    voltage_max = models.SmallIntegerField(null=True)
    voltage_max_time = models.DateTimeField(null=True)
    voltage_min = models.SmallIntegerField(null=True)
    voltage_min_time = models.DateTimeField(null=True)

    # solar_radiation = models.SmallIntegerField(null=True)  # check data type
    # insolation_duration = models.SmallIntegerField(null=True) # check data type, and what is that measure...

    def __str__(self):
        return "agg_hour id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_hour"


class Agg_day(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)

    out_temp_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_sum = models.IntegerField(null=True)
    out_temp_duration = models.IntegerField(null=True)

    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_max_time = models.DateTimeField(null=True)
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)

    in_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_max_time = models.DateTimeField(null=True)
    in_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_min_time = models.DateTimeField(null=True)
    
    heat_index_max = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    heat_index_max_time = models.DateTimeField(null=True)

    windchill_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_max_time = models.DateTimeField(null=True)
    windchill_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_min_time = models.DateTimeField(null=True)

    dewpoint_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_max_time = models.DateTimeField(null=True)
    dewpoint_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_min_time = models.DateTimeField(null=True)

    # humidity_sum/humidity_duration ???

    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)

    in_humidity_max = models.SmallIntegerField(null=True)
    in_humidity_max_time = models.DateTimeField(null=True)
    in_humidity_min = models.SmallIntegerField(null=True)
    in_humidity_min_time = models.SmallIntegerField(null=True)

    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_in_time = models.DateTimeField(null=True)

    barometer_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_sum = models.IntegerField(null=True)
    barometer_duration = models.IntegerField(null=True)

    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)

    rain_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_sum = models.IntegerField(null=True)  # ok to use int here instead of n(5,1) or 6,1 ?
    rain_duration = models.IntegerField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)

    # rain_sum_1h...24h ??? to be decided...

    wind_speed_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_speed_sum = models.IntegerField(null=True)
    win_speed_duration = models.IntegerField(null=True)

    wind_dir_avg = models.SmallIntegerField(null=True)
    wind_dir_sum = models.IntegerField(null=True)
    wind_dir_duration = models.IntegerField(null=True)

    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)

    # windRms windVecAvg, windVerDir ????

    uv_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_max_time = models.DateTimeField(null=True)
    uv_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_min_time = models.DateTimeField(null=True)

    # uv_indixe = models.SmallIntegerField(null=True)
    etp_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_max_time = models.DateTimeField(null=True)
    etp_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_min_time = models.DateTimeField(null=True)

    rx_avg = models.SmallIntegerField(null=True)
    rx_sum = models.IntegerField(null=True)
    rx_duration = models.IntegerField(null=True)
    rx_max = models.SmallIntegerField(null=True)
    rx_max_time = models.DateTimeField(null=True)
    rx_min = models.SmallIntegerField(null=True)
    rx_min_time = models.DateTimeField(null=True)

    voltage_avg = models.SmallIntegerField(null=True)
    voltage_sum = models.IntegerField(null=True)
    voltage_duration = models.IntegerField(null=True)
    voltage_max = models.SmallIntegerField(null=True)
    voltage_max_time = models.DateTimeField(null=True)
    voltage_min = models.SmallIntegerField(null=True)
    voltage_min_time = models.DateTimeField(null=True)

    # solar_radiation = models.SmallIntegerField(null=True)  # check data type
    # insolation_duration = models.SmallIntegerField(null=True) # check data type, and what is that measure...
 
    def __str__(self):
        return "agg_day id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_day"



class Agg_month(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)

    out_temp_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_sum = models.IntegerField(null=True)
    out_temp_duration = models.IntegerField(null=True)

    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_max_time = models.DateTimeField(null=True)
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)

    in_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_max_time = models.DateTimeField(null=True)
    in_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_min_time = models.DateTimeField(null=True)
    
    heat_index_max = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    heat_index_max_time = models.DateTimeField(null=True)

    windchill_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_max_time = models.DateTimeField(null=True)
    windchill_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_min_time = models.DateTimeField(null=True)

    dewpoint_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_max_time = models.DateTimeField(null=True)
    dewpoint_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_min_time = models.DateTimeField(null=True)

    # humidity_sum/humidity_duration ???

    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)

    in_humidity_max = models.SmallIntegerField(null=True)
    in_humidity_max_time = models.DateTimeField(null=True)
    in_humidity_min = models.SmallIntegerField(null=True)
    in_humidity_min_time = models.SmallIntegerField(null=True)

    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_in_time = models.DateTimeField(null=True)

    barometer_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_sum = models.IntegerField(null=True)
    barometer_duration = models.IntegerField(null=True)

    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)

    rain_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_sum = models.IntegerField(null=True)  # ok to use int here instead of n(5,1) or 6,1 ?
    rain_duration = models.IntegerField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)

    # rain_sum_1h...24h ??? to be decided...

    wind_speed_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_speed_sum = models.IntegerField(null=True)
    win_speed_duration = models.IntegerField(null=True)

    wind_dir_avg = models.SmallIntegerField(null=True)
    wind_dir_sum = models.IntegerField(null=True)
    wind_dir_duration = models.IntegerField(null=True)

    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)

    # windRms windVecAvg, windVerDir ????

    uv_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_max_time = models.DateTimeField(null=True)
    uv_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_min_time = models.DateTimeField(null=True)

    # uv_indixe = models.SmallIntegerField(null=True)
    etp_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_max_time = models.DateTimeField(null=True)
    etp_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_min_time = models.DateTimeField(null=True)

    rx_avg = models.SmallIntegerField(null=True)
    rx_sum = models.IntegerField(null=True)
    rx_duration = models.IntegerField(null=True)
    rx_max = models.SmallIntegerField(null=True)
    rx_max_time = models.DateTimeField(null=True)
    rx_min = models.SmallIntegerField(null=True)
    rx_min_time = models.DateTimeField(null=True)

    voltage_avg = models.SmallIntegerField(null=True)
    voltage_sum = models.IntegerField(null=True)
    voltage_duration = models.IntegerField(null=True)
    voltage_max = models.SmallIntegerField(null=True)
    voltage_max_time = models.DateTimeField(null=True)
    voltage_min = models.SmallIntegerField(null=True)
    voltage_min_time = models.DateTimeField(null=True)

    # solar_radiation = models.SmallIntegerField(null=True)  # check data type
    # insolation_duration = models.SmallIntegerField(null=True) # check data type, and what is that measure...
 
    def __str__(self):
        return "agg_month id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_month"


class Agg_year(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)

    out_temp_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_sum = models.IntegerField(null=True)
    out_temp_duration = models.IntegerField(null=True)

    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_max_time = models.DateTimeField(null=True)
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)

    in_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_max_time = models.DateTimeField(null=True)
    in_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_min_time = models.DateTimeField(null=True)
    
    heat_index_max = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    heat_index_max_time = models.DateTimeField(null=True)

    windchill_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_max_time = models.DateTimeField(null=True)
    windchill_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_min_time = models.DateTimeField(null=True)

    dewpoint_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_max_time = models.DateTimeField(null=True)
    dewpoint_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_min_time = models.DateTimeField(null=True)

    # humidity_sum/humidity_duration ???

    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)

    in_humidity_max = models.SmallIntegerField(null=True)
    in_humidity_max_time = models.DateTimeField(null=True)
    in_humidity_min = models.SmallIntegerField(null=True)
    in_humidity_min_time = models.SmallIntegerField(null=True)

    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_in_time = models.DateTimeField(null=True)

    barometer_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_sum = models.IntegerField(null=True)
    barometer_duration = models.IntegerField(null=True)

    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)

    rain_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_sum = models.IntegerField(null=True)  # ok to use int here instead of n(5,1) or 6,1 ?
    rain_duration = models.IntegerField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)

    # rain_sum_1h...24h ??? to be decided...

    wind_speed_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_speed_sum = models.IntegerField(null=True)
    win_speed_duration = models.IntegerField(null=True)

    wind_dir_avg = models.SmallIntegerField(null=True)
    wind_dir_sum = models.IntegerField(null=True)
    wind_dir_duration = models.IntegerField(null=True)

    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)

    # windRms windVecAvg, windVerDir ????

    uv_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_max_time = models.DateTimeField(null=True)
    uv_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_min_time = models.DateTimeField(null=True)

    # uv_indixe = models.SmallIntegerField(null=True)
    etp_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_max_time = models.DateTimeField(null=True)
    etp_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_min_time = models.DateTimeField(null=True)

    rx_avg = models.SmallIntegerField(null=True)
    rx_sum = models.IntegerField(null=True)
    rx_duration = models.IntegerField(null=True)
    rx_max = models.SmallIntegerField(null=True)
    rx_max_time = models.DateTimeField(null=True)
    rx_min = models.SmallIntegerField(null=True)
    rx_min_time = models.DateTimeField(null=True)

    voltage_avg = models.SmallIntegerField(null=True)
    voltage_sum = models.IntegerField(null=True)
    voltage_duration = models.IntegerField(null=True)
    voltage_max = models.SmallIntegerField(null=True)
    voltage_max_time = models.DateTimeField(null=True)
    voltage_min = models.SmallIntegerField(null=True)
    voltage_min_time = models.DateTimeField(null=True)

    # solar_radiation = models.SmallIntegerField(null=True)  # check data type
    # insolation_duration = models.SmallIntegerField(null=True) # check data type, and what is that measure...
 
    def __str__(self):
        return "agg_year id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_year"



class Agg_global(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    qa_modifications = models.IntegerField(default='0')
    qa_incidents = models.IntegerField(default='0')
    qa_check_done = models.BooleanField(default=False)

    out_temp_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_sum = models.IntegerField(null=True)
    out_temp_duration = models.IntegerField(null=True)

    out_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_max_time = models.DateTimeField(null=True)
    out_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    out_temp_min_time = models.DateTimeField(null=True)

    in_temp_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_max_time = models.DateTimeField(null=True)
    in_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    in_temp_min_time = models.DateTimeField(null=True)
    
    heat_index_max = models.DecimalField(max_digits=3, decimal_places=1, null=True) # check data type
    heat_index_max_time = models.DateTimeField(null=True)

    windchill_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_max_time = models.DateTimeField(null=True)
    windchill_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    windchill_min_time = models.DateTimeField(null=True)

    dewpoint_max = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_max_time = models.DateTimeField(null=True)
    dewpoint_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    dewpoint_min_time = models.DateTimeField(null=True)

    # humidity_sum/humidity_duration ???

    humidity_max = models.SmallIntegerField(null=True)
    humidity_max_time = models.DateTimeField(null=True)
    humidity_min = models.SmallIntegerField(null=True)
    humidity_min_time = models.SmallIntegerField(null=True)

    in_humidity_max = models.SmallIntegerField(null=True)
    in_humidity_max_time = models.DateTimeField(null=True)
    in_humidity_min = models.SmallIntegerField(null=True)
    in_humidity_min_time = models.SmallIntegerField(null=True)

    soil_temp_min = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    soil_temp_in_time = models.DateTimeField(null=True)

    barometer_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_sum = models.IntegerField(null=True)
    barometer_duration = models.IntegerField(null=True)

    barometer_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_max_time = models.DateTimeField(null=True)
    barometer_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    barometer_min_time = models.DateTimeField(null=True)

    rain_avg = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_sum = models.IntegerField(null=True)  # ok to use int here instead of n(5,1) or 6,1 ?
    rain_duration = models.IntegerField(null=True)
    rain_rate_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)  # check data type
    rain_rate_max_time = models.DateTimeField(null=True)

    # rain_sum_1h...24h ??? to be decided...

    wind_speed_avg = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    wind_speed_sum = models.IntegerField(null=True)
    win_speed_duration = models.IntegerField(null=True)

    wind_dir_avg = models.SmallIntegerField(null=True)
    wind_dir_sum = models.IntegerField(null=True)
    wind_dir_duration = models.IntegerField(null=True)

    wind_gust = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    wind_gust_dir = models.SmallIntegerField(null=True)
    wind_gust_time = models.DateTimeField(null=True)

    # windRms windVecAvg, windVerDir ????

    uv_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_max_time = models.DateTimeField(null=True)
    uv_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    uv_min_time = models.DateTimeField(null=True)

    # uv_indixe = models.SmallIntegerField(null=True)
    etp_max = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_max_time = models.DateTimeField(null=True)
    etp_min = models.DecimalField(max_digits=5, decimal_places=3, null=True)  # check datatype
    etp_min_time = models.DateTimeField(null=True)

    rx_avg = models.SmallIntegerField(null=True)
    rx_sum = models.IntegerField(null=True)
    rx_duration = models.IntegerField(null=True)
    rx_max = models.SmallIntegerField(null=True)
    rx_max_time = models.DateTimeField(null=True)
    rx_min = models.SmallIntegerField(null=True)
    rx_min_time = models.DateTimeField(null=True)

    voltage_avg = models.SmallIntegerField(null=True)
    voltage_sum = models.IntegerField(null=True)
    voltage_duration = models.IntegerField(null=True)
    voltage_max = models.SmallIntegerField(null=True)
    voltage_max_time = models.DateTimeField(null=True)
    voltage_min = models.SmallIntegerField(null=True)
    voltage_min_time = models.DateTimeField(null=True)

    # solar_radiation = models.SmallIntegerField(null=True)  # check data type
    # insolation_duration = models.SmallIntegerField(null=True) # check data type, and what is that measure...
 
    def __str__(self):
        return "agg_global id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_global"

