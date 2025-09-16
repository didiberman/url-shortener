import os
import secrets
import redis
from flask import Flask, request, redirect, jsonify
from prometheus_client import Counter, generate_latest

# 1. Initialize the Flask App
app = Flask(__name__)

# 2. Connect to Redis
try:
    db = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=6379,
        decode_responses=True
    )
    db.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    exit(1)


# 3. Create Prometheus Counter Metrics
REDIRECTS_COUNTER = Counter(
    'url_shortener_redirects_total',
    'Total number of redirects handled'
)

# NEW: Add a counter for URL creations
CREATES_COUNTER = Counter(
    'url_shortener_creates_total',
    'Total number of short URLs created'
)


# --- API Endpoints ---

@app.route('/create', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided"}), 400

    long_url = data['url']
    short_code = secrets.token_urlsafe(6)

    # Store the mapping in Redis
    db.set(short_code, long_url)

    # NEW: Increment the counter for a successful creation
    CREATES_COUNTER.inc()

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url}), 201

@app.route('/<string:short_code>')
def redirect_to_long_url(short_code):
    long_url = db.get(short_code)

    if long_url:
        REDIRECTS_COUNTER.inc()
        return redirect(long_url, code=302)
    else:
        return jsonify({"error": "Short URL not found"}), 404

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}


# --- Main execution block ---

if __name__ == '__main__':
    # Using flask run is better for development
    # To run this, use: flask --app app run --host=0.0.0.0 --port=3333
    app.run(host='0.0.0.0', port=3333)
