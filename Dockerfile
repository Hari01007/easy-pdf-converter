# Use slim Python base image
FROM python:3.10-slim

# Install system dependencies including full LibreOffice suite
RUN apt-get update && \
    apt-get install -y \
    libreoffice \
    libreoffice-core \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Start the Flask app with correct host and port binding
CMD ["python", "app.py"]
