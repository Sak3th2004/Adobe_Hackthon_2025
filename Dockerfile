# Base image with Python and CPU
FROM python:3.10-slim

# Set UTF-8 encoding
ENV PYTHONIOENCODING=UTF-8

# Set work directory
WORKDIR /app

# Copy all files
COPY . .

# Upgrade pip and install required packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run semantic search script
CMD ["python", "main.py"]
