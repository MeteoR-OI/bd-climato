ssh meteor@localhost
ls -ali ~/.ssh/
echo "ssh-dss AAAAB3NzaC1kc3MAAACBAKV4np/Gag5wIFSIpBH9tTdtzai/E68J+qc/hxqwFzU86amSmBqQt4J0hKclrsYAl/Q9CLBjTO2uB3FWv42VrLn4/6cuN0+L9grr9ehx7qAyH/ktiIhXQGuJchiiAyPaIHdYR6dP5NfmpFCDsjN3oQpQUh/a3tOvLv6k1nZ3j3VPAAAAFQC4V73DVLO90wi5phczg15sy6sKHQAAAIBlMo8PiedWZzj3l9ND5pZfrnw29C4uFdCBWIHDdxqcRyh9Qg3LtcKHSOtCefvXu3xeyVozqHzP6eiO7c7wZfOE361qS8gECWiymtUOu0ZKnTYIG8VY3dwBLPszF3cJLZZ+faNac6qFJWQBA6rjIARapAXGxMzylz6JS5L1n3sEOgAAAIBoGgcrGj7US6MqQJrx8uBgRED7bE37ePy155CeGIYICpTRYRXpVhuK4OZW7tocxH7c8ko8QTLOaq4m93YSO/JR3IsKWNzMnxlD4CfHtTq5ISe4THvLuLUjvAvhaZe95X9hDirA5ioyqucgBjmeF9nHY0110eZdCSMpCEvH2HZGDA== mickael.hoareau@MeteoR-OI" >> ~/.ssh/authorized_keys
ls -ali ~/.ssh/
cat ~/.ssh/authorized_keys
METEOR_USER=meteor
echo $METEOR_USER
sudo addgroup $METEOR_USER weewx
sudo chown -R weewx:weewx /srv/weewx
sudo chmod -R g+w /srv/weewx
cd /srv/weewx/virtualenv && source bin/activate
pip install -U pip
deactivate 
cd
sudo apt-get install python-dev rsync
cat /etc/os-release
apt-cache search libtiff
apt-cache search libjpeg
apt-cache search zlib1g-dev
apt-cache search libfreetype6-dev
apt-cache search liblcms2-dev
apt-cache search libwebp-dev
apt-cache search tcl8.5-dev
apt-cache search tk8.5-dev
apt-cache search python-tk
sudo apt-get install libtiff5-dev libjpeg-dev zlib1g-dev     libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
cd /srv/weewx/virtualenv && source bin/activate
pip install configobj Cheetah pillow pyserial pyusb pyephem
sudo apt-get install mysql-server libmysqld-dev
sudo apt-get install mariadb-server libmariadb-dev
pip install MySQL-python
sudo apt-get install mariadb-server libmariadbclient-dev
df -h
pip install MySQL-python
deactivate 
cd
cd /srv/weewx/virtualenv && source bin/activate && cd -
ll
ls
cd
ls -ali
wget http://www.weewx.com/downloads/weewx-3.8.0.tar.gz
tar xzvf weewx-3.8.0.tar.gz 
ls
cd weewx-3.8.0/
ls
sudo apt-get install ftp
vi setup.cfg 
./setup.py build
./setup.py install
sudo vi /etc/udev/rules.d/vpro.rules
sudo apt-get install fonts-freefont-ttf
cd
wget https://github.com/mhoareau/fuzzy-archer/archive/v2.24-meteoroi-2.tar.gz
cd /srv/weewx/virtualenv && source bin/activate && cd ../root
bin/wee_extension --install=~/v2.24-meteoroi-2.tar.gz
ls -l ~/v2.24-meteoroi-2.tar.gz
bin/wee_extension --install=/home/meteor/v2.24-meteoroi-2.tar.gz
ll
ls
vi skins/Bootstrap/skin.conf 
vi weewx.conf
cd /srv/weewx/root
sudo apt-get install nginx-light
sudo sed -i.backup -e 's/root .*;/root \/srv\/weewx\/root\/public_html;/' /etc/nginx/sites-enabled/default
cat /etc/nginx/sites-enabled/default
diff /etc/nginx/sites-enabled/default.backup /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-enabled/default.backup
sudo nginx -t
sudo service nginx reload
mkdir /srv/weewx/backups
sudo chown -R weewx:weewx /srv/weewx/backups
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install python-smbus python3-smbus python-dev python3-dev
deactivate 
cd
sudo apt-get install python-smbus python3-smbus python-dev python3-dev
sudo apt-get install i2c-tools
sudo i2cdetect -y 1
#TODO : Clone la SD puis créer une nouvelle page sur le wiki (clone la page after-clone)
shutdown -h now
sudo shutdown -h now
sudo apt-get update
sudo apt-get dist-upgrade
sudo passwd pi
sudo vi /etc/environment
echo $STATION_ID_LOWERC
sudo vi /etc/environment
echo $STATION_ID_LOWERC
sudo vi /etc/environment
echo $STATION_ID_LOWERC
sudo vi /etc/environment
echo $STATION_ID_LOWERC
echo $STATION_ID
sudo vi /etc/environment
echo $STATION_ID | tr '[:upper:]' '[:lower:]'
sudo vi /etc/environment
echo $STATION_ID | tr '[:upper:]' '[:lower:]'
ll
ls
vi .bashrc 
ll
mkdir meteoroi_scripts
cd meteoroi_scripts/
ls
vi rasp01_change_hostname.sh
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
echo $CURRENT_HOSTNAME
echo $STATION_ID > /etc/hostname
sudo su
cd meteoroi_scripts/
ll
vi rasp01_change_hostname.sh
sudo su
ll
cat /etc/environment
sudo apt-get install openvpn
ll
sudo su
./test.sh 
sudo su
./test.sh 
sudo su
./test.sh 
whoami 
sudo su
./test.sh 
sudo su
./test.sh 
sudo su
./test.sh 
sudo su
/home/meteor/meteoroi_scripts/rasp02_get_vpn_files.sh 
sudo su weewx
sudo su root 
echo $STATION_ID_LOWERC
echo $STATION_ID
vi /etc/passwd
cat /etc/environment 
sudo su weewx
sudo vi /etc/environment 
sudo vi /etc/bash.bashrc 
sudo su weewx
sudo vi /etc/environment 
sudo su
ll
cd 
ll
sudo su weewx
sudo vi /etc/environment 
ll
sudo su $WEEWX_USER
sudo mariadb -u root
mysql
sudo mysql -u root
echo $STATION_ID
ll
cd meteoroi_scripts/
ls
ls -ali
ln -s /srv/weewx/scripts/rasp04_send_ssh_key.sh rasp04_send_ssh_key.sh
ll
vi rasp05_init_db_access.sh
chmod +x rasp05_init_db_access.sh 
ll
sudo mysql_secure_installation 
mysql -u root -p6DI+mrlnTW
sudo mysql -u root -p6DI+mrlnTW
sudo su
df -h
cd
lsusb
sudo vi /etc/udev/rules.d/vpro.rules
ls
sudo cp /srv/weewx/root/util/init.d/weewx.debian /etc/init.d/weewx
sudo vi /etc/init.d/weewx
chmod +x /etc/init.d/weewx
sudo chmod +x /etc/init.d/weewx
sudo vi /etc/init.d/weewx
sudo chown -R weewx:weewx /srv/weewx
cd /srv/weewx/virtualenv && source bin/activate
ll
cd ../root/
bin/wee_device --set-interval=5
ll
vi /srv/weewx/root/backup.sh
sudo vi /srv/weewx/root/backup.sh
chmod +x /srv/weewx/root/backup.sh
sudo chmod +x /srv/weewx/root/backup.sh
sudo vi ./srv/weewx/root/backup.sh
sudo vi /srv/weewx/root/backup.sh
./srv/weewx/root/backup.sh
/srv/weewx/root/backup.sh
sudo vi /srv/weewx/root/backup.sh
sudo i2cdetect -y 1
sudo i2cdetect -y 0
sudo i2cdetect -y 1
sudo shutdown -h now
cd /home/meteor/meteoroi_scripts
ls
vi rasp02_get_vpn_files.sh 
sudo vi rasp02_get_vpn_files.sh 
sudo vi rasp03
sudo vi rasp03_install_vpn_files.sh 
sudo su
ls
sudo shutdown -h now
date
ifconfig
kjwsfngsijdfghousidfhgkudfgsufdkhsg
ls
ls -l
cd meteoroi_scripts/
ls
cd /srv/weewx/
ls
ls -l
ls scripts/
cd root/
ls -l
sudo vi /etc/environment 
echo $STATION_ID
bash
echo $STATION_ID
source /etc/environment
echo $STATION_ID
sudo su
ls -ls
cd /srv/weewx/root/
ll
vi weewx.conf
ls -l
vi weewx.conf
cd skins/
ls -l
sudo passwd pi
sudo su
cat /etc/openvpn/openvpn-status.log
./4_create_rsync_user.sh $NEWCLIENT rsync|ftp
WEEWX_USER=weewx
sudo su $WEEWX_USER
sudo su
660", GROUP="weewx", SYMLINK+="vp2", TAG+="systemd", ENV{SYSTEMD_WANTS}="weewx.service"
sudo vi root/skins/Bootstrap/skin.conf
cd
cd /srv/weewx/
sudo vi root/skins/Bootstrap/skin.conf
sudo vi root/weewx.conf
sudo update-rc.d weewx defaults 98
sudo mkdir -p /srv/weewx/run
sudo chown -R weewx:weewx /srv/weewx
root/bin/wee_device --set-interval=5
root/bin/wee_device --info
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
vi root/weewx.conf
sudo vi root/weewx.conf
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ls
root/bin/wee_reports 
ifconfig
sudo apt-get update
sudo apt-get dist-upgrade
sudo reboot -h now
sudo service weewx stop
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
su pi
sudo passwd pi
sudo passwd meteor
sudo vi /etc/environment
sudo service weewx stop
sudo su $WEEWX_USER
ls
cd /home/meteor/meteoroi_scripts && sudo ./rasp06_init_db_backup.sh
vi ./rasp06_init_db_backup.sh
cd
sudo su weewx -c "/srv/weewx/root/backup.sh"
ls
sudo cp weewx_cron /etc/cron.d/weewx
sudo vi /etc/cron.d/weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo service weewx stop
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo shutdown -h now
ifconfig
service weewx stop
sudo service weewx stop
ifconfig
sudo service openvpn stop
sudo apt-get update
sudo apt-get dist-upgrade
sudo service openvpn stop
sudo service weewx stop
ll
sudo passwd pi
sudo passwd meteor
sudi vi /etc/environment 
sudo vi /etc/environment 
sudo su
sudo reboot -h now
sudo service weewx stop
sudo service openvpn stop
ifconfig 
sudo su
ifconfig
WEEWX_USER=weewx
sudo su $WEEWX_USER
sudo su
cat /etc/udev/rules.d/vpro.rules
sudo vi 
sudo vi /srv/weewx/root/skins/Bootstrap/skin.conf
sudo vi /srv/weewx/root/weewx.conf
sudo mkdir -p /srv/weewx/run
sudo chown -R weewx:weewx /srv/weewx
shutdown
sudo shutdown
sudo shutdown -h now
ls
rm -rf /etc/openvpn/SLED430.key
sudo rm -rf /etc/openvpn/SLED430.key
sudo rm -rf /etc/openvpn/SLED430.crt
vi /etc/openvpn/MeteorOI.conf 
rm -rf /etc/openvpn/MeteorOI.conf 
sudo rm -rf /etc/openvpn/MeteorOI.conf 
ll
ll /etc/open
ll /etc/openvpn/
sudo rm -rf /etc/openvpn/MeteorOI.ovpn 
ll /etc/openvpn/
ifconfig
service openvpn restart 
sudo service openvpn restart 
ifconfig
sudo apt-get update
sudo apt-get dist-upgrade
man passwd
ll
cd meteoroi_scripts/
ll
cp rasp01_change_hostname.sh rasp00_change_password.sh 
vi rasp00_change_password.sh 
sudo vi /etc/environment 
sudo su
vi rasp00_change_password.sh 
sudo su
su weewx 
su pi
vi rasp00_change_password.sh 
sudo su
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ifconfig
pip install -U pip
apt-get install pip
sudo apt-get install pip
sudo apt-get install python-pip
sudo pip install fabric2
python --version
sudo pip install -U pip
python --version
pip --version
sudo pip install fabric2
apt-cache search ffi
apt-cache search cffi
sudo apt-get install libffi-dev
sudo pip install fabric2
vi setup.py
pip freeze
pip search jinja
pip install jinja
sudo pip install jinja
sudo pip freeze
vi setup.py
chmod +x setup.py 
./setup.py 
vi setup.py
./setup.py 
vi ./setup.py 
vi setup.py
fab2 setup.py 
mv setup.py fabfile.py
fab2 fabfile.py 
fab2
vi setup.py
vi fabfile.py 
fab2
vi fabfile.py 
fab2
vi fabfile.py 
fab test
fab2 test
vi fabfile.py 
fab2 test
vi fabfile.py 
fab2 test
vi fabfile.py 
fab2 test
vi fabfile.py 
fab2 test
vi fabfile.py 
fab2 --help
vi .fabric.py
vi .fabric.json
vi .fabric.yaml
vi .fabric.py
vi fabfile.py 
fab2 --help
fab2 test
vi fabfile.py 
fab2 test
vi fabfile.py 
fab2 test
ll
vi fabfile.py 
fab2 test
vi fabfile.py 
vi fabfile.py
fab2 set_sys_env
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 set_sys_env 
fab2 setsysenv
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi .fabric.yaml
fab2 setSysEnv
vi .fabric.yaml
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
cat /etc/environment 
vi fabfile.py
vi .fabric.yaml
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
vi .fabric.yaml
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
fab2 setSysEnv
vi fabfile.py
vi .fabric.yaml
ls
vi .fabric.yaml
vi fabfile.py
vi meteoroi_scripts/rasp00_change_password.sh 
vi fabfile.py
fab2 initUserHost
vi fabfile.py
fab2 initUserHost
vi fabfile.py
fab2 initUserHost
vi fabfile.py
vi meteoroi_scripts/rasp00_change_password.sh 
sudo apt-get dist-upgrade
fab2 initUserHost
ls
sudo shutdown -h now
df -h
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
sudo su $WEEWX_USER
cd /etc/nginx/sites-available/
ll
cp default 
cp default weewx
sudo cp default weewx
vi weewx 
sudo vi weewx 
cd ..
#ln -s sites-available/weewx sites-enabled/weewx
cd sites-enabled/
ll
sudo ln -s ../sites-available/weewx weewx
ll
cd ..
ll sites-*
sudo rm -rf sites-enabled/default 
ll sites-*
sudo service nginx reload
cd sites-available/
sudo vi weewx 
sudo service nginx reload
cd
sudo mysql -u root -p6DI+mrlnTW
cd /home/meteor/meteoroi_scripts && sudo ./rasp06_init_db_backup.sh
vi rasp06_init_db_backup.sh 
cd /home/meteor/meteoroi_scripts && sudo ./rasp06_init_db_backup.sh
vi rasp06_init_db_backup.sh 
cd
sudo su weewx -c "/srv/weewx/root/backup.sh"
ll /srv/weewx/backups/
sudo rm -rf /srv/weewx/backups/weewx_NDLP1520.sql
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
sudo shutdown -h now
sudo su $WEEWX_USER
sudo shutdown -h now
cd /srv/weewx/
ls
cd root/
vi weewx.conf
sudo vi weewx.conf
apt-cache search php
apt-cache search php | grep ^php

