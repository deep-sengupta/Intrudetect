from flask import Flask, request, jsonify, render_template
from waf_core.profiler import TrafficProfiler
from waf_core.detector import AnomalyDetector, save_anomaly_log
from waf_core.logger import log_request
from datetime import datetime, timezone
import json, os

with open("config.json") as f:
    CONFIG = json.load(f)

app = Flask(__name__)
profiler = TrafficProfiler(CONFIG["BASELINE_FILE"])
detector = AnomalyDetector(CONFIG["BASELINE_FILE"])
MODE = CONFIG["MODE"]

def is_ignored_path(path):
    return (
        path.startswith("/static")
        or path.startswith("/api")
        or path in ("/dashboard", "/favicon.ico", "/robots.txt")
    )

def current_request_data(include_status=False, status=None):
    data = {
        "method": request.method,
        "path": request.path,
        "params": request.args.to_dict(),
        "headers": dict(request.headers),
        "ip": request.remote_addr,
        "body": request.get_data(as_text=True),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    if include_status:
        data["status"] = status or 200
    return data

@app.before_request
def intercept():
    if is_ignored_path(request.path):
        return
    data = current_request_data()
    if MODE == "train":
        profiler.process_request(data)
        profiler.save_profile()
    elif MODE == "detect":
        anomalies = detector.detect(data)
        if anomalies:
            save_anomaly_log(data, anomalies, CONFIG["ANOMALY_FILE"])
            return jsonify({"status": "anomaly_detected", "issues": anomalies}), 403

@app.after_request
def post_intercept(response):
    if is_ignored_path(request.path):
        return response
    data = current_request_data(include_status=True, status=response.status_code)
    log_request(data, CONFIG["LOG_FILE"])
    if response.status_code in (401, 302):
        save_anomaly_log(data, [f"Suspicious response status: {response.status_code}"], CONFIG["ANOMALY_FILE"])
    return response

@app.route('/')
def index():
    return f"WAF Running in {MODE} mode"

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

def load_json_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try: return json.load(f)
            except: pass
    return []

@app.route('/api/logs')
def get_logs():
    return jsonify(load_json_file(CONFIG["LOG_FILE"]))

@app.route('/api/anomalies')
def get_anomalies():
    return jsonify(load_json_file(CONFIG["ANOMALY_FILE"]))

@app.route('/test')
def test_page():
    return "Test page hit!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
