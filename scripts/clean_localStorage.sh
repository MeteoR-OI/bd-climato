

rm -Rf data/localStorage/grafana/
mkdir data/localStorage/grafana
rm -Rf data/localStorage/log/
mkdir data/localStorage/log
rm -Rf data/localStorage/loki/
mkdir data/localStorage/loki
rm -Rf data/localStorage/prometheus/
mkdir data/localStorage/prometheus
rm -Rf data/localStorage/promtail/
mkdir data/localStorage/promtail
rm -Rf data/localStorage/tempo/
mkdir data/localStorage/tempo

touch ./data/localStorage/log/django_debug.log
touch ./data/localStorage/log/django_info.log
