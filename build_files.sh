#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install system dependencies
apt-get update && apt-get install -y default-libmysqlclient-dev

# Ensure Python is available
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found"
    exit 1
fi

# Set up a virtual environment for the project
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Deactivate the virtual environment
deactivate
