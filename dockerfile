# Use an official Python runtime as a parent image
FROM python:3.12-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmysqlclient-dev \
    libpq-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --target /app/dependencies -r requirements.txt

# Second stage: Create a smaller image for runtime
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /app/dependencies /app/dependencies

# Set environment variables for MySQL
ENV MYSQLCLIENT_CFLAGS=-I/usr/include/mysql
ENV MYSQLCLIENT_LDFLAGS=-L/usr/lib/x86_64-linux-gnu

# Copy the rest of the application code into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the PYTHONPATH to include the dependencies
ENV PYTHONPATH=/app/dependencies

# Run Gunicorn when the container launches
CMD ["gunicorn", "--bind", ":8000", "private_info.wsgi:application"]
