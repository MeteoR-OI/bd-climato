# Generated by Django 3.1.5 on 2021-01-17 14:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='COMMUNE',
            fields=[
                ('NOMCOMMUNE', models.CharField(default=None, max_length=25)),
                ('CP', models.IntegerField(default=None, primary_key=True, serialize=False, unique=True, verbose_name='Code postal')),
            ],
            options={
                'verbose_name': 'Commune',
            },
        ),
        migrations.CreateModel(
            name='EVENEMENTS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NOM_EVENEMENT', models.CharField(max_length=100, null=True)),
                ('TYPE_EVENEMENT', models.CharField(max_length=100, null=True)),
                ('DEBUT', models.DateTimeField(null=True)),
                ('FIN', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PAYS',
            fields=[
                ('CODPAYS', models.IntegerField(default=None, primary_key=True, serialize=False)),
                ('NOMPAYS', models.CharField(default=None, max_length=20)),
            ],
            options={
                'verbose_name': 'Pays',
            },
        ),
        migrations.CreateModel(
            name='POSTE',
            fields=[
                ('NUM_POSTE', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Numero de poste')),
                ('CP', models.IntegerField(default=None, verbose_name='Code postal')),
                ('CODE_POSTE', models.CharField(default=None, max_length=50, unique=True)),
                ('REF_MF', models.CharField(default=None, max_length=10, null=True, unique=True)),
                ('NOM', models.CharField(default=None, max_length=50, verbose_name='Nom du poste (ex : NDLP)')),
                ('COMMUNE', models.CharField(default=None, max_length=60, verbose_name='Nom de lacommune')),
                ('LAT', models.FloatField(default=None)),
                ('LON', models.FloatField(default=None)),
                ('ALT', models.FloatField(default=None, verbose_name='Altitude du poste en m')),
                ('POS', models.IntegerField(default=None, verbose_name='Personne physique(1) - Morale (2)')),
                ('AUT', models.IntegerField(default=None, verbose_name='Autorisation de stockage/diffusion')),
                ('PROP', models.CharField(default=None, max_length=20, verbose_name='Nom du propriétaire/entreprise')),
                ('DATEOUV', models.DateTimeField(default=None)),
                ('DATEFERM', models.DateTimeField(blank=True, default=None, null=True)),
                ('MAINT', models.IntegerField(default=None, null=True, verbose_name='Code maintenance (tableau)')),
                ('TYPE', models.CharField(default=None, max_length=20, verbose_name='Modèle de station')),
                ('TYPINFO', models.CharField(default=None, max_length=20, verbose_name='Type de donnees (route,agricole,pédagogique,..)')),
                ('ADRESSE', models.CharField(default=None, max_length=100)),
                ('LIEU_DIT', models.CharField(default=None, max_length=30, null=True)),
                ('MEL', models.CharField(default=None, max_length=40, null=True)),
                ('TEL', models.CharField(default=None, max_length=10, null=True)),
                ('COMM', models.TextField(default=None, null=True)),
                ('PDT', models.IntegerField(default=5, verbose_name="Pas de temps d'envoie (min)")),
                ('INIT', models.IntegerField(default=None, null=True, verbose_name="Etat d'initialisation")),
            ],
            options={
                'db_table': 'poste',
            },
        ),
        migrations.CreateModel(
            name='RECMENS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PARAM', models.CharField(max_length=25, null=True)),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now)),
                ('NUM_MOIS', models.IntegerField(null=True, verbose_name='13 = record mini annuel, 14 = record maxi annuel')),
                ('DATDEB', models.DateTimeField(null=True)),
                ('DATFIN', models.DateTimeField(null=True)),
                ('RECORD', models.FloatField(null=True)),
                ('DATERECORD', models.DateTimeField(null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'record_mois',
            },
        ),
        migrations.CreateModel(
            name='Q',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATJ', models.DateField(default=django.utils.timezone.now)),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now)),
                ('RR', models.FloatField(default=None, null=True)),
                ('DRR', models.FloatField(default=None, null=True, verbose_name='Durée de la précipitation en min')),
                ('STATUS_DRR', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('TN', models.FloatField(default=None, null=True)),
                ('HTN', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de TN')),
                ('TX', models.FloatField(default=None, null=True)),
                ('HTX', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de TX')),
                ('TM', models.FloatField(default=None, null=True)),
                ('TAMPLI', models.FloatField(null=True)),
                ('DG', models.IntegerField(default=None, null=True, verbose_name='Duree du gel en min')),
                ('PMERM', models.FloatField(default=None, null=True)),
                ('PMERMIN', models.FloatField(default=None, null=True)),
                ('FXY', models.FloatField(default=None, null=True, verbose_name='Valeur max de FF dans la journee')),
                ('DXY', models.FloatField(default=None, null=True, verbose_name='Direction de FXY')),
                ('HXY', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de FXY')),
                ('FXI', models.FloatField(default=None, null=True, verbose_name='Rafales max de FF dans la journee')),
                ('DXI', models.FloatField(default=None, null=True, verbose_name='Direction de FXI')),
                ('HXI', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de FXI')),
                ('UM', models.FloatField(default=None, null=True)),
                ('UN', models.FloatField(default=None, null=True, verbose_name='Humidite minimale dans la journee')),
                ('HUN', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de UN')),
                ('UX', models.FloatField(default=None, null=True, verbose_name="Humidite maximale dans l'heure")),
                ('HUX', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de UX')),
                ('ETPM', models.FloatField(default=None, null=True)),
                ('HFM', models.FloatField(default=None, null=True)),
                ('HFMX', models.FloatField(default=None, null=True)),
                ('HFMN', models.FloatField(default=None, null=True)),
                ('HSM', models.FloatField(default=None, null=True)),
                ('HSMX', models.FloatField(default=None, null=True)),
                ('HSMN', models.FloatField(default=None, null=True)),
                ('TS', models.FloatField(default=None, null=True)),
                ('TSX', models.FloatField(default=None, null=True)),
                ('TSN', models.FloatField(default=None, null=True)),
                ('INST', models.IntegerField(default=None, null=True, verbose_name="Duree d'insolation quotidienne (min)")),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'agg_jour',
            },
        ),
        migrations.CreateModel(
            name='POSTE_EVENEMENTS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EVENEMENTS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.evenements')),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='PANNE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DEBUT', models.DateTimeField(null=True)),
                ('FIN', models.DateTimeField(null=True)),
                ('CAPTEUR', models.CharField(max_length=25, null=True)),
                ('COMM', models.TextField(null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='MENSQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATJ', models.DateField(default=django.utils.timezone.now)),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now)),
                ('RR', models.FloatField(default=None, null=True)),
                ('STATUS_DRR', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('RRAB', models.FloatField(default=None, null=True, verbose_name='Precipitation maxi en 24h')),
                ('STATUS_RRAB', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('RRABDAT', models.DateTimeField(default=None, null=True)),
                ('NBJRR1', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 1mm')),
                ('NBJRR5', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 5mm')),
                ('NBJRR10', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 10mm')),
                ('NBJRR30', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 30mm')),
                ('NBJRR50', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 50mm')),
                ('NBJRR100', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 100mm')),
                ('PMERM', models.FloatField(default=None, null=True)),
                ('PMERMINAB', models.FloatField(default=None, null=True)),
                ('PMERMINABDAT', models.DateTimeField(default=None, null=True)),
                ('TX', models.FloatField(default=None, null=True, verbose_name='Moyenne des TX du mois')),
                ('TXAB', models.FloatField(default=None, null=True, verbose_name='TX max du mois')),
                ('TXABDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TX max du mois')),
                ('TXMIN', models.FloatField(default=None, null=True, verbose_name='TX min du mois')),
                ('TXMINDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TX min du mois')),
                ('NBJTX0', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 0')),
                ('NBJTX25', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 25')),
                ('NBJTX30', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 30')),
                ('NBJTX35', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 35')),
                ('NBJTXI20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 20')),
                ('NBJTXI27', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 27')),
                ('NBJTX32', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 32')),
                ('TN', models.FloatField(default=None, null=True, verbose_name='Moyenne des TN du mois')),
                ('TNAB', models.FloatField(default=None, null=True, verbose_name='TN min du mois')),
                ('TNDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TN min du mois')),
                ('TNMAX', models.FloatField(default=None, null=True, verbose_name='TN max du mois')),
                ('TNMAXDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TN max du mois')),
                ('NBJTN5', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à -5')),
                ('NBJTNI10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 10')),
                ('NBJTNI15', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 15')),
                ('NBJTNI20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 20')),
                ('NBJTNS20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est sup à 20')),
                ('NBJTNS25', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est sup à 25')),
                ('NBJGELEE', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 0')),
                ('UNAB', models.FloatField(default=None, null=True, verbose_name='Humidite relative minimale du mois')),
                ('UNABDAT', models.DateTimeField(default=None, null=True, verbose_name="Date de l'Humidite relative minimale du mois")),
                ('UXAB', models.FloatField(default=None, null=True, verbose_name='Humidite relative maximale du mois')),
                ('UXABDAT', models.DateTimeField(default=None, null=True, verbose_name="Date de l'humidite relative maximale du mois")),
                ('UMM', models.FloatField(default=None, null=True, verbose_name='Moyenne des humidites relatives du mois')),
                ('FXIAB', models.FloatField(default=None, null=True, verbose_name='Rafale maxi du mois')),
                ('DXIAB', models.FloatField(default=None, null=True, verbose_name='Direction de la rafale maxi du mois')),
                ('FXIDAT', models.DateTimeField(default=None, null=True, verbose_name='Date la rafale maxi du mois')),
                ('NBJFF10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXI est sup à 10m/s')),
                ('NBJFF16', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXI est sup à 16m/s')),
                ('NBJFF28', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXI est sup à 28m/s')),
                ('FXYAB', models.FloatField(default=None, null=True, verbose_name='FXY max du mois')),
                ('DXYAB', models.FloatField(default=None, null=True, verbose_name='Direction du FXYAB du mois')),
                ('FXYABDAT', models.DateTimeField(default=None, null=True, verbose_name='Date du FXYAB du moise')),
                ('NBJFXY8', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 8m/s')),
                ('NBJFXY10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 10m/s')),
                ('NBJFXY15', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 15m/s')),
                ('INST', models.IntegerField(default=None, null=True, verbose_name="Duree d'insolation quotidienne moyenne (min, default=None)")),
                ('HFM', models.FloatField(default=None, null=True)),
                ('HFX', models.FloatField(default=None, null=True)),
                ('HFN', models.FloatField(default=None, null=True)),
                ('HSM', models.FloatField(default=None, null=True)),
                ('HSX', models.FloatField(default=None, null=True)),
                ('HSN', models.FloatField(default=None, null=True)),
                ('TSM', models.FloatField(default=None, null=True)),
                ('TSX', models.FloatField(default=None, null=True)),
                ('TSN', models.FloatField(default=None, null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'agg_mois',
            },
        ),
        migrations.CreateModel(
            name='MAINTENANCE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CAPTEUR', models.CharField(max_length=25)),
                ('DATMAINT', models.DateTimeField(null=True, verbose_name='Date de la derniere maintenance')),
                ('DATPMAINT', models.DateTimeField(null=True, verbose_name='Date de la prochaine maintenance')),
                ('TYPE', models.CharField(max_length=100, null=True, verbose_name='Type de maintenance')),
                ('IMPORTANCE', models.IntegerField(null=True, verbose_name='1 si alteration de la mesure - 2 aucune alteration')),
                ('ACTEUR', models.CharField(max_length=15, null=True, verbose_name="Personne s'occupant de la maintenance")),
                ('TELACTEUR', models.IntegerField(null=True)),
                ('COMM', models.CharField(max_length=100, null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='INSTRUMENT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CAPTEUR', models.CharField(max_length=25, verbose_name='Capteur')),
                ('DATDEB', models.DateTimeField(blank=True, help_text='AAAA-MM-JJ HH:MM', null=True, verbose_name='Date et heure de la mise en service')),
                ('DATFIN', models.DateTimeField(blank=True, null=True)),
                ('MODELE', models.CharField(blank=True, max_length=25, null=True, verbose_name='Version et modele du capteur')),
                ('HAUTEUR', models.FloatField(blank=True, help_text='(en mètres)', null=True, verbose_name='Hauteur')),
                ('VENTILATION', models.IntegerField(blank=True, choices=[(0, 'Non ventilé'), (1, 'Ventilé')], null=True, verbose_name='Ventilation du capteur ')),
                ('SEUILMIN', models.FloatField(blank=True, null=True, verbose_name='Seuil min')),
                ('SEUILMAX', models.FloatField(blank=True, null=True, verbose_name='Seuil max')),
                ('PRECISION', models.FloatField(blank=True, null=True, verbose_name='Précision')),
                ('QUALITE', models.CharField(blank=True, max_length=2, null=True, verbose_name="Qualite du site d'installation (voir classification)")),
                ('PASDETEMPS', models.FloatField(blank=True, null=True, verbose_name='Intervalle de mesure en s')),
                ('TYPE_TERRAIN', models.CharField(blank=True, max_length=15, null=True, verbose_name="Type de terrain sur l'implantation du capteur")),
                ('UNITE', models.CharField(blank=True, max_length=10, null=True, verbose_name='Unite de mesure')),
                ('COMM', models.CharField(blank=True, max_length=100, null=True, verbose_name='Commentaires')),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='INSTAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATJ', models.DateTimeField(verbose_name='AAAA-MM-JJ HH-MM de la mesure')),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now, verbose_name='AAAA-MM-JJ HH-MM de la derniere modification')),
                ('RR', models.FloatField(default=None, null=True)),
                ('RRI', models.FloatField(default=None, null=True, verbose_name='Intensité max des precipitations')),
                ('FF', models.FloatField(default=None, null=True)),
                ('DD', models.FloatField(default=None, null=True)),
                ('FXI', models.FloatField(default=None, null=True)),
                ('DXI', models.FloatField(default=None, null=True)),
                ('T', models.FloatField(default=None, null=True)),
                ('TD', models.FloatField(default=None, null=True)),
                ('U', models.FloatField(default=None, null=True)),
                ('PMER', models.FloatField(default=None, null=True)),
                ('UV', models.FloatField(default=None, null=True, verbose_name='Indice UV')),
                ('RAD', models.FloatField(default=None, null=True)),
                ('IC', models.FloatField(default=None, null=True, verbose_name='Indice de chaleur')),
                ('WINDCHILL', models.FloatField(default=None, null=True)),
                ('ETP', models.FloatField(default=None, null=True, verbose_name='Evapotranspiration')),
                ('HF', models.FloatField(default=None, null=True, verbose_name='Humidite du feuillage')),
                ('HS', models.FloatField(default=None, null=True, verbose_name='Humidite du sol')),
                ('TS', models.FloatField(default=None, null=True, verbose_name='Temperature du sol')),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'mesure',
            },
        ),
        migrations.CreateModel(
            name='HISTPOST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LIEU_DIT', models.CharField(max_length=30, null=True)),
                ('DATDEB', models.DateTimeField(null=True)),
                ('DATFIN', models.DateTimeField(null=True)),
                ('LAT', models.FloatField()),
                ('LON', models.FloatField()),
                ('ALT', models.FloatField(verbose_name='Altitude du poste en m')),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now)),
                ('PROP', models.CharField(max_length=20, verbose_name='Nom du propriétaire/entreprise')),
                ('ADRESSE', models.CharField(max_length=100)),
                ('MEL', models.CharField(max_length=40, null=True)),
                ('TEL', models.CharField(max_length=10, null=True)),
                ('COMM', models.TextField(null=True)),
                ('COMMUNE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.commune')),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='HISTMAINT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATMAINT', models.DateTimeField(null=True)),
                ('TYPE', models.CharField(max_length=100, null=True)),
                ('CAPT', models.CharField(max_length=25, null=True)),
                ('ACTEUR', models.CharField(max_length=25, null=True)),
                ('COMM', models.CharField(max_length=100, null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
        ),
        migrations.CreateModel(
            name='H',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATJ', models.DateTimeField(default=django.utils.timezone.now, verbose_name='AAAA-MM-JJ HH-MM de la mesure')),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now, verbose_name='AAAA-MM-JJ HH-MM de la derniere modification')),
                ('RR1', models.FloatField(default=None, null=True)),
                ('DRR1', models.IntegerField(default=None, null=True, verbose_name='Durée de la précipitation en min')),
                ('STATUS_DRR1', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('RRI', models.FloatField(default=None, null=True)),
                ('HRRI', models.DateTimeField(default=None, null=True)),
                ('FF', models.FloatField(default=None, null=True, verbose_name='Force du vent moyenné sur 10 dernieres min')),
                ('DD', models.FloatField(default=None, null=True)),
                ('FXY', models.FloatField(default=None, null=True, verbose_name="Valeur max de FF dans l'heure")),
                ('DXY', models.FloatField(default=None, null=True, verbose_name='Direction de FXY')),
                ('HXY', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de FXY')),
                ('FXI', models.FloatField(default=None, null=True, verbose_name="Rafales max de FF dans l'heure")),
                ('DXI', models.FloatField(default=None, null=True, verbose_name='Direction de FXI')),
                ('HXI', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de FXI')),
                ('T', models.FloatField(default=None, null=True)),
                ('TD', models.FloatField(default=None, null=True)),
                ('TN', models.FloatField(default=None, null=True)),
                ('HTN', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de TN')),
                ('TX', models.FloatField(default=None, null=True)),
                ('HTX', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de TX')),
                ('U', models.FloatField(default=None, null=True)),
                ('UN', models.FloatField(default=None, null=True, verbose_name="Humidite minimale dans l'heure")),
                ('HUN', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de UN')),
                ('UX', models.FloatField(default=None, null=True, verbose_name="Humidite maximale dans l'heure")),
                ('HUX', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de UX')),
                ('PMER', models.FloatField(default=None, null=True)),
                ('PMERMIN', models.FloatField(default=None, null=True)),
                ('HPERMIN', models.DateTimeField(default=None, null=True, verbose_name='AAAA MM JJ HH MM de PMERMIN')),
                ('UV', models.IntegerField(default=None, null=True)),
                ('RAD', models.FloatField(default=None, null=True)),
                ('IC', models.FloatField(default=None, null=True)),
                ('WINDCHILL', models.FloatField(default=None, null=True)),
                ('ETP', models.FloatField(default=None, null=True)),
                ('ETPX', models.FloatField(default=None, null=True)),
                ('ETPN', models.FloatField(default=None, null=True)),
                ('HF', models.FloatField(default=None, null=True)),
                ('HFX', models.FloatField(default=None, null=True)),
                ('HFN', models.FloatField(default=None, null=True)),
                ('HS', models.FloatField(default=None, null=True)),
                ('HSX', models.FloatField(default=None, null=True)),
                ('HSN', models.FloatField(default=None, null=True)),
                ('TS', models.FloatField(default=None, null=True)),
                ('TSX', models.FloatField(default=None, null=True)),
                ('TSN', models.FloatField(default=None, null=True)),
                ('INST', models.FloatField(default=None, null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'agg_heure',
            },
        ),
        migrations.CreateModel(
            name='DECADQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATJ', models.DateField(default=django.utils.timezone.now)),
                ('DATRECU', models.DateTimeField(default=django.utils.timezone.now)),
                ('NUM_DECADE', models.IntegerField(default=None, null=True, verbose_name='Numero de la decade')),
                ('RR', models.FloatField(default=None, null=True)),
                ('STATUS_DRR', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('RRAB', models.FloatField(default=None, null=True, verbose_name='Precipitation maxi en 24h')),
                ('STATUS_RRAB', models.IntegerField(default=None, null=True, verbose_name='1 - Relevé manuel, 2 - Relevé automatique')),
                ('RRABDAT', models.DateTimeField(default=None, null=True)),
                ('NBJRR1', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 1mm')),
                ('NBJRR5', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 5mm')),
                ('NBJRR10', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 10mm')),
                ('NBJRR30', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 30mm')),
                ('NBJRR50', models.IntegerField(default=None, null=True, verbose_name='Nb de jours RR sup à 50mm')),
                ('NBJRR100', models.IntegerField(null=True, verbose_name='Nb de jours RR sup à 100mm, default=None')),
                ('PMERM', models.FloatField(default=None, null=True)),
                ('PMERMINAB', models.FloatField(default=None, null=True)),
                ('PMERMINABDAT', models.DateTimeField(default=None, null=True)),
                ('TX', models.FloatField(default=None, null=True, verbose_name='Moyenne des TX de la decade')),
                ('TXAB', models.FloatField(default=None, null=True, verbose_name='TX max de la decade')),
                ('TXABDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TX de la decade')),
                ('TXMIN', models.FloatField(default=None, null=True, verbose_name='TX min de la decade')),
                ('TXMINDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TX min de la decade')),
                ('NBJTX0', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 0')),
                ('NBJTX25', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 25')),
                ('NBJTX30', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 30')),
                ('NBJTX35', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 35')),
                ('NBJTXI20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 20')),
                ('NBJTXI27', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est inf à 27')),
                ('NBJTX32', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TX est sup à 32')),
                ('TN', models.FloatField(default=None, null=True, verbose_name='Moyenne des TN de la decade')),
                ('TNAB', models.FloatField(default=None, null=True, verbose_name='TN min de la decade')),
                ('TNDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TN min de la decade')),
                ('TNMAX', models.FloatField(default=None, null=True, verbose_name='TN max de la decade')),
                ('TNMAXDAT', models.DateTimeField(default=None, null=True, verbose_name='Date de la TN max de la decade')),
                ('NBJTN5', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à -5')),
                ('NBJTNI10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 10')),
                ('NBJTNI15', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 15')),
                ('NBJTNI20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 20')),
                ('NBJTNS20', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est sup à 20')),
                ('NBJTNS25', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est sup à 25')),
                ('NBJGELEE', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou la TN est inf à 0')),
                ('UNAB', models.FloatField(default=None, null=True, verbose_name='Humidite relative minimale de la decade')),
                ('UNABDAT', models.DateTimeField(default=None, null=True, verbose_name="Date de l'Humidite relative minimale de la decade")),
                ('UXAB', models.FloatField(default=None, null=True, verbose_name='Humidite relative maximale de la decade')),
                ('UXABDAT', models.DateTimeField(default=None, null=True, verbose_name="Date de l'humidite relative maximale de la decade")),
                ('UMM', models.FloatField(default=None, null=True, verbose_name='Moyenne des humidites relatives de la decade')),
                ('FXIAB', models.FloatField(default=None, null=True, verbose_name='Rafale maxi de la décade')),
                ('DXIAB', models.FloatField(default=None, null=True, verbose_name='Direction de la rafale maxi de la décade')),
                ('FXIDAT', models.DateTimeField(default=None, null=True, verbose_name='Date la rafale maxi de la decade')),
                ('NBJFF10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FF est sup à 10m/s')),
                ('NBJFF16', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FF est sup à 16m/s')),
                ('NBJFF28', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FF est sup à 28m/s')),
                ('FXYAB', models.FloatField(default=None, null=True, verbose_name='FXY max de la decade')),
                ('DXYAB', models.FloatField(default=None, null=True, verbose_name='Direction du FXYAB de la decade')),
                ('FXYABDAT', models.DateTimeField(default=None, null=True, verbose_name='Date du FXYAB de la decade')),
                ('NBJFXY8', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 8m/s')),
                ('NBJFXY10', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 10m/s')),
                ('NBJFXY15', models.IntegerField(default=None, null=True, verbose_name='Nombre de jours ou FXY est sup à 15m/s')),
                ('INST', models.IntegerField(default=None, null=True, verbose_name="Duree d'insolation quotidienne moyenne (min, default=None)")),
                ('HFM', models.FloatField(default=None, null=True)),
                ('HFX', models.FloatField(default=None, null=True)),
                ('HFN', models.FloatField(default=None, null=True)),
                ('HSM', models.FloatField(default=None, null=True)),
                ('HSX', models.FloatField(default=None, null=True)),
                ('HSN', models.FloatField(default=None, null=True)),
                ('TSM', models.FloatField(default=None, null=True)),
                ('TSX', models.FloatField(default=None, null=True)),
                ('TSN', models.FloatField(default=None, null=True)),
                ('POSTE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.poste')),
            ],
            options={
                'db_table': 'agg_decad',
            },
        ),
        migrations.AddField(
            model_name='commune',
            name='PAYS',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='gestion.pays'),
        ),
    ]
