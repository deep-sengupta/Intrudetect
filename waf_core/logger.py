import json, os
from datetime import datetime, timezone

def log_request(req_data, log_file):
    entry = {
        "timestamp": req_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
        "method": req_data["method"],
        "path": req_data["path"],
        "params": req_data["params"],
        "headers": req_data["headers"],
        "ip": req_data["ip"],
        "body": req_data.get("body", ""),
        "status": req_data.get("status", 200)
    }

    data = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                data = json.load(f)
        except:
            pass

    data.append(entry)
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)
