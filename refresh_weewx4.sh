rsync -v weewx4/tags.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/wee_json weewx@192.168.1.10:root/bin
rsync -v weewx4/units.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/engine.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/accum.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/reportengine.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/cheetahgenerator.py weewx@192.168.1.10:root/bin/weewx
rsync -v weewx4/extensions.py weewx@192.168.1.10:root/bin/user
rsync -v weewx4/weewx.conf weewx@192.168.1.10:root
rsync -v weewx4/weewx_json.conf weewx@192.168.1.10:root
rsync -v weewx4/skin_Bootstrap.conf weewx@192.168.1.10:root/skins/Bootstrap/skin.conf
rsync -v weewx/skin_Json.conf weewx@192.168.1.10:root/skins/Json/skin.conf
rsync -v weewx/obs.YYYY-MM-DD-HH-mm.json.tmpl weewx@192.168.1.10:root/skins/Bootstrap/json
rsync -v weewx/arch.json.tmpl weewx@192.168.1.10:root/skins/Json/json
