# Simple example of Python Fabric + Jinja deployment of a file using templating

from datetime import datetime

from fabric2.tasks import task
#from fabric.tasks import execute
#from fabric.contrib.files import upload_template


######### Subtasks  ########
@task
def setSysEnv(c):
    src_file = '/etc/environment'
    default_pattern = c.sys_default.station_id
    station_id = c.station.id
    cmd = "sed -i 's/%s/%s/g' %s" % (default_pattern, station_id, src_file)
    result = c.sudo(cmd)
    c.run("cat %s" % src_file)

@task
def initUserHost(c):
    with(c.cd('/home/meteor/meteoroi_scripts')):
        c.run('sudo ./rasp00_change_password.sh', env={'STATION_ID': c.station.id})

###########################



@task
def test(c):
    today = datetime.now()
    today_string = today.strftime('%m%d%Y')
    print today_string
    print c.get('station')
    c.run("env", env={'STATION_ID': c.station.id})
    # Replaces {{ datestring|escape }} in the template with a date string.
#    upload_template('/path/to/local_dir/setup.py.jinja', 
#                      '/path/to/remote_dir/setup.py', 
#                      context={ 'datestring': today_string }, 
#                      use_jinja=True)

#execute(create_setup_from_template, hosts=[''])
