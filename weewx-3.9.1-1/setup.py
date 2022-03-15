#!/usr/bin/env python
#
#    weewx --- A simple, high-performance weather station server
#
#    Copyright (c) 2009-2019 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Customized distutils setup file for weewx."""

from __future__ import with_statement

import os.path
import sys
import re
import tempfile
import shutil

import configobj

from distutils.core import setup
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.command.install_scripts import install_scripts
from distutils.command.sdist import sdist
import distutils.dir_util

# Useful for debugging setup.py. Set the environment variable
# DISTUTILS_DEBUG to get more debug info.
from distutils.debug import DEBUG

# Find the install bin subdirectory:
this_file = os.path.join(os.getcwd(), __file__)
this_dir = os.path.abspath(os.path.dirname(this_file))
bin_dir = os.path.abspath(os.path.join(this_dir, 'bin'))

# Now that we've found the bin subdirectory, inject it into the path:
sys.path.insert(0, bin_dir)

# Now we can import some weewx modules
import weewx

VERSION = weewx.__version__
import weecfg.extension
import weeutil.weeutil
from weecfg import Logger

logger=Logger(verbosity=1)

# start_scripts = ['util/init.d/weewx.bsd',
#                  'util/init.d/weewx.debian',
#                  'util/init.d/weewx.lsb',
#                  'util/init.d/weewx.redhat',
#                  'util/init.d/weewx.suse']

# The default station information:
stn_info = {'station_type': 'Simulator',
            'driver': 'weewx.drivers.simulator'}


# ==============================================================================
# install
# ==============================================================================

class weewx_install(install):
    """Specialized version of install, which adds a --no-prompt option to
    the 'install' command."""

    # Add an option for --no-prompt:
    user_options = install.user_options + [('no-prompt', None, 'Do not prompt for station info')]

    def initialize_options(self, *args, **kwargs):
        install.initialize_options(self, *args, **kwargs)
        self.no_prompt = None

    def finalize_options(self):
        install.finalize_options(self)
        if self.no_prompt is None:
            self.no_prompt = False


# ==============================================================================
# install_lib
# ==============================================================================

class weewx_install_lib(install_lib):
    """Specialized version of install_lib, which backs up old bin subdirectories."""

    def run(self):
        # Save any existing 'bin' subdirectory:
        if os.path.exists(self.install_dir):
            bin_savedir = weeutil.weeutil.move_with_timestamp(self.install_dir)
            print "Saved bin subdirectory as %s" % bin_savedir
        else:
            bin_savedir = None

        # Run the superclass's version. This will install all incoming files.
        install_lib.run(self)

        # If the bin subdirectory previously existed, and if it included
        # a 'user' subsubdirectory, then restore it
        if bin_savedir:
            user_backupdir = os.path.join(bin_savedir, 'user')
            if os.path.exists(user_backupdir):
                user_dir = os.path.join(self.install_dir, 'user')
                distutils.dir_util.copy_tree(user_backupdir, user_dir)
                try:
                    # The file schemas.py is no longer used, and can interfere with schema
                    # imports. See issue #54.
                    os.rename(os.path.join(user_dir, 'schemas.py'),
                              os.path.join(user_dir, 'schemas.py.old'))
                except OSError:
                    pass
                try:
                    os.remove(os.path.join(user_dir, 'schemas.pyc'))
                except OSError:
                    pass

        # added by QUETELARD new version extensions.py
        incoming_schema_path = os.path.join(bin_dir, 'user/extensions.py')
        target_path = os.path.join(self.install_dir, 'user/extensions.py')
        distutils.file_util.copy_file(incoming_schema_path, target_path)


# ==============================================================================
# install_data
# ==============================================================================

