# Generated by Django 3.2.9 on 2021-12-09 18:27

import app.models
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_observation_stop_dat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='agg_start_dat',
            field=app.models.DateCharField(default='1900-01-01T00:00:00', max_length=20, verbose_name='date début période'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='duration',
            field=models.IntegerField(default=0, verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='j',
            field=app.models.DateJSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Json data'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='j_agg',
            field=app.models.DateJSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Json pre-aggregated data'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stop_dat',
            field=app.models.DateCharField(max_length=20, verbose_name='date de fin de période'),
        ),
    ]