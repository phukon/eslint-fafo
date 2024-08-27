import sys
import os

if len(sys.argv) > 1:
    env = sys.argv[1]
else:
    env = 'dev'
os.environ['SERVER_ENV'] = env

from flask import Flask, request, jsonify
import gzip
import json
from loadEnv import TEST

app = Flask(__name__)

LOG_FILE = 'logs.json'

@app.route('/logs', methods=['POST'])
def receive_logs():
    try:
        compressed_data = request.data
        decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
        logs = json.loads(decompressed_data)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    existing_logs = json.load(f)
                except json.JSONDecodeError:
                    existing_logs = []
        else:
            existing_logs = []

        existing_logs.extend(logs)

        with open(LOG_FILE, 'w') as f:
            json.dump(existing_logs, f, indent=4)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print('🍅', os.getenv("SERVER_ENV"))
    print('🎯', TEST)
    
    app.run(host='0.0.0.0', port=5000)