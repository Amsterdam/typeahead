#!/usr/bin/env bash

set -e
set -u

echo '' | sudo echo "bypassing the lecture"

uwsgi --ini /app/uwsgi.ini