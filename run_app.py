#!/usr/bin/env python3
"""
Railway deployment runner for Basketball Shot Analyzer
"""
import os
import subprocess
import sys

def main():
    # Get the port from environment variable, default to 8000
    port = os.environ.get('PORT', '8000')
    
    print(f"Starting Basketball Shot Analyzer on port {port}")
    
    # Build the streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running streamlit: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
