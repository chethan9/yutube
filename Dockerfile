# Use an official Python runtime as a base image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp via pip
RUN pip install yt-dlp Flask

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for Flask app
EXPOSE 5000

# Define environment variable to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]
