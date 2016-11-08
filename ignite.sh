#!/usr/bin/env bash

set -e
set -u

echo '' | sudo echo "bypassing the lecture"
sudo -u consul /usr/local/bin/consul agent --config-dir /etc/consul.d &
uwsgi --ini /app/uwsgi.ini