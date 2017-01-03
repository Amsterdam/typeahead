#!/usr/bin/env bash

set -e
set -u

echo '' | sudo echo "bypassing the lecture"

export DOCKER_IP=$(hostname --ip-address)

uwsgi --ini /app/uwsgi.ini