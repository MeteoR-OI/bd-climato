# installer for MeteoR-OI database project.
#
# Based on bootstrap installer (Nick Dajda 2014-2015)
#
# Configured by Quetelard 2023.

import os.path
import configobj

import setup
import distutils

def loader():
    return MeteoROIInstaller()

class MeteoROIInstaller(setup.ExtensionInstaller):
    _skin_conf_files = ['Bootstrap/skin.conf',
                        'Images/skin.conf',
                        'Json/skin.conf']

    def __init__(self):
        files=[('skins/Bootstrap',
            ['skins/Bootstrap/about.html.tmpl',
             'skins/Bootstrap/history.html.tmpl',
             'skins/Bootstrap/direct.html.tmpl',
             'skins/Bootstrap/index.html.tmpl',
             'skins/Bootstrap/menu.html.tmpl',
             'skins/Bootstrap/month.html.tmpl',
             'skins/Bootstrap/stats.html.tmpl',
             'skins/Bootstrap/week.html.tmpl',
             'skins/Bootstrap/year.html.tmpl',
             'skins/Bootstrap/noaa_statistics.html.tmpl',
             'skins/Bootstrap/skin.conf']),
           ('skins/Bootstrap/NOAA',
            ['skins/Bootstrap/NOAA/NOAA-YYYY.txt.tmpl',
             'skins/Bootstrap/NOAA/NOAA-YYYY-MM.txt.tmpl']),
           ('skins/Bootstrap/XML',
            ['skins/Bootstrap/XML/weewx_pws.xml.tmpl']),
           ('skins/Bootstrap/json',
            ['skins/Bootstrap/json/obs.MTG320.YYYY-MM-DDTHH-mm.json.tmpl',
             'skins/Bootstrap/json/daily.json.tmpl']),
           ('skins/Images',
            ['skins/Images/skin.conf']),
           ('skins/Bootstrap/Statistics',
            ['skins/Bootstrap/Statistics/YYYY_MM_NOAA.txt.tmpl',
             'skins/Bootstrap/Statistics/YYYY_NOAA.txt.tmpl']),
           ('skins/Json',
            ['skins/Json/skin.conf',
             'skins/Json/weewx.conf']),
           ('skins/Json/json',
            ['skins/Json/json/arch.MTG320.YYYY-MM-DDTHH-mm.json.tmpl']),
           ('bin',
            ['bin/wee_json',
             'bin/wee_import']),
           ('bin/user',
            ['bin/user/gaugeengine.py',
             'bin/user/gauges.py',
             'bin/user/extensions.py',
             'bin/user/historygenerator.py',
             'bin/user/translategenerator.py',
             'bin/user/timeperiods.py']),
           ('bin/weewx',
            ['bin/weewx/__init__.py',
             'bin/weewx/accum.py',
             'bin/weewx/cheetahgenerator.py',
             'bin/weewx/engine.py',
             'bin/weewx/reportengine.py',
             'bin/weewx/tags.py',
             'bin/weewx/units.py']),
           ('skins/Bootstrap/css',
            ['skins/Bootstrap/css/bootstrap.min.css']),
           ('skins/Bootstrap/js',
            ['skins/Bootstrap/js/bootstrap.min.js',
             'skins/Bootstrap/js/ekko-lightbox.min.js']),
           ('skins/languages',
            ['skins/languages/catala.conf',
             'skins/languages/dutch.conf',
             'skins/languages/espanol.conf',
             'skins/languages/finnish.conf',
             'skins/languages/francais.conf',
             'skins/languages/german.conf',
             'skins/languages/italian.conf'])]

        super(MeteoROIInstaller, self).__init__(
            version="0.1",
            name='meteor-oi',
            description='modifs for meteor-oi database project',
            author="Hubert Quetelard",
            author_email="hubert.quetelard@gmail.com",
            config={
                'StdReport': {
                    'SmallImages': {
                        'skin':'Images',
                        'HTML_ROOT':'Bootstrap/images'},
                    'BigImages': {
                        'skin':'Images',
                        'HTML_ROOT':'Bootstrap/big_images',
                        'ImageGenerator' : {
                            'image_width'            : '900',
                            'image_height'           : '600',
                            'anti_alias'             : '2',
                            'top_label_font_size'    : '18',
                            'unit_label_font_size'   : '18',
                            'bottom_label_font_size' : '14',
                            'axis_label_font_size'   : '14'}},
                    'HTMLPages': {
                        'skin':'Bootstrap',
                        'HTML_ROOT':'Bootstrap'}}},
            files=files)

        print ("")
        print ("The following alternative languages are available:")
        self.language = None

        for f in files:
            if f[0] == 'skins/languages':
                for language in f[1]:
                    l = language.strip('conf').split('/')[-1]
                    print ("   %s" % l[:-1])

        print ("")
        print ("Language changes can be made in skins/Bootstrap/skin.conf")

        print ("")
        print ("Default location for HTML and image files is public_html/Bootstrap")
        print ("*** POINT YOUR BROWSER TO: public_html/Bootstrap/index.html ***")
        print ("")
