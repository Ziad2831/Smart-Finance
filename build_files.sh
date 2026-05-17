#!/bin/bash
set -e

uv pip install -r requirements.txt
python manage.py collectstatic --noinput

if [ -n "$DATABASE_URL" ]; then
  python manage.py migrate --noinput
fi
