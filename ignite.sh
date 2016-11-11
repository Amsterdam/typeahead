#!/usr/bin/env bash

set -e
set -u

[[  -z  ${CONSUL_ENV}  ]] && CONSUL_ENV=${CONSUL_DEFAULT_ENV}

echo '' | sudo echo "bypassing the lecture"
echo Running in ${CONSUL_ENV} mode
sudo -u consul /usr/local/bin/consul agent --config-dir /etc/consul.d/${CONSUL_ENV} &
uwsgi --ini /app/uwsgi.ini