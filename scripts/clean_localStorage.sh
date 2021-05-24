
mkdir -p data/localStorage
rm -Rf data/localStorage/docker/
mkdir data/localStorage/docker
rm -Rf data/localStorage/grafana/
mkdir data/localStorage/grafana
rm -Rf data/localStorage/log/
mkdir data/localStorage/log
rm -Rf data/localStorage/loki/
mkdir data/localStorage/loki
rm -Rf data/localStorage/postgres/
mkdir data/localStorage/postgres
rm -Rf data/localStorage/prometheus/
mkdir data/localStorage/prometheus
rm -Rf data/localStorage/promtail/
mkdir data/localStorage/promtail
rm -Rf data/localStorage/tempo/
mkdir data/localStorage/tempo

touch ./data/localStorage/log/django.log

mkdir -p data/json_auto_load/done
mkdir -p data/json_auto_load/failed
