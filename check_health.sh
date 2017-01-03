#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

curl -f -s -v http://localhost:8080/health
