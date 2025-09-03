#!/bin/bash

# Railway deployment script for Basketball Shot Analyzer
echo "Starting Basketball Shot Analyzer deployment..."

# Install system dependencies if needed
apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0

# Set environment variables for Railway
export PYTHONPATH=/app:$PYTHONPATH
export STREAMLIT_SERVER_PORT=$PORT
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Create necessary directories
mkdir -p ~/.streamlit

# Create Streamlit config with proper port handling
cat > ~/.streamlit/config.toml << EOF
[server]
port = ${PORT:-8000}
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
showErrorDetails = true

[theme]
base = "light"
EOF

echo "Configuration complete. Starting Streamlit..."

# Start the application with proper port handling
echo "Starting Streamlit on port $PORT"
exec streamlit run app.py \
  --server.port "${PORT:-8000}" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false
