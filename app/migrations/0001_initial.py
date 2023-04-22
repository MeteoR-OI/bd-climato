# Generated by Django 4.1.7 on 2023-04-22 20:28

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', app.models.DateTimeFieldNoTZ(max_length=30, verbose_name="date'")),
                ('timeend', app.models.DateTimeFieldNoTZ(max_length=30, verbose_name="date'")),
                ('text', models.CharField(max_length=100, verbose_name='source')),
                ('tags', models.CharField(max_length=100, verbose_name='source')),
            ],
            options={
                'db_table': 'annotations',
            },
        ),
        migrations.CreateModel(
            name='Exclusion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_dat', app.models.DateTimeFieldNoTZ(default='1900-01-01T00:00:00', max_length=20, verbose_name='Datetime locale début exclusion')),
                ('stop_dat', app.models.DateTimeFieldNoTZ(default='2100-12-31T23:59:59', max_length=20, verbose_name='Datetime locale fin exclusion')),
                ('value', models.JSONField(default=dict, verbose_name='Exclusion')),
            ],
            options={
                'db_table': 'exclusions',
            },
        ),
        migrations.CreateModel(
            name='Extreme',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_local', models.DateField(verbose_name="date locale de l'extrême")),
                ('min', models.FloatField(null=True, verbose_name='valeur minimum')),
                ('min_time', app.models.DateTimeFieldNoTZ(null=True, verbose_name='date du minimum')),
                ('max', models.FloatField(null=True, verbose_name='valeur maximum')),
                ('max_time', app.models.DateTimeFieldNoTZ(null=True, verbose_name='date du maximum')),
                ('max_dir', models.SmallIntegerField(null=True, verbose_name='direction du maximum')),
            ],
            options={
                'db_table': 'extremes',
            },
        ),
        migrations.CreateModel(
            name='HistoExtremes',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('src_min_obs_id', models.BigIntegerField(null=True, verbose_name='obs_id source')),
                ('src_max_obs_id', models.BigIntegerField(null=True, verbose_name='obs_id source')),
                ('target_x_id', models.BigIntegerField(verbose_name='extreme_id modifiée')),
            ],
            options={
                'db_table': 'histo_extreme',
            },
        ),
        migrations.CreateModel(
            name='HistoObs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('src_obs_id', models.BigIntegerField(verbose_name='obs_id source')),
                ('target_obs_id', models.BigIntegerField(verbose_name='obs_id modifiée')),
            ],
            options={
                'db_table': 'histo_obs',
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_utc', app.models.DateTimeFieldNoTZ(max_length=30, verbose_name='date')),
                ('source', models.CharField(max_length=100, verbose_name='source')),
                ('level', models.CharField(max_length=20, verbose_name='niveau')),
                ('reason', models.TextField(verbose_name='raison')),
                ('details', models.JSONField(default=dict, verbose_name='details')),
                ('active', models.BooleanField(default=True, null=True, verbose_name='active')),
            ],
            options={
                'db_table': 'incidents',
            },
        ),
        migrations.CreateModel(
            name='Mesure',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nom de la mesure')),
                ('json_input', models.CharField(max_length=20, verbose_name='Clé utilisée dans le json')),
                ('json_input_bis', models.CharField(max_length=20, null=True, verbose_name='Autre clé utilisée dans le json')),
                ('archive_col', models.CharField(max_length=20, verbose_name='nom colonne table weewx.archive')),
                ('archive_table', models.CharField(default=None, max_length=20, null=True, verbose_name='nom table weewx.archive')),
                ('field_dir', models.SmallIntegerField(null=True, verbose_name='id de la mesure wind dans table weewx.archive')),
                ('val_deca', models.SmallIntegerField(default=0, null=True, verbose_name='Décalage mesure')),
                ('max', models.BooleanField(default=True, null=True, verbose_name='Calcul des max')),
                ('max_deca', models.SmallIntegerField(default=0, null=True, verbose_name='Décalage du max')),
                ('min', models.BooleanField(default=True, null=True, verbose_name='Calcul des min')),
                ('min_deca', models.SmallIntegerField(default=0, null=True, verbose_name='Décalage du min')),
                ('is_avg', models.BooleanField(default=True, null=True, verbose_name='Calcul de moyenne')),
                ('is_wind', models.BooleanField(default=False, null=True, verbose_name='Calcul du wind_dir')),
                ('omm_link', models.SmallIntegerField(default=0, null=True, verbose_name='Lien entre mesure OMM et mesure de base')),
                ('allow_zero', models.BooleanField(default=True, null=True, verbose_name='Zero est une valeur valide')),
                ('is_hourly', models.BooleanField(default=False, null=True, verbose_name='Must be agregated by hour(s) or more, not less')),
            ],
            options={
                'db_table': 'mesures',
            },
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('meteor', models.CharField(max_length=10, verbose_name='Code MeteoR.OI')),
                ('delta_timezone', models.SmallIntegerField(default=0, null=True, verbose_name='delta heure locale et UTC')),
                ('meteofr', models.CharField(default='', max_length=10, null=True, verbose_name='Code Meteo France')),
                ('title', models.CharField(default='', max_length=50, null=True, verbose_name='Nom clair de la station')),
                ('owner', models.CharField(default='', max_length=50, null=True, verbose_name='Propriétaire')),
                ('email', models.CharField(default='', max_length=50, null=True, verbose_name='E-Mail')),
                ('phone', models.CharField(default='', max_length=50, null=True, verbose_name='Téléphone')),
                ('address', models.CharField(default='', max_length=50, null=True, verbose_name='Addresse')),
                ('zip', models.CharField(default='', max_length=10, null=True, verbose_name='Code Postal')),
                ('city', models.CharField(default='', max_length=50, null=True, verbose_name='Ville')),
                ('country', models.CharField(default='', max_length=50, null=True, verbose_name='Payse')),
                ('altitude', models.FloatField(default=0, null=True, verbose_name='Altitude')),
                ('lat', models.FloatField(default=0, null=True, verbose_name='Latitude')),
                ('long', models.FloatField(default=0, null=True, verbose_name='Longitude')),
                ('start_dat', app.models.DateTimeFieldNoTZ(default='1900-01-01T00:00:00', null=True, verbose_name="Datetime locale d'activation")),
                ('stop_dat', app.models.DateTimeFieldNoTZ(default='2100-12-31T23:59:59', null=True, verbose_name='Datetime locale de désactivation')),
                ('comment', models.TextField(default='', null=True)),
                ('last_obs_date', app.models.DateTimeFieldNoTZ(default='2000-01-01T00:00:00', null=True, verbose_name='Datetime locale de derniere reception de donnees')),
                ('last_obs_id', models.BigIntegerField(default=0, null=True, verbose_name='ID obs de la derniere reception de donnees')),
                ('last_extremes_date', app.models.DateTimeFieldNoTZ(default='2000-01-01T00:00:00', null=True, verbose_name='Datetime locale de dernier record')),
                ('last_extremes_id', models.BigIntegerField(default=0, null=True, verbose_name='ID du dernier record')),
                ('load_json', models.BooleanField(default=False, null=True, verbose_name='load json status')),
            ],
            options={
                'db_table': 'postes',
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name="id de l'observation")),
                ('date_local', app.models.DateTimeFieldNoTZ(verbose_name='datetime locale fin période observation')),
                ('date_utc', app.models.DateTimeFieldNoTZ(verbose_name='datetime UTC fin période observation')),
                ('duration', models.SmallIntegerField(default=0, null=True, verbose_name='durée période, seulement pour les obs principales')),
                ('barometer', models.FloatField(null=True, verbose_name='pression niveau mer')),
                ('barometer_omm', models.FloatField(null=True, verbose_name='pression niveau mer OMM')),
                ('dewpoint', models.FloatField(null=True, verbose_name='point de rosée')),
                ('etp', models.FloatField(null=True, verbose_name='somme etp')),
                ('extra_humid1', models.FloatField(null=True, verbose_name='extra humidité 1')),
                ('extra_humid2', models.FloatField(null=True, verbose_name='extra humidité 2')),
                ('extra_temp1', models.FloatField(null=True, verbose_name='extra temperature 1')),
                ('extra_temp2', models.FloatField(null=True, verbose_name='extra temperature 2')),
                ('extra_temp3', models.FloatField(null=True, verbose_name='extra temperature 3')),
                ('hail', models.FloatField(null=True, verbose_name='hail')),
                ('hail_rate', models.FloatField(null=True, verbose_name='hail rate')),
                ('heatindex', models.FloatField(null=True, verbose_name='heatindex')),
                ('heating_temp', models.FloatField(null=True, verbose_name='heating temp')),
                ('in_humidity', models.FloatField(null=True, verbose_name='humidité intérieure')),
                ('in_temp', models.FloatField(null=True, verbose_name='température intérieure')),
                ('leaf_temp1', models.FloatField(null=True, verbose_name='temp des feuilles no 1')),
                ('leaf_temp2', models.FloatField(null=True, verbose_name='temp des feuilles no 2')),
                ('leaf_wet1', models.FloatField(null=True, verbose_name='humidité des feuilles no 1')),
                ('leaf_wet2', models.FloatField(null=True, verbose_name='humidité des feuilles no 2')),
                ('out_humidity', models.FloatField(null=True, verbose_name='humidité')),
                ('out_humidity_omm', models.FloatField(null=True, verbose_name='humidité OMM')),
                ('out_temp', models.FloatField(null=True, verbose_name='température extérieure')),
                ('out_temp_omm', models.FloatField(null=True, verbose_name='température OMM extérieure')),
                ('pressure', models.FloatField(null=True, verbose_name='pression station')),
                ('radiation', models.FloatField(null=True, verbose_name='radiation')),
                ('rain', models.FloatField(null=True, verbose_name='pluie')),
                ('rain_omm', models.FloatField(null=True, verbose_name='pluie OMM')),
                ('rain_rate', models.FloatField(null=True, verbose_name='rain_rate')),
                ('rx', models.FloatField(null=True, verbose_name='taux reception station')),
                ('soil_moist1', models.FloatField(null=True, verbose_name='humidité du sol niveau du sol')),
                ('soil_moist2', models.FloatField(null=True, verbose_name='humidité du sol niveau 2')),
                ('soil_moist3', models.FloatField(null=True, verbose_name='humidité du sol niveau 3')),
                ('soil_moist4', models.FloatField(null=True, verbose_name='humidité du sol niveau 4')),
                ('soil_temp1', models.FloatField(null=True, verbose_name='température du sol niveau du sol')),
                ('soil_temp2', models.FloatField(null=True, verbose_name='température du sol niveau 2')),
                ('soil_temp3', models.FloatField(null=True, verbose_name='température du sol niveau 3')),
                ('soil_temp4', models.FloatField(null=True, verbose_name='température du sol niveau 4')),
                ('uv', models.FloatField(null=True, verbose_name='indice UV')),
                ('voltage', models.FloatField(null=True, verbose_name='voltage')),
                ('wind', models.FloatField(null=True, verbose_name='vitesse moyenne du vent sur la période')),
                ('wind_dir', models.FloatField(null=True, verbose_name='direction moyenne du vent sur la période')),
                ('wind_gust', models.FloatField(null=True, verbose_name='rafale max')),
                ('wind_gust_dir', models.FloatField(null=True, verbose_name='direction de la rafale max')),
                ('wind10', models.FloatField(null=True, verbose_name='vent moyen sur 10')),
                ('wind10_dir', models.FloatField(null=True, verbose_name='direction moyenne du vent sur 10 mn')),
                ('wind10_omm', models.FloatField(null=True, verbose_name='vent moyen 10 mn OMM')),
                ('windchill', models.FloatField(null=True, verbose_name='windchill')),
                ('j', models.JSONField(default=dict, null=True, verbose_name='données autres')),
                ('qa_modifications', models.IntegerField(default=0, null=True, verbose_name='qa_modifications')),
                ('qa_incidents', models.IntegerField(default=0, null=True, verbose_name='qa_incidents')),
                ('qa_check_done', models.BooleanField(default=False, null=True, verbose_name='qa_check_done')),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.poste')),
            ],
            options={
                'db_table': 'obs',
            },
        ),
        migrations.AddIndex(
            model_name='histoobs',
            index=models.Index(fields=['src_obs_id', 'target_obs_id'], name='histo_obs_target'),
        ),
        migrations.AddIndex(
            model_name='histoobs',
            index=models.Index(fields=['target_obs_id', 'src_obs_id'], name='histo_obs_src'),
        ),
        migrations.AddConstraint(
            model_name='histoobs',
            constraint=models.UniqueConstraint(fields=('src_obs_id', 'target_obs_id'), name='unique_histo_obs_mapping'),
        ),
        migrations.AddIndex(
            model_name='histoextremes',
            index=models.Index(fields=['target_x_id', 'id'], name='histo_x_src'),
        ),
        migrations.AddIndex(
            model_name='histoextremes',
            index=models.Index(condition=models.Q(('src_min_obs_id__isnull', False)), fields=['src_min_obs_id', 'target_x_id'], name='histo_x_target_min'),
        ),
        migrations.AddIndex(
            model_name='histoextremes',
            index=models.Index(condition=models.Q(('src_max_obs_id__isnull', False)), fields=['src_max_obs_id', 'target_x_id'], name='histo_x_target_max'),
        ),
        migrations.AddField(
            model_name='extreme',
            name='mesure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.mesure'),
        ),
        migrations.AddField(
            model_name='extreme',
            name='poste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.poste'),
        ),
        migrations.AddField(
            model_name='exclusion',
            name='poste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.poste'),
        ),
        migrations.AddIndex(
            model_name='observation',
            index=models.Index(fields=['poste_id', '-date_local'], name='obs_pid'),
        ),
        migrations.AddIndex(
            model_name='extreme',
            index=models.Index(fields=['poste_id', '-date_local'], name='extremes_pid'),
        ),
    ]
