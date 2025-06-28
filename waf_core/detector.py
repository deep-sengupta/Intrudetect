import json, os

class AnomalyDetector:
    def __init__(self, baseline_file):
        self.baseline_file = baseline_file
        self.baseline = {}
        self.load_baseline()

    def load_baseline(self):
        if os.path.exists(self.baseline_file):
            try:
                with open(self.baseline_file, "r") as f:
                    self.baseline = json.load(f)
            except:
                pass

    def detect(self, req_data):
        anomalies = []

        if req_data["method"] not in self.baseline.get("methods", {}):
            anomalies.append(f"Unexpected HTTP method: {req_data['method']}")
        if req_data["path"] not in self.baseline.get("paths", {}):
            anomalies.append(f"Unseen request path: {req_data['path']}")
        for key in req_data.get("params", {}):
            if key not in self.baseline.get("param_keys", {}):
                anomalies.append(f"Unexpected parameter key: {key}")
        for key in req_data.get("headers", {}):
            if key not in self.baseline.get("headers", {}):
                anomalies.append(f"Unexpected header: {key}")

        try:
            body_len = len(req_data.get("body", ""))
            if self.baseline.get("content_lengths"):
                if body_len > max(self.baseline["content_lengths"]) * 1.5:
                    anomalies.append(f"Request body too large: {body_len} bytes")
        except:
            anomalies.append("Body length check failed")

        ip = req_data["ip"]
        if self.baseline.get("ip_requests", {}).get(ip, 0) > 1000:
            anomalies.append(f"High traffic from IP: {ip}")

        return anomalies

def save_anomaly_log(req_data, issues, anomaly_file):
    entry = {
        "timestamp": req_data.get("timestamp"),
        "method": req_data["method"],
        "path": req_data["path"],
        "params": req_data["params"],
        "headers": req_data["headers"],
        "ip": req_data["ip"],
        "body": req_data.get("body", ""),
        "issues": issues
    }

    data = []
    if os.path.exists(anomaly_file):
        try:
            with open(anomaly_file, "r") as f:
                data = json.load(f)
        except:
            pass

    data.append(entry)
    with open(anomaly_file, "w") as f:
        json.dump(data, f, indent=2)
