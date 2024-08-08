# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmariadb-dev \
    libpq-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Set up a virtual environment
RUN python -m venv venv

# Upgrade pip and install dependencies
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

# Apply database migrations and collect static files (if needed)
# RUN venv/bin/python manage.py migrate
# RUN venv/bin/python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the application
CMD ["venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
