import os
import secrets
import redis
from flask import Flask, request, redirect, jsonify
from prometheus_client import Counter, generate_latest

# 1. Initialize the Flask App
app = Flask(__name__)

# 2. Connect to Redis
# It's configured to connect to a Redis instance.
# The host is read from an environment variable 'REDIS_HOST', defaulting to 'localhost'.
try:
    db = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=6379,
        decode_responses=True # Decode responses from bytes to strings
    )
    db.ping() # Check the connection
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    # Exit or handle the error gracefully if Redis is essential
    exit(1)


# 3. Create a Prometheus Counter Metric
# This will count every time a redirect is successfully served.
REDIRECTS_COUNTER = Counter(
    'url_shortener_redirects_total',
    'Total number of redirects handled'
)

# --- API Endpoints ---

@app.route('/create', methods=['POST'])
def create_short_url():
    """
    Creates a short URL mapping.
    Accepts a POST request with a JSON body: {"url": "https://your-long-url.com"}
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided"}), 400

    long_url = data['url']
    # Generate a short, 6-character code
    short_code = secrets.token_urlsafe(6)

    # Store the mapping in Redis
    db.set(short_code, long_url)

    # Return the full short URL in the response
    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url}), 201

@app.route('/<string:short_code>')
def redirect_to_long_url(short_code):
    """
    Looks up the short code and redirects the user.
    """
    long_url = db.get(short_code)

    if long_url:
        # Increment the counter for a successful redirect
        REDIRECTS_COUNTER.inc()
        return redirect(long_url, code=302)
    else:
        return jsonify({"error": "Short URL not found"}), 404

@app.route('/metrics')
def metrics():
    """
    Exposes Prometheus metrics.
    """
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}


# --- Main execution block ---

if __name__ == '__main__':
    # Run the app, making it accessible on the network (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)
