#!/usr/bin/env python3
import requests
import sys
import time

def health_check(url, timeout=30, interval=2):
    """Perform health check on the given URL"""
    print(f"🩺 Performing health check on {url}")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Version: {data.get('version', 'unknown')}")
                print(f"   Environment: {data.get('environment', 'unknown')}")
                return True
        except requests.RequestException as e:
            print(f"⏳ Health check failed, retrying... ({e})")
            time.sleep(interval)
    
    print(f"❌ Health check failed after {timeout} seconds")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python health_check.py <url>")
        print("Example: python health_check.py http://localhost:5001")
        sys.exit(1)
    
    url = sys.argv[1]
    success = health_check(url)
    sys.exit(0 if success else 1)