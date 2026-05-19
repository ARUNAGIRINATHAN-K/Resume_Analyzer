# Use a lightweight official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies needed for compiling packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY . .

# Ensure the uploads directory exists inside the container
RUN mkdir -p uploads

# Expose server port
EXPOSE 5000

# Run using Gunicorn production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
