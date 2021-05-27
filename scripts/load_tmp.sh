

psql -d climatest < data/sqlScripts/delete_all.sql
cp data/json_in_git/obs_05_23/*.json  data/json_auto_load/done
cp data/json_in_git/obs_05_24/*.json  data/json_auto_load/done
cp data/json_in_git/obs_05_25/*.json  data/json_auto_load/done

cp data/json_in_git/obs.2021-05-24.json  data/json_not_in_git
cp data/json_in_git/obs.2021-05-25.json  data/json_not_in_git

mv data/json_auto_load/done/*.json data/json_auto_load

python3 manage.py svc auto --run

python3 manage.py loadJson obs.2021-05-24.json --tmp --validation
python3 manage.py loadJson obs.2021-05-25.json --tmp --validation

python3 manage.py compAgg 2 --day
