#!/usr/bin/env python3
import os
import shutil
import json
import subprocess
import sys
import time
import requests

def deploy_to_environment(environment, version, port):
    """Deploy application to specified environment"""
    env_folder = f"{environment.lower()}_environment"
    
    print(f"🚀 Starting deployment to {environment} environment...")
    
    # Create environment directory
    os.makedirs(env_folder, exist_ok=True)
    
    # Copy application files
    print("📁 Copying application files...")
    shutil.copytree("app", f"{env_folder}/app", dirs_exist_ok=True)
    
    # Update configuration for the environment
    config_file = f"{env_folder}/app/config.json"
    config_data = {
        "version": version,
        "environment": environment.upper(),
        "features": [
            "Basic Features",
            "User Authentication",
            "Data Processing"
        ]
    }
    
    if environment.upper() == "GREEN":
        # Add new features for green environment
        config_data["features"].extend([
            "Advanced Analytics",
            "Real-time Notifications", 
            "API Gateway"
        ])
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"✅ Deployed version {version} to {environment} environment")
    print(f"🌐 Application will run on port {port}")
    
    return True

def start_environment(environment, port):
    """Start the application in specified environment"""
    env_folder = f"{environment.lower()}_environment"
    
    print(f"▶️ Starting {environment} environment on port {port}...")
    
    # Create start script
    start_script = f"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['PORT'] = '{port}'
from app.app import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port={port}, debug=False)
"""
    
    with open(f"{env_folder}/start.py", 'w') as f:
        f.write(start_script)
    
    print(f"✅ {environment} environment ready to start")
    print(f"💡 Run: cd {env_folder} && python start.py")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python deploy.py <environment> <version> <port>")
        print("Example: python deploy.py BLUE 1.0.0 5000")
        sys.exit(1)
    
    environment = sys.argv[1]
    version = sys.argv[2] 
    port = sys.argv[3]
    
    deploy_to_environment(environment, version, port)
    start_environment(environment, port)