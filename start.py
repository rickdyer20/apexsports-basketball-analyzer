#!/usr/bin/env python3
"""
Ultra-simple startup script to bypass Railway's Streamlit auto-detection.
This script will explicitly unset Railway's problematic environment variables
and then run our proper startup script.
"""

import os
import subprocess
import sys

def main():
    """Start the application with clean environment variables."""
    
    print("=== RAILWAY BYPASS STARTUP ===")
    
    # Explicitly remove Railway's Streamlit auto-detection variables
    problematic_vars = [
        'STREAMLIT_SERVER_PORT',
        'STREAMLIT_SERVER_ADDRESS',
        'STREAMLIT_SERVER_HEADLESS'
    ]
    
    for var in problematic_vars:
        if var in os.environ:
            print(f"Removing problematic environment variable: {var}={os.environ[var]}")
            del os.environ[var]
    
    # Print environment info
    port = os.environ.get('PORT', '8080')
    print(f"Starting with PORT={port}")
    
    # Now run our actual startup script
    print("Starting run_app.py...")
    try:
        result = subprocess.run([sys.executable, 'run_app.py'], check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
