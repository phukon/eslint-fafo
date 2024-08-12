from flask import Flask, request, jsonify
import gzip
import json

app = Flask(__name__)

LOG_FILE = 'logs.txt'

@app.route('/logs', methods=['POST'])
def receive_logs():
    try:
        # Read and decompress the logs
        compressed_data = request.data
        decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
        logs = json.loads(decompressed_data)

        # Write logs to file
        with open(LOG_FILE, 'a') as f:
            for log in logs:
                f.write(json.dumps(log) + '\n')

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)