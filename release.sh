#!/bin/bash

set -e

python E_Commerce_API/manage.py migrate
python E_Commerce_API/manage.py createsuperuser --noinput
