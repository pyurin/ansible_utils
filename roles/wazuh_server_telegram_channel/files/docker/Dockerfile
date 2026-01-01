FROM python:3.11-slim

WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY telegram_config.py .

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "-u", "app.py"]
