#!/bin/bash

# Install Python and Pip
if ! command -v python3 &> /dev/null
then
    echo "Python not found. Installing..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Install dependencies
pip3 install -r requirements.txt

# Run migrations (if needed)
python3 manage.py migrate

# Collect static files (if applicable)
python3 manage.py collectstatic --noinput
