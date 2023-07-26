

all: test test2

bootstrap:
	sudo ./rasp00_bootstrap.py
	sudo reboot -h now

rasp00:
	./rasp00_change_password.sh

rasp01:
	./rasp01_change_hostname.sh

rasp02:
	./rasp02_get_vpn_files.sh

rasp03:
	./rasp03_install_vpn_files.sh

rasp04:
	./rasp04_send_ssh_key.sh

rasp05:
	./rasp05_init_db_access.sh

rasp06:
	sudo ./rasp06_setup_weewx.py

rasp07:
	./rasp07_init_db_backup.sh

clean:
	echo "TODO"
