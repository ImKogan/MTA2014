# -*- mode: ruby -*-
# vi: set ft=ruby ts=2 sws=2 sw=2:

# How much MTA data to get "short" or "full"
data_size = "short"

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8001

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  config.vm.provision "shell", inline: <<-SHELL

		# TODO(isroelkogan) figure out way to automate insertion
		# of django secret key and api key, defined in
		# ./MTA/django_app/mta/settings.ini

		# setup linux requirements
  	bash /vagrant/MTA/setup/linux-env-setup.sh
		# setup python requirements
		pip3 install -r /vagrant/MTA/requirements.txt
		# setup database
		sudo -u postgres psql -f /vagrant/MTA/setup/db_setup.sql

		# get static data
		bash /vagrant/MTA/setup/get-static.sh

		# make shapefiles from static data
		bash /vagrant/MTA/setup/make-shapefile.sh

	SHELL

  # get mta data to start off with
  if data_size == "full"
		config.vm.provision "shell", inline: <<-SHELL
			bash /vagrant/MTA/setup/get-realtime.sh 100
		SHELL
  elsif data_size == "short"
		config.vm.provision "shell", inline: <<-SHELL
			bash /vagrant/MTA/setup/get-realtime.sh 4
		SHELL
	end

	
	# process realtime data into csv
  config.vm.provision "shell", inline: <<-SHELL
		python3 /vagrant/MTA/gtfs_to_csv_dir.py /vagrant/MTA/data/realtime

		# make db migrations
		bash /vagrant/MTA/setup/migrate.sh
	
		# load static data to db
		bash /vagrant/MTA/setup/load-static-db.sh

		# load realtime data to db
		python3 /vagrant/MTA/django_app/db_2014/trip_to_sql.py /vagrant/MTA/data
	SHELL

	# generate django secret key and update settings.ini
  config.vm.provision "shell", inline: <<-SHELL
	cd /vagrant/MTA/django_app/mta
	python3 manage.py generate_secret_key --replace
	sed -ir '/^SECRET_KEY/s/.*/SECRET_KEY: '"$(cat secretkey.txt)"'/' settings.ini
	while [ $? -ne 0 ]; do
		python3 manage.py generate_secret_key --replace
		sed -ir '/^SECRET_KEY/s/.*/SECRET_KEY: '"$(cat secretkey.txt)"'/' settings.ini
	done
	rm -f secretkey.txt
	rm -f settings.inir
	echo secret key generated
	SHELL
end
