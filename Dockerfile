# Railway-optimized Dockerfile for Basketball Shot Analyzer
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create streamlit config directory (config will be created dynamically by run_app.py)
RUN mkdir -p ~/.streamlit

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV STREAMLIT_SERVER_HEADLESS=true

# Start command using our Python runner that handles PORT properly
CMD ["python", "run_app.py"]
