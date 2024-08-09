#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations (if needed)
python manage.py migrate

# Collect static files (if applicable)
python manage.py collectstatic --noinput

