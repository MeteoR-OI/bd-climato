rsync -v weewx@192.168.1.10:root/bin/weewx/tags.py weewx
rsync -v weewx@192.168.1.10:root/bin/wee_json weewx
rsync -v weewx@192.168.1.10:root/bin/weewx/units.py weewx
rsync -v weewx@192.168.1.10:root/bin/weewx/engine.py weewx
rsync -v weewx@192.168.1.10:root/bin/weewx/accum.py weewx
rsync -v weewx@192.168.1.10:root/bin/weewx/reportengine.py weewx
rsync -v weewx@192.168.1.10:root/bin/weewx/cheetahgenerator.py weewx
rsync -v weewx@192.168.1.10:root/bin/user/extensions.py weewx
rsync -v weewx@192.168.1.10:root/weewx.conf weewx
rsync -v weewx@192.168.1.10:root/weewx_json.conf weewx
rsync -v weewx@192.168.1.10:root/skins/Bootstrap/skin.conf weewx/skin_Bootstrap.conf
rsync -v weewx@192.168.1.10:root/skins/Json/skin.conf weewx/skin_Json.conf
rsync -v weewx@192.168.1.10:root/skins/Bootstrap/json/obs.YYYY-MM-DD-HH-mm.json.tmpl weewx
rsync -v weewx@192.168.1.10:root/skins/Json/json/arch.json.tmpl weewx