class weewx_install_data(install_data):
    """Specialized version of install_data. Mostly, it deals with upgrading
    and merging any old weewx.conf configuration files."""

    def initialize_options(self):
        # Initialize my superclass's options:
        install_data.initialize_options(self)
        # Set to None so we inherit whatever setting comes from weewx_install:
        self.no_prompt = None

    def finalize_options(self):
        # Finalize my superclass's options:
        install_data.finalize_options(self)
        # This will set no_prompt to whatever is in weewx_install:
        self.set_undefined_options('install', ('no_prompt', 'no_prompt'))

    def copy_file(self, f, install_dir, **kwargs):
        # If this is the configuration file, then merge it instead
        # of copying it
        if f == 'weewx.conf':
            rv = self.process_config_file(f, install_dir, **kwargs)
        # added by QUETELARD
        elif f == 'skins/Json/weewx.conf':
            rv = self.process_Json_config_file(f, install_dir, **kwargs)
        elif f == 'skins/Bootstrap/skin.conf':
            rv = self.process_Bootstrap_skin_file(f, install_dir, **kwargs) 
        elif f == 'skins/Json/skin.conf':
            rv = self.process_Json_skin_file(f, install_dir, **kwargs) 
        # end added by QUETELARD  
        # elif f in start_scripts:
        #     rv = self.massage_start_file(f, install_dir, **kwargs)
        else:
            rv = install_data.copy_file(self, f, install_dir, **kwargs)
        return rv

    def run(self):
        # If there is a skins directory already, just install what the user doesn't already have.
        if os.path.exists(os.path.join(self.install_dir, 'skins')):
            # A skins directory already exists. Build a list of skins that are missing and should be added to it.
            install_files = []
            for skin_name in ['Ftp', 'Mobile', 'Rsync', 'Seasons', 'Smartphone', 'Standard']:
                rel_name = 'skins/' + skin_name
                if not os.path.exists(os.path.join(self.install_dir, rel_name)):
                    # The skin has not already been installed. Include it.
                    install_files += filter(lambda dat: dat[0].startswith(rel_name), self.data_files)
            # Exclude all the skins files...
            other_files = filter(lambda dat: not dat[0].startswith('skins'), self.data_files)
            # ... then add the needed skins back in
            # disabled by QUETELARD
            #self.data_files = other_files + install_files

        remove_obsolete_files(self.install_dir)

        # Run the superclass's run():
        install_data.run(self)

    def process_config_file(self, f, install_dir, **kwargs):
        global stn_info

        # Open up and parse the distribution config file:
        try:
            dist_config_dict = configobj.ConfigObj(f, file_error=True)
        except IOError as e:
            sys.exit(str(e))
        except SyntaxError as e:
            sys.exit("Syntax error in distribution configuration file '%s': %s"
                     % (f, e))

        # The path where the weewx.conf configuration file will be installed
        install_path = os.path.join(install_dir, os.path.basename(f))

        # Do we have an old config file?
        if os.path.isfile(install_path):
            # Yes. Read it
            config_path, config_dict = weecfg.read_config(install_path, None)
            if DEBUG:
                print "Old configuration file found at", config_path

            # Update the old configuration file to the current version,
            # then merge it into the distribution file
            weecfg.update_and_merge(config_dict, dist_config_dict)
        else:
            # No old config file. Use the distribution file, then, if we can,
            # prompt the user for station specific info
            config_dict = dist_config_dict
            if not self.no_prompt:
                # Prompt the user for the station information:
                stn_info = weecfg.prompt_for_info()
                driver = weecfg.prompt_for_driver(stn_info.get('driver'))
                stn_info['driver'] = driver
                stn_info.update(weecfg.prompt_for_driver_settings(driver, config_dict))
                if DEBUG:
                    print "Station info =", stn_info
            weecfg.modify_config(config_dict, stn_info, DEBUG)

        # Set the WEEWX_ROOT
        config_dict['WEEWX_ROOT'] = os.path.normpath(install_dir)

        # NB: use mkstemp instead of NamedTemporaryFile because we need to
        # do the delete (windows gets mad otherwise) and there is no delete
        # parameter in NamedTemporaryFile in python 2.5.

        # Time to write it out. Get a temporary file:
        tmpfd, tmpfn = tempfile.mkstemp()
        # Wrap the os-level file descriptor in a Python file object
        with os.fdopen(tmpfd, 'w') as tmpfile:
            # Write the config file
            config_dict.write(tmpfile)

        # Save the old config file if it exists:
        if not self.dry_run and os.path.exists(install_path):
            backup_path = weeutil.weeutil.move_with_timestamp(install_path)
            print "Saved old configuration file as %s" % backup_path

        # Now install the temporary file (holding the merged config data)
        # into the proper place:
        rv = install_data.copy_file(self, tmpfn, install_path, **kwargs)

        # Now get rid of the temporary file
        os.remove(tmpfn)

        # Set the permission bits unless this is a dry run:
        if not self.dry_run:
            shutil.copymode(f, install_path)

        return rv

    # added by QUETELARD
    def process_Json_config_file(self, f, install_dir, **kwargs):

        # Open up and parse the distribution json config file:
        try:
            dist_config_dict = configobj.ConfigObj(f, file_error=True)
        except IOError as e:
            sys.exit(str(e))
        except SyntaxError as e:
            sys.exit("Syntax error in distribution configuration file '%s': %s"
                     % (f, e))

        # The path where the json weewx.conf configuration file will be installed
        install_path = os.path.join(install_dir, os.path.basename(f))

        # Do we have an old json config file?
        if os.path.isfile(install_path):
            # Yes. Read it
            config_path, config_dict = weecfg.read_config(install_path, None)
            if DEBUG:
                print "Old configuration file found at", config_path

            # Update the old json configuration file to the current version,
            # then merge it into the distribution file
            weecfg.update_and_merge(config_dict, dist_config_dict)
        else:
            # No old config file. Use the distribution file, then, if we can,
            # use the root config file weewx.conf
            config_dict = dist_config_dict
            install_dir = install_dir.replace('/skins/Json','') 
            root_install_path = os.path.join(install_dir, 'weewx.conf')
            root_config_path, root_config_dict = weecfg.read_config(root_install_path, None)

            # update with root weewx.conf
            config_dict['Station']       = root_config_dict['Station']
            config_dict['Vantage']       = root_config_dict['Vantage']
            # Add a major comment deliminator:
            config_dict.comments['Vantage'] = weecfg.major_comment_block

            config_dict['StdConvert']    = root_config_dict['StdConvert']
            config_dict['DataBindings']  = root_config_dict['DataBindings']
            config_dict['Databases']     = root_config_dict['Databases']
            config_dict['DatabaseTypes'] = root_config_dict['DatabaseTypes']

        weecfg.reorder_sections(config_dict, 'Vantage', 'Station', after=True)
       
        # Set the WEEWX_ROOT
        config_dict['WEEWX_ROOT']    = os.path.normpath(install_dir.replace('/skins/Json',''))

        # NB: use mkstemp instead of NamedTemporaryFile because we need to
        # do the delete (windows gets mad otherwise) and there is no delete
        # parameter in NamedTemporaryFile in python 2.5.

        # Time to write it out. Get a temporary file:
        tmpfd, tmpfn = tempfile.mkstemp()
        # Wrap the os-level file descriptor in a Python file object
        with os.fdopen(tmpfd, 'w') as tmpfile:
            # Write the config file
            config_dict.write(tmpfile)

        # Save the old config file if it exists:
        if not self.dry_run and os.path.exists(install_path):
            backup_path = weeutil.weeutil.move_with_timestamp(install_path)
            print "Saved old configuration file as %s" % backup_path

        # Now install the temporary file (holding the merged config data)
        # into the proper place:
        rv = install_data.copy_file(self, tmpfn, install_path, **kwargs)

        # Now get rid of the temporary file
        os.remove(tmpfn)

        # Set the permission bits unless this is a dry run:
        if not self.dry_run:
            shutil.copymode(f, install_path)
            
        return rv

    def process_Bootstrap_skin_file(self, f, install_dir, **kwargs):

        # Open up and parse the distribution Bootstrap skin file:
        try:
            dist_skin_dict = configobj.ConfigObj(f, file_error=True)
        except IOError as e:
            sys.exit(str(e))
        except SyntaxError as e:
            sys.exit("Syntax error in distribution Bootstrap skin file '%s': %s"
                     % (f, e))

        # The path where the Bootstrap skin.conf file will be installed
        install_path = os.path.join(install_dir, os.path.basename(f))
        
        # Do we have an old Bootstrap config file?
        if os.path.isfile(install_path):
            # Yes. Read it
            skin_path, skin_dict = weecfg.read_config(install_path, None)
            if DEBUG:
                print "Old Bootstrap json file found at", config_path
             
            # Update the old Bootstrap configuration file to the current version
            if 'JSON2' not in skin_dict['CheetahGenerator']['ToDate']:
                id_station = skin_dict['BootstrapLabels']['station_id']
                json2_template = dist_skin_dict['CheetahGenerator']['ToDate']['JSON2']['template']
                json2_template = json2_template.replace('meteor', id_station)
                skin_dict['CheetahGenerator']['ToDate']['JSON2'] = \
                          dist_skin_dict['CheetahGenerator']['ToDate']['JSON2']
                skin_dict['CheetahGenerator']['ToDate']['JSON2']['template'] = json2_template 
                skin_dict['CheetahGenerator']['ToDate'].comments['JSON2'] = ['    # added by QUETELARD']
        else:
            # No old Bootstrap skin file. No possible
            sys.exit("Bootstrap skin file not found. Installation process stopped !")

        # Time to write it out. Get a temporary file:
        tmpfd, tmpfn = tempfile.mkstemp()
        # Wrap the os-level file descriptor in a Python file object
        with os.fdopen(tmpfd, 'w') as tmpfile:
            # Write the config file
            skin_dict.write(tmpfile)

        # Save the old config file if it exists:
        if not self.dry_run and os.path.exists(install_path):
            backup_path = weeutil.weeutil.move_with_timestamp(install_path)
            print "Saved old configuration file as %s" % backup_path

        # Now install the temporary file (holding the merged config data)
        # into the proper place:
        rv = install_data.copy_file(self, tmpfn, install_path, **kwargs)

        # Now get rid of the temporary file
        os.remove(tmpfn)
        
        # Set the permission bits unless this is a dry run:
        if not self.dry_run:
            shutil.copymode(f, install_path)

        return rv

    def process_Json_skin_file(self, f, install_dir, **kwargs):
	
        # Open up and parse the distribution Json skin file:
        try:
            dist_skin_dict = configobj.ConfigObj(f, file_error=True)
        except IOError as e:
            sys.exit(str(e))
        except SyntaxError as e:
            sys.exit("Syntax error in distribution Json skin file '%s': %s"
                     % (f, e))

        # The path where the json skin.conf file will be installed
        install_path = os.path.join(install_dir, os.path.basename(f))

        # The path where the Bootstrap skin.conf (ref) is installed
        install_dir_ref = install_dir.replace('/skins/Json','/skins/Bootstrap')
        install_path_ref = os.path.join(install_dir_ref, os.path.basename(f))
        skin_path_ref, skin_dict_ref = weecfg.read_config(install_path_ref, None)
        id_station = skin_dict_ref['BootstrapLabels']['station_id'] 
        json_template = dist_skin_dict['CheetahGenerator']['ToDate']['JSON']['template'] 
        json_template = json_template.replace('meteor', id_station) 

        # Do we have an old json skin file?
        if os.path.isfile(install_path):
            # Yes. Read it
            skin_path, skin_dict = weecfg.read_config(install_path, None)

            if DEBUG:
                print "Old Bootstrap skin file found at", config_path

            # Update the old json configuration file to the current version
            if 'JSON' not in skin_dict['CheetahGenerator']['ToDate']:
                skin_dict['CheetahGenerator']['ToDate']['JSON'] = \
                         dist_skin_dict['CheetahGenerator']['ToDate']['JSON']   
                skin_dict['CheetahGenerator']['ToDate']['JSON']['template'] = json_template
                skin_dict['CheetahGenerator']['ToDate'].comments['JSON'] = ['    # added by QUETELARD']
            else:
                skin_dict['CheetahGenerator']['ToDate']['JSON']['template'] = json_template
                 
        else:
            # No old Json skin file. Use the distribution file, then, if we can,
            # use the Bootstrap skin file for update distribution file
            skin_dict = dist_skin_dict
            skin_dict['Extras']['station_id'] = id_station
            skin_dict['CheetahGenerator']['ToDate']['JSON']['template'] = json_template
            skin_dict['CheetahGenerator']['ToDate'].comments['JSON'] = ['    # added by QUETELARD']
            
        # Time to write it out. Get a temporary file:
        tmpfd, tmpfn = tempfile.mkstemp()
        # Wrap the os-level file descriptor in a Python file object
        with os.fdopen(tmpfd, 'w') as tmpfile:
            # Write the config file
            skin_dict.write(tmpfile)

        # Save the old config file if it exists:
        if not self.dry_run and os.path.exists(install_path):
            backup_path = weeutil.weeutil.move_with_timestamp(install_path)
            print "Saved old configuration file as %s" % backup_path

        # Now install the temporary file (holding the merged config data)
        # into the proper place:
        rv = install_data.copy_file(self, tmpfn, install_path, **kwargs)

        # Now get rid of the temporary file
        os.remove(tmpfn)

        # Set the permission bits unless this is a dry run:
        if not self.dry_run:
            shutil.copymode(f, install_path)

        return rv

    # end added by QUETELARD

    def massage_start_file(self, f, install_dir, **kwargs):

        outname = os.path.join(install_dir, os.path.basename(f))
        sre = re.compile(r"WEEWX_ROOT\s*=")

        with open(f, 'r') as infile:
            with tempfile.NamedTemporaryFile("w") as tmpfile:
                for line in infile:
                    if sre.match(line):
                        tmpfile.writelines("WEEWX_ROOT=%s\n" % self.install_dir)
                    else:
                        tmpfile.writelines(line)
                tmpfile.flush()

                rv = install_data.copy_file(self, tmpfile.name, outname, **kwargs)

        # Set the permission bits unless this is a dry run:
        if not self.dry_run:
            shutil.copymode(f, outname)

        return rv


