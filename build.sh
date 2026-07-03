#!/usr/bin/env bash
# Build step for Render / Railway: install deps, collect admin static, migrate.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
