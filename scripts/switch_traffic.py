#!/usr/bin/env python3
import requests
import sys
import json

def switch_traffic(controller_url, environment):
    """Switch traffic to specified environment"""
    print(f"🔄 Switching traffic to {environment} environment...")
    
    try:
        response = requests.post(
            f"{controller_url}/switch",
            json={"environment": environment},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Traffic successfully switched to {environment}")
            print(f"📊 Response: {data['message']}")
            return True
        else:
            error_data = response.json()
            print(f"❌ Failed to switch traffic: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to traffic controller: {e}")
        return False

def rollback_traffic(controller_url, environment):
    """Rollback traffic to specified environment"""
    print(f"↩️ Rolling back traffic to {environment} environment...")
    return switch_traffic(controller_url, environment)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python switch_traffic.py <controller_url> <environment>")
        print("Example: python switch_traffic.py http://localhost:8000 GREEN")
        sys.exit(1)
    
    controller_url = sys.argv[1]
    environment = sys.argv[2]
    
    success = switch_traffic(controller_url, environment)
    sys.exit(0 if success else 1)