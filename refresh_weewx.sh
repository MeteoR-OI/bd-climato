rsync -v weewx/tags.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/wee_json weewx@192.168.1.10:root/bin
rsync -v weewx/units.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/engine.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/accum.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/reportengine.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/cheetahgenerator.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx/extensions.py weewx@192.168.1.10:root/bin/user
rsync -v weewx/weewx.conf weewx@192.168.1.10:root
rsync -v weewx/weewx_json.conf weewx@192.168.1.10:root
rsync -v weewx/skin_Bootstrap.conf weewx@192.168.1.10:root/skins/Bootstrap/skin.conf
rsync -v weewx/skin_Json.conf weewx@192.168.1.10:root/skins/Json/skin.conf
rsync -v weewx/obs.YYYY-MM-DD-HH-mm.json.tmpl weewx@192.168.1.10:root/skins/Bootstrap/json
rsync -v weewx/arch.json.tmpl weewx@192.168.1.10:root/skins/Json/json

