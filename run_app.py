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
    
    print(f"🚀 Starting Basketball Shot Analyzer on port {port}")
    print(f"📊 Environment check:")
    print(f"   PORT = {os.environ.get('PORT', 'NOT SET')}")
    print(f"   STREAMLIT_SERVER_PORT = {os.environ.get('STREAMLIT_SERVER_PORT', 'NOT SET')}")
    
    # Create dynamic Streamlit config
    streamlit_dir = os.path.expanduser("~/.streamlit")
    os.makedirs(streamlit_dir, exist_ok=True)
    
    config_content = f"""[server]
port = {port}
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
showErrorDetails = true
"""
    
    config_path = os.path.join(streamlit_dir, "config.toml")
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"📝 Created Streamlit config at {config_path}")
    print(f"🎯 Config content:\n{config_content}")
    
    # Build the streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    print(f"🔧 Running command: {' '.join(cmd)}")
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running streamlit: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
