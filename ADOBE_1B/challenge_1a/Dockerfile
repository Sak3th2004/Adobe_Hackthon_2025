FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/input /app/output


CMD ["python", "process_pdfs.py"]