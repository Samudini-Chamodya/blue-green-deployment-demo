from flask import Flask, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Load configuration
def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    default_config = {
        "version": "1.0.0",
        "environment": "BLUE",
        "features": ["Basic Features", "User Authentication", "Data Processing"]
    }
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', 
                         version=config['version'],
                         environment=config['environment'],
                         features=config['features'],
                         timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

@app.route('/health')
def health_check():
    config = load_config()
    return jsonify({
        "status": "healthy",
        "version": config['version'],
        "environment": config['environment'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/version')
def get_version():
    config = load_config()
    return jsonify(config)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)