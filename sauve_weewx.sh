rsync -v weewx@192.168.1.10:root/bin/weewx/tags.py weewx4
rsync -v weewx@192.168.1.10:root/bin/wee_json weewx4
rsync -v weewx@192.168.1.10:root/bin/weewx/units.py weewx4
rsync -v weewx@192.168.1.10:root/bin/weewx/engine.py weewx4
rsync -v weewx@192.168.1.10:root/bin/weewx/accum.py weewx4
rsync -v weewx@192.168.1.10:root/bin/weewx/reportengine.py weewx4
rsync -v weewx@192.168.1.10:root/bin/weewx/cheetahgenerator.py weewx4
rsync -v weewx@192.168.1.10:root/bin/user/extensions.py weewx4
rsync -v weewx@192.168.1.10:root/weewx.conf weewx4
rsync -v weewx@192.168.1.10:root/weewx_dev.conf weewx4
rsync -v weewx@192.168.1.10:root/skins/Bootstrap/skin.conf weewx4/skin_bootstrap.conf
rsync -v weewx@192.168.1.10:root/skins/Dev/skin.conf weewx4/skin_dev.conf
rsync -v weewx@192.168.1.10:root/skins/Bootstrap/json/obs.YYYY-MM-DD-HH-mm.json.tmpl weewx4
rsync -v weewx@192.168.1.10:root/skins/Dev/json/dev.obs.json.tmpl weewx4