# ==============================================================================
# install_scripts
# ==============================================================================

class weewx_install_scripts(install_scripts):

    def run(self):
        # Run the superclass's version:
        install_scripts.run(self)


# ==============================================================================
# sdist
# ==============================================================================

class weewx_sdist(sdist):
    """Specialized version of sdist which checks for password information in
    the configuration file before creating the distribution.

    For other sdist methods, see:
    http://epydoc.sourceforge.net/stdlib/distutils.command.sdist.sdist-class.html
    """

    def copy_file(self, f, install_dir, **kwargs):
        """Specialized version of copy_file that checks for stray passwords."""

        # If this is the configuration file, check for passwords
        if f == 'weewx.conf':
            import configobj
            config = configobj.ConfigObj(f)

            for section in ['StdRESTful', 'StdReport']:
                for subsection in config[section].sections:
                    try:
                        password = config[section][subsection]['password']
                        if password != 'replace_me':
                            sys.exit("\n*** [%s][[%s]] password found in configuration file. Aborting ***\n\n" \
                                     % (section, subsection))
                    except KeyError:
                        pass

        # Pass on to my superclass:
        return sdist.copy_file(self, f, install_dir, **kwargs)


# ==============================================================================
# utility functions
# ==============================================================================

def remove_obsolete_files(install_dir):
    """Remove no longer needed files from the installation
    directory, nominally /home/weewx."""

    # If the file #upstream.last exists, delete it, as it is no longer used.
    try:
        os.remove(os.path.join(install_dir, 'public_html/#upstream.last'))
    except OSError:
        pass

    # If the file $WEEWX_INSTALL/readme.htm exists, delete it. It's
    # the old readme (since replaced with README)
    try:
        os.remove(os.path.join(install_dir, 'readme.htm'))
    except OSError:
        pass

    # If the file $WEEWX_INSTALL/CHANGES.txt exists, delete it. It's
    # been moved to the docs subdirectory and renamed
    try:
        os.remove(os.path.join(install_dir, 'CHANGES.txt'))
    except OSError:
        pass

    # # The directory start_scripts is no longer used
    # shutil.rmtree(os.path.join(install_dir, 'start_scripts'), True)

    # The file docs/README.txt is now gone
    try:
        os.remove(os.path.join(install_dir, 'docs/README.txt'))
    except OSError:
        pass

    # If the file docs/CHANGES.txt exists, delete it. It's been renamed
    # to docs/changes.txt
    try:
        os.remove(os.path.join(install_dir, 'docs/CHANGES.txt'))
    except OSError:
        pass

    # setup.py is no longer left in WEEWX_ROOT.
    try:
        os.remove(os.path.join(install_dir, 'setup.py'))
    except OSError:
        pass


