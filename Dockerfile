
# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into container
COPY . .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt || true

# Expose port (change if needed)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
