#!/bin/sh

set -e
cd E_Commerce_API/
# gunicorn E_Commerce_API.wsgi --log-file -
gunicorn E_Commerce_API.wsgi:application --bind 0.0.0.0:8000 --workers 4 --log-file -
