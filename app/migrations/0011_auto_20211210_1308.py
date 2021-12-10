# Generated by Django 3.2.9 on 2021-12-10 13:08

import app.models
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20211210_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclusion',
            name='value',
            field=app.models.DateJSONField(default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Exclusion'),
        ),
        migrations.AlterField(
            model_name='typeinstrument',
            name='model_value',
            field=app.models.DateJSONField(default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Model Json'),
        ),
        migrations.AlterField(
            model_name='typeinstrument',
            name='name',
            field=models.CharField(max_length=10, verbose_name='Type Instrument'),
        ),
    ]
