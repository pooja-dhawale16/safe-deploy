
from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "safedeploy_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_DURATION = Histogram(
    "safedeploy_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


@app.before_request
def start_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    # Do not count metrics scraping as application traffic.
    if request.path != "/metrics":
        duration = time.perf_counter() - getattr(
            request, "start_time", time.perf_counter()
        )

        REQUEST_COUNT.labels(
            request.method, request.path, str(response.status_code)
        ).inc()

        REQUEST_DURATION.labels(
            request.method, request.path
        ).observe(duration)

    return response


@app.route("/")
def home():
    return jsonify({
        "project": "SafeDeploy",
        "status": "running",
        "message": "Secure deployment pipeline demo"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

