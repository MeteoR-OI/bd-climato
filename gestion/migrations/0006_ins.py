# Generated by Django 2.0.6 on 2018-07-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0005_commune'),
    ]

    operations = [
        migrations.CreateModel(
            name='INS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RR5MN', models.IntegerField(null=True)),
            ],
        ),
    ]
