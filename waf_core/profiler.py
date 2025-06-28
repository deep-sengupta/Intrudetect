import json, os
from collections import defaultdict

class TrafficProfiler:
    def __init__(self, baseline_file):
        self.baseline_file = baseline_file
        self.profile = {
            "methods": defaultdict(int),
            "paths": defaultdict(int),
            "param_keys": defaultdict(int),
            "content_lengths": [],
            "headers": defaultdict(int),
            "ip_requests": defaultdict(int)
        }
        self.load_profile()

    def process_request(self, req_data):
        self.profile["methods"][req_data["method"]] += 1
        self.profile["paths"][req_data["path"]] += 1
        for key in req_data.get("params", {}):
            self.profile["param_keys"][key] += 1
        self.profile["content_lengths"].append(len(req_data.get("body", "")))
        for key in req_data.get("headers", {}):
            self.profile["headers"][key] += 1
        self.profile["ip_requests"][req_data["ip"]] += 1

    def save_profile(self):
        with open(self.baseline_file, "w") as f:
            json.dump(self.profile, f, indent=2)

    def load_profile(self):
        if os.path.exists(self.baseline_file):
            try:
                with open(self.baseline_file, "r") as f:
                    self.profile = json.load(f)
            except:
                pass
