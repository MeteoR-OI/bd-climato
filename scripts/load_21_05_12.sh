
psql -p 5435 -d climatest < data/sqlScripts/delete_all.sql
rm data/json_auto_load/*.json
cp data/json_in_git/obs_05_12/*.json data/json_auto_load
cp data/json_in_git/obs.2021-05-12.json  data/json_not_in_git
python3 manage.py svc auto --run
python3 manage.py loadJson obs.2021-05-12.json  --tmp --validation
echo 'Appuyez sur une touche quand toutes les données sont chargées'
read -s
python manage.py compAgg 2 --day
