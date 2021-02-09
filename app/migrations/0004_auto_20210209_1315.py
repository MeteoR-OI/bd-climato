# Generated by Django 3.1.5 on 2021-02-09 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210209_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agg_hour',
            name='j',
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_avg',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_max',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_min',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='barometer_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='dewpoint_max',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='dewpoint_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='dewpoint_min',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='dewpoint_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='etp_max',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='etp_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='etp_min',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='etp_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='heat_index_max',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='heat_index_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='humidity_max',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='humidity_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='humidity_min',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='humidity_min_time',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_humidity_max',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_humidity_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_humidity_min',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_humidity_min_time',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_temp_max',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_temp_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_temp_min',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='in_temp_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_avg',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_max',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_min',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='out_temp_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rain_avg',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rain_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rain_rate_max',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rain_rate_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rain_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_avg',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_max',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_min',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='rx_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='soil_temp_in_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='soil_temp_min',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='uv_max',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='uv_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='uv_min',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='uv_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_avg',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_max',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_min',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='voltage_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='win_speed_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_dir_avg',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_dir_duration',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_dir_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_gust',
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_gust_dir',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_gust_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_speed_avg',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='wind_speed_sum',
            field=models.IntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='windchill_max',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='windchill_max_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='windchill_min',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='agg_hour',
            name='windchill_min_time',
            field=models.DateTimeField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='observation',
            name='rx',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='observation',
            name='voltage',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
    ]
