#!/bin/sh

set -e
cd E_Commerce_API/
gunicorn E_Commerce_API.wsgi --log-file -
