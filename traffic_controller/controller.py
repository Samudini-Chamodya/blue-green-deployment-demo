
from flask import Flask, jsonify, request, render_template_string, Response
import requests
import json
import os
from urllib.parse import urljoin

app = Flask(__name__)

# Traffic configuration
TRAFFIC_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'traffic_flag.txt')
BLUE_URL = "http://localhost:5000"
GREEN_URL = "http://localhost:5001"

def get_active_environment():
    try:
        with open(TRAFFIC_CONFIG_FILE, 'r') as f:
            return f.read().strip().upper()
    except FileNotFoundError:
        # Default to BLUE
        with open(TRAFFIC_CONFIG_FILE, 'w') as f:
            f.write('BLUE')
        return 'BLUE'

def set_active_environment(env):
    with open(TRAFFIC_CONFIG_FILE, 'w') as f:
        f.write(env.upper())

def get_active_url():
    active_env = get_active_environment()
    return BLUE_URL if active_env == 'BLUE' else GREEN_URL

def proxy_request(path, query_string=""):
    target_url = get_active_url()
    url = urljoin(target_url, path)
    if query_string:
        url += "?" + query_string
    
    try:
        # Forward the request to the active environment
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=5
        )
        
        # Create a Flask response object
        response = Response(resp.content, resp.status_code, resp.headers.items())
        return response
    except requests.RequestException as e:
        return f"<h1>Service Unavailable</h1><p>Error connecting to active environment: {str(e)}</p>", 503

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return proxy_request(path, request.query_string.decode('utf-8'))

@app.route('/switch', methods=['POST'])
def switch_traffic():
    data = request.get_json()
    new_env = data.get('environment', '').upper()
    
    if new_env not in ['BLUE', 'GREEN']:
        return jsonify({"error": "Invalid environment. Use BLUE or GREEN"}), 400
    
    # Health check before switching
    target_url = BLUE_URL if new_env == 'BLUE' else GREEN_URL
    try:
        health_response = requests.get(f"{target_url}/health", timeout=5)
        if health_response.status_code == 200:
            set_active_environment(new_env)
            return jsonify({
                "message": f"Traffic switched to {new_env}",
                "previous_environment": get_active_environment(),
                "new_environment": new_env
            })
        else:
            return jsonify({"error": f"{new_env} environment is not healthy"}), 503
    except requests.RequestException:
        return jsonify({"error": f"Cannot connect to {new_env} environment"}), 503

@app.route('/status')
def get_status():
    active_env = get_active_environment()
    blue_status = "unknown"
    green_status = "unknown"
    
    # Check BLUE environment
    try:
        response = requests.get(f"{BLUE_URL}/health", timeout=3)
        blue_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        blue_status = "offline"
    
    # Check GREEN environment  
    try:
        response = requests.get(f"{GREEN_URL}/health", timeout=3)
        green_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        green_status = "offline"
    
    return jsonify({
        "active_environment": active_env,
        "blue_status": blue_status,
        "green_status": green_status,
        "traffic_controller": "running"
    })

@app.route('/admin')
def admin_panel():
    return render_template_string(ADMIN_TEMPLATE)

# Admin Panel Template
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Blue-Green Deployment Controller</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .status { padding: 20px; margin: 20px 0; border-radius: 5px; }
        .blue { background: #e3f2fd; border-left: 5px solid #2196f3; }
        .green { background: #e8f5e8; border-left: 5px solid #4caf50; }
        .active { font-weight: bold; }
        button { padding: 10px 20px; margin: 10px; border: none; border-radius: 5px; cursor: pointer; }
        .btn-blue { background: #2196f3; color: white; }
        .btn-green { background: #4caf50; color: white; }
        .btn-refresh { background: #ff9800; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Blue-Green Deployment Controller</h1>
        <div id="status-container">
            <div class="status">Loading status...</div>
        </div>
        
        <div>
            <button class="btn-blue" onclick="switchEnvironment('BLUE')">Switch to BLUE</button>
            <button class="btn-green" onclick="switchEnvironment('GREEN')">Switch to GREEN</button>
            <button class="btn-refresh" onclick="refreshStatus()">Refresh Status</button>
        </div>
        
        <div>
            <h3>Environment Links:</h3>
            <p><a href="http://localhost:5000" target="_blank">🔵 Blue Environment (Port 5000)</a></p>
            <p><a href="http://localhost:5001" target="_blank">🟢 Green Environment (Port 5001)</a></p>
            <p><a href="http://localhost:8000" target="_blank">🌐 Live Traffic (Port 8000)</a></p>
        </div>
    </div>
    <script>
        async function refreshStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                document.getElementById('status-container').innerHTML = `
                    <div class="status blue ${data.active_environment === 'BLUE' ? 'active' : ''}">
                        🔵 BLUE Environment: ${data.blue_status} ${data.active_environment === 'BLUE' ? '(ACTIVE)' : ''}
                    </div>
                    <div class="status green ${data.active_environment === 'GREEN' ? 'active' : ''}">
                        🟢 GREEN Environment: ${data.green_status} ${data.active_environment === 'GREEN' ? '(ACTIVE)' : ''}
                    </div>
                `;
            } catch (error) {
                console.error('Error refreshing status:', error);
            }
        }
        async function switchEnvironment(env) {
            try {
                const response = await fetch('/switch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ environment: env })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert(`✅ Successfully switched to ${env} environment`);
                    refreshStatus();
                    // Refresh the live traffic page
                    window.open('http://localhost:8000', '_blank');
                } else {
                    alert(`❌ Failed to switch: ${result.error}`);
                }
            } catch (error) {
                alert(`❌ Error switching environment: ${error.message}`);
            }
        }
        // Auto-refresh every 10 seconds
        setInterval(refreshStatus, 10000);
        
        // Initial load
        refreshStatus();
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
