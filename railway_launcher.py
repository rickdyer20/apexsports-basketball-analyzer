#!/usr/bin/env python3
"""
Railway-compatible startup script.
Instead of fighting Railway's auto-detection, we'll work with it.
"""

import os
import sys
import subprocess

def main():
    """Start Streamlit with proper port handling for Railway."""
    
    print("=== RAILWAY STREAMLIT LAUNCHER ===")
    
    # Get the port from Railway
    port = os.environ.get('PORT', '8080')
    print(f"Railway PORT environment variable: {port}")
    
    # Railway sets STREAMLIT_SERVER_PORT to "$PORT" (literal string)
    # We need to replace it with the actual port number
    if 'STREAMLIT_SERVER_PORT' in os.environ:
        if os.environ['STREAMLIT_SERVER_PORT'] == '$PORT':
            print("Fixing Railway's STREAMLIT_SERVER_PORT from '$PORT' to actual port")
            os.environ['STREAMLIT_SERVER_PORT'] = port
        else:
            print(f"STREAMLIT_SERVER_PORT already set to: {os.environ['STREAMLIT_SERVER_PORT']}")
    else:
        print("Setting STREAMLIT_SERVER_PORT")
        os.environ['STREAMLIT_SERVER_PORT'] = port
    
    # Set other required environment variables
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    print(f"Starting Streamlit on 0.0.0.0:{port}")
    
    # Start streamlit directly with the correct parameters
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Execute streamlit
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
