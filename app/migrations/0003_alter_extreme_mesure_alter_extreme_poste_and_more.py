# Generated by Django 4.1.7 on 2023-03-31 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_init_timescaledb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extreme',
            name='mesure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.mesure'),
        ),
        migrations.AlterField(
            model_name='extreme',
            name='poste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.poste'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='poste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.poste'),
        ),
    ]
