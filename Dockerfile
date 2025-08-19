# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y nodejs npm

# Copy frontend files and build
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Go back to app directory and copy backend files
WORKDIR /app
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]