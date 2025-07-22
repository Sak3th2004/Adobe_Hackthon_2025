FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set the command to run the main script
CMD ["python", "process_pdfs.py"]
