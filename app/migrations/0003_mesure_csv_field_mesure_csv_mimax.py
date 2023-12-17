# Generated by Django 4.2.6 on 2023-12-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_init_timescaledb'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesure',
            name='csv_field',
            field=models.CharField(default=None, max_length=20, null=True, verbose_name='nom colonne csv'),
        ),
        migrations.AddField(
            model_name='mesure',
            name='csv_mimax',
            field=models.JSONField(default=dict, verbose_name='Nom champs min, minTime, max, maxTime maxDir'),
        ),
    ]
