#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create the superuser automatically without prompting for input
python manage.py createsuperuser --noinput || true