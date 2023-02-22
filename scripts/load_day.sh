
psql -d climatest < data/sqlScripts/delete_all.sql
rm -f data/json_auto_load/*.json
rm -f data/json_auto_load/done/*.json
rm -f data/json_auto_load/failed/*.json
cp data/json_in_git/MTG320/obs.2022.01.14/*.json  data/json_auto_load
cp data/json_in_git/MTG320/obs.2022.01.15/*.json  data/json_auto_load
cp data/json_in_git/MTG320/obs.2022.01.16/*.json  data/json_auto_load
cp data/json_in_git/MTG320/day.2022-01-15.json  data/json_not_in_git
python3 manage.py svc auto --run
python3 manage.py loadJson day.2022-01-15.json  --tmp --validation
echo 'Appuyez sur une touche quand toutes les données sont chargées'
read -s
python3 manage.py compAgg 2 --day
