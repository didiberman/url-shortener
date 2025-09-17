import os
import secrets
import redis
# NEW: Import render_template
from flask import Flask, request, redirect, jsonify, render_template
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

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

REDIRECTS_COUNTER = Counter(
    'url_shortener_redirects_total',
    'Total number of redirects handled'
)
CREATES_COUNTER = Counter(
    'url_shortener_creates_total',
    'Total number of short URLs created'
)

# --- GUI Endpoint ---

# NEW: Add a route for the root URL ("/") to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# --- API Endpoints ---

@app.route('/create', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided"}), 400

    long_url = data['url']
    short_code = secrets.token_urlsafe(6)
    db.set(short_code, long_url)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
