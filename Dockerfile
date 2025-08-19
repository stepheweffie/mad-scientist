# Use the official Node.js 20 image with Ubuntu
FROM node:20-bullseye

# Set working directory
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy package files
COPY package*.json ./
COPY wrangler.toml ./

# Install Node.js dependencies (including Wrangler)
RUN npm install
RUN npm install -g wrangler

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Expose the port that Wrangler dev server uses
EXPOSE 8787

# Set environment variables
ENV NODE_ENV=development

# Start the development server
CMD ["wrangler", "dev", "--port", "8787", "--host", "0.0.0.0"]
