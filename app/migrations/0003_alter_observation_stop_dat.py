# Generated by Django 3.2.9 on 2021-12-09 17:48

import app.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_observation_stop_dat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='stop_dat',
            field=app.models.DateCharField(max_length=20, verbose_name='stop date, date de la mesure'),
        ),
    ]
