rsync -v tags.py weewx@192.168.1.10:root/bin/weewx
rsync -v wee_json weewx@192.168.1.10:root/bin
rsync -v units.py weewx@192.168.1.10:root/bin/weewx
rsync -v engine.py weewx@192.168.1.10:root/bin/weewx
rsync -v accum.py weewx@192.168.1.10:root/bin/weewx
rsync -v reportengine.py weewx@192.168.1.10:root/bin/weewx
rsync -v cheetahgenerator.py weewx@192.168.1.10:root/bin/weewx
rsync -v extensions.py weewx@192.168.1.10:root/bin/user
rsync -v weewx_json.conf weewx@192.168.1.10:root
rsync -v skin_Bootstrap.conf weewx@192.168.1.10:root/skins/Bootstrap/skin.conf
rsync -v skin_Json.conf weewx@192.168.1.10:root/skins/Json/skin.conf
rsync -v obs.YYYY-MM-DD-HH-mm.json.tmpl weewx@192.168.1.10:root/skins/Bootstrap/json
rsync -v arch.json.tmpl weewx@192.168.1.10:root/skins/Json/json

