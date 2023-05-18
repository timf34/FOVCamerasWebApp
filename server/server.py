from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This allows cross-origin requests

status = {
    'deviceId': 'jetson_nano_1',
    'wifiStatus': True,
    'batteryLevel': 90,
    'temperature': 40
}

@app.route('/api/status')
def get_status():
    return jsonify(status)

if __name__ == '__main__':
    app.run(port=5000)
