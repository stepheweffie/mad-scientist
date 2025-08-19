# Use Python 3.11 with Ubuntu 22.04 for better compatibility
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY local_dev.py ./
COPY src/ ./src/
COPY wrangler.toml ./

# Expose the port that the local dev server uses
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Start the local development server (with mock AI responses)
CMD ["python", "local_dev.py"]
