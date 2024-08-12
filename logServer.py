from flask import Flask, request, jsonify
import gzip
import json
import os

app = Flask(__name__)

LOG_FILE = 'logs.json'

@app.route('/logs', methods=['POST'])
def receive_logs():
    try:
        # Read and decompress the logs
        compressed_data = request.data
        decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
        logs = json.loads(decompressed_data)

        # Load existing logs
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    existing_logs = json.load(f)
                except json.JSONDecodeError:
                    existing_logs = []
        else:
            existing_logs = []

        # Append new logs to the existing logs
        existing_logs.extend(logs)

        # Write back to the file
        with open(LOG_FILE, 'w') as f:
            json.dump(existing_logs, f, indent=4)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
