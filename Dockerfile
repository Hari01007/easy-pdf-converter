FROM python:3.10-slim

# Install LibreOffice
RUN apt-get update && apt-get install -y libreoffice libreoffice-core libreoffice-writer

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