# ==============================================================================
# main entry point
# ==============================================================================

if __name__ == "__main__":
    setup(name='weewx',
          version=VERSION,
          description='weather software',
          long_description="weewx interacts with a weather station to produce graphs, "
                           "reports, and HTML pages.  weewx can upload data to services such as the "
                           "WeatherUnderground, PWSweather.com, or CWOP.",
          author='Tom Keffer',
          author_email='tkeffer@gmail.com',
          url='http://www.weewx.com',
          license='GPLv3',
          classifiers=['Development Status :: 5 - Production/Stable',
                       'Intended Audience :: End Users/Desktop',
                       'License :: GPLv3',
                       'Operating System :: OS Independent',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 2'],
          requires=['configobj(>=4.5)',
                    'serial(>=2.3)',
                    'Cheetah(>=2.0)',
                    'sqlite3(>=2.5)',
                    'PIL(>=1.1.6)'],
          provides=['weedb',
                    'weeplot',
                    'weeutil',
                    'weewx'],
          cmdclass={"sdist": weewx_sdist,
                    "install": weewx_install,
                    "install_scripts": weewx_install_scripts,
                    "install_data": weewx_install_data,
                    "install_lib": weewx_install_lib},
          platforms=['any'],
          package_dir={'': 'bin'},
          packages=['schemas',
                    'user',
                    'weecfg',
                    'weedb',
                    'weeimport',
                    'weeplot',
                    'weeutil',
                    'weewx',
                    'weewx.drivers'],
          py_modules=['daemon'],
          scripts=['bin/wee_config',
                   'bin/wee_database',
                   'bin/wee_debug',
                   'bin/wee_device',
                   'bin/wee_extension',
                   'bin/wee_import',
                   'bin/wee_reports',
                   'bin/weewxd',
                   'bin/wunderfixer',
                   'bin/wee_json'],
          data_files=[
              ('',
               ['LICENSE.txt',
                'README',
                'trans_json.sh',
                'wee_json.sh',
                'weewx.conf']),
              ## added by QUETELARD  
              ('skins/Bootstrap',
               ['skins/Bootstrap/skin.conf']),
              ('skins/Bootstrap/json',
               ['skins/Bootstrap/json/obs.meteor.YYYY-MM-DDTHH-mm.json.tmpl']),
              ('skins/Json',
               ['skins/Json/skin.conf',
                'skins/Json/weewx.conf']),
              ('skins/Json/json',
               ['skins/Json/json/arch.meteor.YYYY-MM-DDTHH-mm.json.tmpl']),
              ('skins/Images',
               ['skins/Images/skin.conf']),
              ('json_archive',
               ['json_archive/daily.json'])            
              ## end added by QUETELARD
            ]
          )