#!/usr/bin/env bash

set -e
set -u

echo '' | sudo echo "bypassing the lecture"

METADATA_HOST=169.254.169.254
METADATA_PORT=80
METADATA_URL=http://${METADATA_HOST}:${METADATA_PORT}/latest/meta-data/local-ipv4

export DOCKER_IP=$(hostname --ip-address)

#Check connectivity
curl -s -m1 ${METADATA_URL} || exitcode=$?
if [ -n "${exitcode+set}" ]; then
  echo 1
  export DOCKER_EXTERNAL_IP=${DOCKER_IP}
else
  echo 2
  export DOCKER_EXTERNAL_IP=$(curl ${METADATA_URL})
fi

uwsgi --ini /app/uwsgi.ini