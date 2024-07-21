# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /web

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /web/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /web/

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]