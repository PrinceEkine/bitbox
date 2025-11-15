#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies using pip (override poetry)
pip install --upgrade pip
pip install Django==5.2.5
pip install Pillow==10.0.0
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0

# Create necessary directories
mkdir -p static media

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear