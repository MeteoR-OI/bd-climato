# Generated by Django 4.1.7 on 2023-05-04 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_poste_pause'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poste',
            old_name='pause',
            new_name='pause_json',
        ),
    ]
