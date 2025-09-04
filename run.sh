#!/bin/bash
# Railway bypass script - looks like bash but runs Python
echo "=== RAILWAY BASH BYPASS ==="

# Unset Railway's problematic environment variables
unset STREAMLIT_SERVER_PORT
unset STREAMLIT_SERVER_ADDRESS
unset STREAMLIT_SERVER_HEADLESS

# Get the port from Railway
ACTUAL_PORT=${PORT:-8080}
echo "Using PORT: $ACTUAL_PORT"

# Run our Python startup script
python3 start.py
