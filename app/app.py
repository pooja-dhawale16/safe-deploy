
from flask import Flask, jsonify

app = Flask(__name__)


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