sudo pip install php7.0 php7.0-fpm php7.0-cli php7.0-opcache php7.0-mbstring php7.0-curl php7.0-xml php7.0-gd php7.0-mysql
sudo apt-get install php7.0 php7.0-fpm php7.0-cli php7.0-opcache php7.0-mbstring php7.0-curl php7.0-xml php7.0-gd php7.0-mysql
sudo apt-get update
sudo apt-get install php7.0 php7.0-fpm php7.0-cli php7.0-opcache php7.0-mbstring php7.0-curl php7.0-xml php7.0-gd php7.0-mysql
vi /etc/php/7.0/fpm/php.ini
sed -i 's/^;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' /etc/php/7.0/fpm/php.ini
sudo sed -i 's/^;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' /etc/php/7.0/fpm/php.ini
sudo sed -i 's/# server_names_hash_bucket_size/server_names_hash_bucket_size/' /etc/nginx/nginx.conf
sudo vi /etc/nginx/sites-available/weewx 
ll
cd /etc/nginx/
ll
sudo mkdir inc
ll
cd inc/
sudo vi phpmyadmin.conf
cd ..
ll
ll snippets/
sudo vi inc/phpmyadmin.conf
cat fastcgi_params 
sudo vi inc/phpmyadmin.conf
vi snippets/fastcgi-php.conf 
vi fastcgi.conf 
ll
dif fastcgi.conf fastcgi_params 
diff fastcgi.conf fastcgi_params 
sudo vi inc/phpmyadmin.conf
sudo vi sites-available/weewx 
nginx -t
sudo nginx -t
sudo vi sites-available/weewx 
sudo mysql -u root -p6DI+mrlnTW
service --help
service --status-all
service php7.0-fpm restart
sudo service php7.0-fpm restart
service --status-all
sudo apt-get install phpmyadmin
ifconfig
service nginx reload
sudo service nginx reload
ll
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo vi inc/phpmyadmin.conf
cat /etc/nginx/snippets/fastcgi-php.conf
sudo vi inc/phpmyadmin.conf
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
ll /usr/share/phpmyadmin/
ls -ali /usr/share/phpmyadmin/
ls -ali /usr/share/phpmyadmin/js
sudo vi inc/phpmyadmin.conf
nginx -t
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi sites-available/weewx 
sudo vi inc/phpmyadmin.conf
sudo vi sites-available/weewx 
tail -f /var/log/nginx/*.log
sudo tail -f /var/log/nginx/*.log
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo tail -f /var/log/nginx/*.log
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo tail -f /var/log/nginx/*.log
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
sudo vi inc/phpmyadmin.conf
sudo vi /etc/php/7.0/fpm/php.ini 

sudo vi inc/phpmyadmin.conf
sudo nginx -t
sudo service nginx reload
cd sites-available/
ll
sudo vi phpmyadmin
cd ..
ll
vi nginx.conf 
sudo ln -s sites-available/phpmyadmin sites-enabled/phpmyadmin
nginx -t
sudo nginx -t
sudo service nginx reload
sudo vi sites-available/phpmyadmin 
sudo service nginx restart
sudo vi sites-available/phpmyadmin 
ifconfig
sudo vi sites-available/phpmyadmin 
sudo vi sites-enabled/phpmyadmin 
sudo vi sites-enabled/phpmyadmin
cd sites-enabled/
ll
rm phpmyadmin
sudo rm phpmyadmin
sudo ln -s /etc/nginx/sites-available/phpmyadmin phpmyadmin
sudo nginx -t
sudo service nginx reload
ll
cd
ll
cd meteoroi_scripts/
ll
vi rasp05_init_db_access.sh
ll
rm VPN_SLED430.tar.gz 
ll
ll root/
rm -rf root/tmp_vpn/SLED430/
sudo rm -rf root/tmp_vpn/SLED430/
ll
vi rasp00_change_password.sh
./rasp00_change_password.sh 
sudo ./rasp00_change_password.sh 
vi rasp00_change_password.sh
sudo ./rasp00_change_password.sh 
echo $STATION_ID
vi rasp00_change_password.sh
sudo ./rasp00_change_password.sh 
vi rasp00_change_password.sh
sudo -c 'echo $STATION_ID'
sudo ' $STATION_ID'
sudo 'echo $STATION_ID'
sudo echo $STATION_ID
vi rasp00_change_password.sh
sudo ./rasp00_change_password.sh 
man sudo
sudo -E ./rasp00_change_password.sh 
vi rasp00_change_password.sh
sudo -E ./rasp00_change_password.sh 
ll
mv rasp06_init_db_backup.sh rasp07_init_db_backup.sh
cp rasp07_init_db_backup.sh rasp06_setup_weewx.sh
ll
vi rasp06_setup_weewx.sh
cat *
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh 
vi rasp06_setup_weewx.sh
echo $STATION_ID_LOWERC 
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh 
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh 
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh 
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh 
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
vi rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
sudo ./rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
sudo ./rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
vi rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
sudo vi /srv/weewx/root/weewx.conf
sudo ./rasp06_setup_weewx.sh
sudo vi /srv/weewx/root/weewx.conf
vi /srv/weewx/root/weewx.conf
vi rasp06_setup_weewx.sh
vi /srv/weewx/root/weewx.conf
vi rasp06_setup_weewx.sh
ll
vi rasp07_init_db_backup.sh
vi rasp05_init_db_access.sh 
vi rasp04_send_ssh_key.sh 
ll
cd /srv/weewx/
ll
ll backups/
ll
ll root/
tar -czvf XXX000_root.tar.gz root/
ll
mv XXX000_root.tar.gz /root/
mv XXX000_root.tar.gz ~/
cd
ll
sudo shutdown -h now
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
sudo shutdown -h now
sudo i2cdetect -y 1
ll /etc/nginx/modules-enabled/
ll /etc/nginx/sites-enabled/
ll /etc/nginx/sites-enabled/phpmyadmin 
cat /etc/nginx/sites-enabled/phpmyadmin 
sudo mysql -u root -p6DI+mrlnTW
apt-get update
sudo apt-get update
sudo apt-get dist-upgrade
sudo reboot -h now
cat /sys/class/net/wlan0/operstate
cat /sys/class/net/wlan0/carrier
cat /sys/class/net/eth0
cat /sys/class/net/eth0/operstate 
ll
cd meteoroi_scripts/
ll
vi rasp06_setup_weewx.sh
./rasp06_setup_weewx.sh
sudo ./rasp06_setup_weewx.sh
vi rasp06_setup_weewx.sh
ll
chmod + rasp06_setup_weewx.py 
ll
chmod +x rasp06_setup_weewx.py 
ll
./rasp06_setup_weewx.py
apt-get install python
sudo apt-get install python
ll /bin/python
whereis python
ll /usr/bin/python
./rasp06_setup_weewx.py
sudo ./rasp06_setup_weewx.py
pip --help
pip search jinja
sudo ./rasp06_setup_weewx.py
whereis pip
vi /etc/pip.conf 
pip install jinja2
sudo pip install jinja2
sudo ./rasp06_setup_weewx.py
whereis pip
whereis jinja
whereis jinja2
whereis jinja1.2
whereis jinja12
python3.5
sudo apt-get install python3-pip
sudo apt-get install python3-jinja2
sudo ./rasp06_setup_weewx.py
chown weewx:meteor /srv/weewx/root/weewx.conf
sudo chown weewx:meteor /srv/weewx/root/weewx.conf
ll /srv/weewx/root/weewx.conf
sudo chmod g+w weewx:meteor /srv/weewx/root/weewx.conf
sudo chmod g+w /srv/weewx/root/weewx.conf
ll /srv/weewx/root/weewx.conf
sudo ./rasp06_setup_weewx.py
pwd
ll
mkdir templates
cp /srv/weewx/root/weewx.conf templates/weewx.conf.tpl
sudo ./rasp06_setup_weewx.py
ll
ll templates/
sudo ./rasp06_setup_weewx.py
vi station.json
sudo ./rasp06_setup_weewx.py
ll
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
sudo ./rasp06_setup_weewx.py
diff templates/weewx.conf.tpl test.conf 
ll
rm rasp06_setup_weewx.sh
vi Makefile
make test
vi Makefile
make test
vi Makefile
make test
vi Makefile
make
make test
vi Makefile
make test
make all
vi Makefile
make all
vi Makefile
make all
vi Makefile
make all
ll
l
ls
ls -l
ls
cat /etc/environment 
cp /etc/environment templates/environment.tpl
cp /etc/bash.bashrc templates/bash.bashrc.tpl
cp rasp06_setup_weewx.py rasp00_bootstrap.py
cp rasp00_bootstrap.py utils/utils.py
touch utils/__init__.py
make rasp06
ll /srv/weewx/root/
ll templates/
ll
make bootstrap
ll
cd meteoroi_scripts/
ll
ll /etc/environment*
diff /etc/environment /etc/environment.20190317224057
diff /etc/environment /etc/environment.20190317224057 templates/environment.tpl 
diff /etc/environment templates/environment.tpl 
ll
diff /etc/environment environment.test
diff /etc/bash.bashrc bash.bashrc.test 
sudo shutdown -h now
echo $STATION_ID_LOWERC 
sudo su $WEEWX_USER
ll
cd
ll
ifconfig
ip route
ssh root@10.8.0.1
ssh root@10.8.0.2
tail -f /var/log/auth.log
sudo tail -f /var/log/auth.log
sudo mv json /srv/weewx/root/skins/Bootstrap/
sudo vi /srv/weewx/root/skins/Bootstrap/skin.conf 
sudo chown -R weewx:weewx /srv/weewx/root/skins/Bootstrap/
tar -xzvf VPN_XXX000.tar.gz 
ll
ll root/
ll root/tmp_vpn/XXX000/
ll /etc/openvpn/
ll /etc/openvpn/client/
ll /etc/openvpn/server/
ifconfig
cp root/tmp_vpn/XXX000/* /etc/openvpn/
sudo cp root/tmp_vpn/XXX000/* /etc/openvpn/
sudo service openvpn restart 
sudo tail -f /var/log/nginx/*.log
tail -f /var/log/syslog
sudo tail -f /var/log/syslog
ifconfig
openvpn --help
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
cd /etc/openvpn/
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
sudo vi /etc/openvpn/MeteoR_OI.conf 
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
sudo vi /etc/openvpn/MeteoR_OI.conf 
ping vpn.meteor-oi.re
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
lls
ll
vi MeteoR_OI.conf
sudo vi MeteoR_OI.conf
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
sudo vi MeteoR_OI.conf
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
sudo vi MeteoR_OI.conf
sudo openvpn --config /etc/openvpn/MeteoR_OI.conf 
sudo service openvpn restart 
tail -f /var/log/syslog
sudo tail -f /var/log/syslog
ifconfig
sudo ll
sudo ls -l
rm MeteoR_OI.ovpn
sudo rm MeteoR_OI.ovpn
sudo cp MeteoR_OI.conf MeteoR_OI.ovpn
ll
sudo service openvpn restart 
sudo tail -f /var/log/syslog
ifconfig
ip addr
sudo reboot -h now
ip addr
sudo shutdown -h now
lsusb
ls /dev/vp2 
ls
./vp2_set_EU.py 
vi vp2_set_EU.py 
cd /srv/weewx/virtualenv && source bin/activate
cd -
./vp2_set_EU.py 
python vp2_set_EU.py 
vi vp2_set_EU.py 
ifconfig
cat /etc/openvpn/MeteoR_OI.ovpn 
sudo su $WEEWX_USER
ll
cd meteoroi_scripts/
ll
vi rasp06_setup_weewx.py 
vi station.json 
ll
cd templates/
ll
vi weewx.conf.tpl 
vi ../Makefile 
cd ..
make clean
vi ../Makefile 
vi Makefile 
make clean
vi Makefile 
make clean
vi Makefile 
make clean
vi Makefile 
ll
vi rasp00_bootstrap.py 
vi rasp06_setup_weewx.py 
vi station.json 
ll
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
ll
sudo vi rasp04_send_ssh_key.sh 
man ssh
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
echo $STATION_ID_LOWERC 
sudo vi rasp04_send_ssh_key.sh 
sudo echo $STATION_ID_LOWERC 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
sudo echo $STATION_ID_LOWERC 
vi /etc/environment
vi /etc/bash.bashrc
cat /etc/bash.bashrc
echo $SHELL
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
vi /etc/profile
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo ./rasp04_send_ssh_key.sh 
ll
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
sudo ./rasp04_send_ssh_key.sh 
ll
sudo vi rasp04_send_ssh_key.sh 
sudo ./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
./rasp04_send_ssh_key.sh 
sudo ./rasp04_send_ssh_key.sh 
sudo vi rasp04_send_ssh_key.sh 
sudo su $WEEWX_USER
cd
sudo tail -f /var/log/syslog
cd
wget http://weewx.com/downloads/weewx-3.9.1.tar.gz
sudo shutdown -h now
sudo su $WEEWX_USER
ll
cd meteoroi_scripts/
ll
cd ..
ll
tar xzvf weewx-3.9.1.tar.gz
ll
cd weewx-3.9.1/
./setup.py build
ls
cd /srv/weewx/virtualenv && source bin/activate
cd -
./setup.py build
ll
vi setup.cfg 
ll /srv/weewx/root/
vi setup.cfg 
sudo ./setup.py install
sudo chown -R weewx:weewx /srv/weewx
deactivate 
cd /home/
cd
cp meteoroi_scripts/templates/weewx.conf.tpl /srv/weewx/root/
sudo cp meteoroi_scripts/templates/weewx.conf.tpl /srv/weewx/root/
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service openvpn stop
sudo service openvpn start
sudo service weewx stop
sudo chmod g+w /srv/weewx/root/weewx.conf
sudo chmod g+w /srv/weewx/root/weewx.conf.tpl 
sudo chown -R weewx:weewx /srv/weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
uname -a
apt --version
sudo apt-get update
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
cp /srv/weewx/root/weewx.conf.tpl meteoroi_scripts/templates/
sudo shutdown -h now
sudo apt-get update
sudo apt-get dist-upgrade
sudo reboot -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo service weewx stop
cd meteoroi_scripts/templates/
vi weewx.conf.tpl 
sudo shutdown -h now
cd meteoroi_scripts/
vi rasp00_bootstrap.py 
vi rasp02_get_vpn_files.sh 
sudo vi rasp02_get_vpn_files.sh 
sudo vi /etc/udev/rules.d/vpro.rules
vi rasp05_init_db_access.sh 
vi rasp06_setup_weewx.py 
sudo vi templates/weewx.conf.tpl 
sudo shutdown -h now
vi .ssh/authorized_keys 
cd meteoroi_scripts/templates/
cd ..
vi station.json 
ll templates/
ll /srv/weewx/root/skins/Bootstrap/
vi /etc/openvpn/MeteoR_OI.conf 
sudo vi /etc/openvpn/MeteoR_OI.conf 
sudo service openvpn restart 
ifconfig
ls
ll
cd meteoroi_scripts/
ls
cd templates/
ls
cp /srv/weewx/root/skins/Bootstrap/skin.conf skin.conf.tpl
vi weewx.conf.tpl 
vi skin.conf.tpl 
vi weewx.conf.tpl 
cd ..
ls
vi rasp06_setup_weewx.py 
./rasp06_setup_weewx.py 
vi rasp06_setup_weewx.py 
vi templates/skin.conf.tpl 
./rasp06_setup_weewx.py 
sudo ./rasp06_setup_weewx.py 
ll /srv/weewx/root/skins/Bootstrap/
ll
vi test_skin.conf
sudo ./rasp06_setup_weewx.py 
vi rasp06_setup_weewx.py 
vi station.json 
sudo shutdown -h now
sudo vi templates/weewx.conf.tpl 
ls
cd meteoroi_scripts/
ls
sudo vi templates/weewx.conf.tpl 
vi /srv/weewx/root/weewx.conf
vi /srv/weewx/root/skins/Bootstrap/noaa_statistics.html.tmpl 
vi /srv/weewx/root/weewx.conf
sudo vi templates/weewx.conf.tpl 
sudo shutdown -h now
cd meteoroi_scripts/templates/
ms
ls
ll
cd ..
vi station.json 
ls
ll
vi rasp00_bootstrap.py 
vi rasp06_setup_weewx.py
./rasp06_setup_weewx.py
sudo chown -R weewx:weewx /srv/weewx
./rasp06_setup_weewx.py
sudo ./rasp06_setup_weewx.py
vi rasp06_setup_weewx.py
ll utils/
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo su $WEEWX_USER
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
cd meteoroi_scripts/
ls
sudo ./rasp06_setup_weewx.py 
vi station.json 
sudo ./rasp06_setup_weewx.py 
vi station.json 
sudo ./rasp06_setup_weewx.py 
vi station.json 
sudo ./rasp06_setup_weewx.py 
apt-get update
sudo apt-get update
sudo apt-get dist-upgrade
cat /etc/nginx/sites-enabled/phpmyadmin 
sudo vi /boot/config.txt
sudo vi /etc/modules
sudo shutdown -h now
sudo apt-get update
sudo apt-get dist-upgrade
grep -rl stretch /etc/apt/ | sudo xargs sed -i 's/stretch/buster/g'
sudo apt-get update
sudo rpi-update
sudo apt-get remove apt-listchanges
sudo apt dist-upgrade
sudo apt purge timidity lxmusic gnome-disk-utility deluge-gtk evince wicd wicd-gtk clipit usermode gucharmap gnome-system-tools pavucontrol
sudo apt autoremove -y
sudo apt autoclean
sudo apt-get clean
df -h
sudo reboot
ip -4 a
cat /etc/nginx/sites-enabled/phpmyadmin 
sudo i2cdetect -y 1
uname -a
wget http://www.weewx.com/downloads/weewx-3.9.2.tar.gz
ls
ll
tar -xzf weewx-3.9.2.tar.gz 
ll
meld weewx-3.9.1/ weewx-3.9.2/
diff weewx-3.9.1/setup.cfg weewx-3.9.2/setup.cfg 
vi weewx-3.9.2/setup.cfg
cd /srv/weewx/virtualenv && source bin/activate && cd -
ls
cd weewx-3.9.2
./setup.py build
sudo ./setup.py install 
./setup.py install 
sudo chown -R weewx:weewx /srv/weewx
./setup.py install 
ls /srv/weewx/root/
ls /srv/weewx/root/bin/
sudo chown -R weewx:weewx /srv/weewx
./setup.py install 
sudo su $WEEWX_USER
deactivate 
ll
cd 
cd /srv/weewx/root/

sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su $WEEWX_USER
sudo apt-get install default-libmysqlclient-dev
sudo su $WEEWX_USER
sudo apt-cache mysql dev
sudo apt-cache search mysql dev
sudo apt-cache search mysql
sudo apt-cache search libmaria
apt-get install libmariadbclient-dev
sudo apt-get install libmariadbclient-dev
sudo apt-get install libmariadb-dev
sudo apt-get remove default-libmysqlclient-dev
sudo apt-get autoremove
sudo su $WEEWX_USER
sudo apt-get install libmariadbclient-dev libmariadb-dev
sudo ln -s /usr/bin/mariadb_config /usr/bin/mysql_config
sudo su $WEEWX_USER
sudo apt-get install default-libmysqlclient-dev
sudo su $WEEWX_USER

sudo su $WEEWX_USER
apt-get install python-dev
sudo apt-get install python-dev
ls
c
cd
#virtualenv -p python2.7 test
ll
virtualenv -p python2.7 test
cd test/
ls
source bin/activate
pip install mysql-python
vi /usr/include/mariadb/mysql.h 
sudo vi /usr/include/mariadb/mysql.h 
pip install mysql-python
sudo apt-get install lsb-release 
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo reboot -h now
sudo su $WEEWX_USER
sudo chown -R weewx:weewx /srv/weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
ps aux | grep weewx
kill -9 20444
sudo kill -9 20444
ps aux | grep weewx
echo "DROP DATABASE IF EXISTS  weewx_${STATION_ID};
CREATE DATABASE weewx_${STATION_ID};
FLUSH PRIVILEGES;" | sudo mysql -u root -p6DI+mrlnTW
sudo su $WEEWX_USER
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ps aux | grep weewx
kill -9 21005
sudo kill -9 21005
ll /srv/weewx/run/weewx.pid
rm /srv/weewx/run/weewx.pid
sudo rm /srv/weewx/run/weewx.pid
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ls
sudo su $WEEWX_USER
ls
cd meteoroi_scripts/
ls
cd templates/
ls
vi weewx.conf.tpl
cd ..
ls
vi station.json 
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
cat /etc/init.d/weewx /srv/weewx/root/util/systemd/weewx.service 
cat  /srv/weewx/root/util/systemd/weewx.service 
cat /etc/init.d/weewx 
cat  /srv/weewx/root/util/systemd/weewx.service 
cat /srv/weewx/root/bin/weewxd 
cp /etc/init.d/weewx ./weewx.initd
cat weewx.initd 
sudo update-rc.d -f weewx remove
ll /etc/init.d/
less /etc/init.d/weewx 
sudo update-rc.d -f weewx remove
ll /etc/init.d/
sudo rm /etc/init.d/weewx 
service --status-all
cat  /srv/weewx/root/util/systemd/weewx.service 
vi  /srv/weewx/root/util/systemd/weewx.service 
sudo vi  /srv/weewx/root/util/systemd/weewx.service 
cat  /srv/weewx/root/util/systemd/weewx.service 
ll /srv/weewx/root/bin/weewxd
ll /srv/weewx/root/weewx.conf
sudo cp /srv/weewx/root/util/systemd/weewx.service /etc/systemd/system/
sudo systemctl start weewx
systemctl daemon-reload
df -h
sudo vi /etc/systemd/system/weewx.service 
systemctl daemon-reload weewx
systemctl daemon-reload
cat /etc/systemd/system/* | grep PolicyKit1
cat /etc/systemd/system/*/* | grep PolicyKit1
sudo vi /etc/systemd/system/weewx.service 
systemctl status
systemctl status weewx
systemctl stop weewx
systemctl status weewx
systemctl status nginx.service
systemctl status weewx.service 
systemctl restart nginx.service
systemctl status weewx
systemctl status nginx.service
sudo rm /etc/systemd/system/weewx.service 
systemctl daemon-reload
sudo systemctl daemon-reload
sudo cp /srv/weewx/root/util/systemd/weewx.service /etc/systemd/system/
sudo vi /etc/systemd/system/weewx.service 
sudo systemctl daemon-reload
sudo systemctl start weewx
sudo systemctl status
sudo systemctl status weewx.service 
sudo systemctl stop weewx.service 
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo vi /etc/systemd/system/weewx.service 
cat /etc/systemd/system/weewx.service 
ll /srv/weewx/run/weewx.pid
rm /srv/weewx/run/weewx.pid
sudo rm /srv/weewx/run/weewx.pid
sudo systemctl daemon-reload
sudo systemctl start weewx
sudo systemctl restart weewx
ls /srv/weewx/run/
sudo iwlist wlan0 scan
systemctl stop weewx
sudo systemctl stop weewx
ls
cd meteoroi_scripts/
ll
vi rasp10_weewx_cleanup_restart.sh
ll
chmod +x rasp10_weewx_cleanup_restart.sh 
ll
./rasp10_weewx_cleanup_restart.sh 
vi rasp10_weewx_cleanup_restart.sh
./rasp10_weewx_cleanup_restart.sh
sudo systemctl stop weewx
cd /srv/weewx/root/
ls
vi weewx.conf 
ls
man scp
ll
cd ..
ll
ll backups/
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su weewx -c "/srv/weewx/root/backup.sh"
ll /srv/weewx/backups/
sudo vi /etc/cron.d/weewx 
ll /srv/weewx/backups/
sudo vi /etc/cron.d/weewx 
tail -f /srv/weewx/backups/cron_clone.log 
sudo vi /etc/cron.d/weewx 
tail -f /srv/weewx/backups/cron_clone.log 
sudo vi /etc/cron.d/weewx 
date
sudo vi /etc/cron.d/weewx 
tail -f /srv/weewx/backups/cron_clone.log 
sudo vi /etc/cron.d/weewx 
tail -f /srv/weewx/backups/cron_clone.log 
sudo vi /etc/cron.d/weewx 
vi root/clone_data.sh 
sudo vi root/clone_data.sh 
sudo vi /etc/cron.d/weewx 
sudo systemctl stop weewx
cd ~/meteoroi_scripts/ && ./rasp10_weewx_cleanup_restart.sh
cd -
ll
ll backups/
rm -rf  backups/weewx_XXX000.sql 
sudo rm -rf  backups/weewx_XXX000.sql 
ll root/public_html/
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ll
rm -rf test
ll
df -h
sudo apt-get clean
df -h
rm -rf weewx-3.8.0 weewx-3.9.1 weewx-3.9.1.tar.gz weewx-3.9.2.tar.gz weewx-3.9.2
df -h
ll
rm -rf weewx.initd
cat weewx_cron
ll root/tmp_vpn/XXX000/
ll
rm -rf ./root/
ll
cat fabfile.py 
ll
cd meteoroi_scripts/
ll
ll root/
ll root/tmp_vpn/
rm -rf root
sudo rm -rf root
ll
cat Makefile 
ll
cd /srv/weewx/
ll
rm v2.24-meteoroi-10.tar.gz
ll
ll scripts/
ll backups/
rm weewx_XXX000.sql
sudo rm backups/weewx_XXX000.sql
ll
cd root/
ll
sudo rm weewx.conf.20191123112317
sudo rm -rf bin.20190202154758 bin.20190609151213 bin.20191123112315
ll
ll public_html/
df -h
ls
cat /etc/cron.d/weewx 
ls
ll
vi clone_data.sh
sudo vi clone_data.sh
ll
chmod +x clone_data.sh 
chmod +x clone_data.sh
sudo chmod +x clone_data.sh
sudo chown -R weewx:weewx /srv/weewx
ll
cd /home/meteor/meteoroi_scripts && ./rasp10_weewx_cleanup_restart.sh
sudo su $WEEWX_USER
llt /srv/weewx/backups/weewx_XXX000.sql 
ll /srv/weewx/backups/weewx_XXX000.sql 
vi /etc/cron.d/weewx 
vi /srv/weewx/root/backup.sh 
vi /etc/cron.d/weewx 
vi /srv/weewx/root/backup.sh 
sudo vi clone_data.sh
vi /srv/weewx/root/clone_data.sh 
sudo vi /srv/weewx/root/clone_data.sh 
sudo su $WEEWX_USER
ls
sudi vi /etc/cron.d/weewx 
sudo vi /etc/cron.d/weewx 
sudo tail -f /var/log/syslog  -n 50
vi /home/meteor/meteoroi_scripts/station.json
cd /home/meteor/meteoroi_scripts && sudo make bootstrap
sudo su
ip -4 a
sudo su $WEEWX_USER
sudo su
cd /home/meteor/meteoroi_scripts && sudo ./rasp07_init_db_backup.sh
sudo su weewx -c "/srv/weewx/root/backup.sh"
sudo i2cdetect -y 1
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo systemctl restart weewx
sudo tail -f /var/log/syslog  -n 50 | grep weewx
apt-get clean
sudo apt-get clean
df -h
cd
ls -ali
ls -alih
df -h
exit
sudo shutdown -h now
sudo service weewx stop
sudo mysql -f --show-warnings weewx_MTG320 < weewx_MTG320.sql 
sudo mysql -f --show-warnings weewx_MTG320 < /srv/weewx/rootweewx_MTG320.sql 
sudo mysql -f --show-warnings weewx_MTG320 < /srv/weewx/root/weewx_MTG320.sql 
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
wee_device --logger-summary=/var/tmp/summary.txt
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service mysql stop
sudo shutdown -h now
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service mysql stop
sudo shutdown -h now
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
history | grep mysql
sudo mysql -u root -p6DI+mrlnTW
exit
ls
ls -l
sudo mysql -f --show-warnings weewx_MTG320 < weewx_MTG280_outTemp_rain_barometer2.sql 
sudo mysql -u root -p6DI+mrlnTW
exit
sudo mysql -f --show-warnings weewx_MTG320 < weewx_MTG280_outTemp_rain_barometer2.sql 
sudo mysql -u root -p6DI+mrlnTW
sudo service weewx stop
sudo service mysql stop
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo shutdown -h now
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
pwd
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service mysql stop
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop

sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo su -
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo mysql -u root -p6DI+mrlnTW
cat meteoroi_scripts/station.json 
version
lsb_release -a
sudo tail -f /var/log/syslog  -n 50 | grep weewx
exit
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo tail -f /var/log/syslog  -n 100 | grep weewx
exit
sudo tail -f /var/log/syslog  -n 100 | grep weewx
sudo tail -f /var/log/syslog  -n 1000 | grep weewx
exit
sudo tail -f /var/log/syslog  -n 1000 | grep weewx
exit
su - weewx
sudo dpkg-reconfigure locales
sudo tail -f /var/log/syslog  -n 1000 | grep weewx
sudo mysql -u root -p6DI+mrlnTWservice --status-all
service --status-all
cd /
sudo find . -name 'mysql' -print
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo /srv/bin/weewx/root/bin/wee_device --clear-memory
sudo /srv/weewx/root/bin/wee_device --clear-memory
sudo /srv/weewx/root/bin/wee_device --dump
su - weewx
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo /srv/weewx/root/bin/wee_device --clear-memory
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ls -l /srv/weewx
ls -altr
cd .ssh
ls
vim authorized_keys
ls -altr
vim known_hosts
cd
exit
meteor@RASPNAME:~ $ cat ~/.ssh/authorized_keys 
meteor@MTG320:~ $ cat ~/.ssh/authorized_keys 
ls -al ~/.ssh
su - weewx
sudo passwd weewx
su - weewx
meteor@RASPNAME:~ $ cat ~/.ssh/authorized_keys 
sudo tail -f /var/log/syslog  -n 50 | grep weewx
rsync --archive --stats --compress -e ssh /srv/weewx/root/public_html/ mtg320@obs.meteor-oi.re:/srv/stations/MTG320
exit
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service start
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo tail -f /var/log/syslog  -n 5000 | grep weewx
sudo service ssh status
ssh mtg320@obs.meteor-oi.re
rsync --archive --stats --compress -e ssh /srv/weewx/root/public_html mtg320@obs.meteor-oi.re:/srv/stations/MTG320
ssh meteor@localhost
exit
sudo tail -f /var/log/syslog  -n 50 | grep weewx
exit
cd .ssh
ls -altr
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
ls -altr
sudo su -
cd
sudo su - weewx
sudo tail -f /var/log/syslog  -n 50 | grep weewx
exit
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo mysql -u root
sudo tail -f /var/log/syslog  -n 50 | grep weewx
find . -name 'Template.py' -print
sudo tail -f /var/log/syslog  -n 50 | grep weewx
su - weewx
rsync --archive --stats --compress -e ssh /srv/weewx/root/public_html/ mtg320@obs.meteor-oi.re:/srv/stations/MTG320
cd .ssh
ls -altr
sudo su -
exit
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx restart
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx stop
sudo service mysql stop
sudo update-rc.d
sudo systemctl
sudo systemctl --help
!
sudo tail -f /var/log/syslog  -n 5000
sudo shutdown -h
sudo shutdown -c
sudo shutdown -h now
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo service weewx start
sudo tail -f /var/log/syslog  -n 50 | grep weewx
su - weewx
sudo tail -f /var/log/syslog  -n 50 | grep weewx
sudo tail -f /var/log/syslog  -n 500 | grep weewx
su - weewx
sudo reboot
sudo tail -f /var/log/syslog  -n 500 | grep weewx
ls -l /srv/weewx/root/bin
sudo tail -f /var/log/syslog  -n 500 | grep weewx
vim /src/weewx/root/weewx.conf
vim /srv/weewx/root/weewx.conf
sudo tail -f /var/log/syslog  -n 500 | grep weewx
exit
sudo tail -f /var/log/syslog  -n 500 | grep weewx
sudo service weewx start
sudo tail -f /var/log/syslog  -n 500 | grep weewx
ls -l .ssh
su - weewx
sudo tail -f /var/log/syslog  -n 500 | grep weewx
su - weewx
exit
ls -l
pwd
ls -l meteoroi_scripts
exit
