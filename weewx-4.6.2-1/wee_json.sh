from=$1
to=$2
level=$3
bin/wee_json --from=$from --to=$to --level=$level --verbose
from_in_ut=$(date +%s --date=$from)
to_in_ut=$(date +%s --date=$to)
next_from_in_ut=$((from_in_ut + 86400))
while [ $next_from_in_ut -lt $to_in_ut ]
do
from=$(date +'%Y-%m-%dT00:00' --date=@$next_from_in_ut)
bin/wee_json --from=$from --to=$to --level=$level
from_in_ut=$(date +%s --date=$from)
next_from_in_ut=$((from_in_ut + 86400))
done
cd public_html/json
find . -name 'arch.*.json' -exec bash -c 'mv $0 ${0/arch/obs-regen}' {} \;
mv obs-regen.*.json ../../json_archive
cd
