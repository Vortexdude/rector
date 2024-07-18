#!/bin/bash


set -a
source "${PWD}/app/.env"
set +a
env | grep POSTGRES_*
python3 app/main.py >app/app.log
