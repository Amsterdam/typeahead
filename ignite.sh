#!/usr/bin/env bash

set -e
set -u

[[  -z  ${CONSUL_ENV}  ]] && CONSUL_ENV=${CONSUL_DEFAULT_ENV}

echo '' | sudo echo "bypassing the lecture"
echo Running in ${CONSUL_ENV} mode
sudo -u consul /usr/local/bin/consul agent --config-dir /etc/consul.d/${CONSUL_ENV} &

while ! nc -z localhost 8500
do
	echo "Waiting for Consul..."
	sleep 0.1
done

sleep 5

uwsgi --ini /app/typeahead/uwsgi.ini