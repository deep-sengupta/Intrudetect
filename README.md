# Overview

The system operates in two configurable modes:

- **Training Mode**: Builds a baseline of normal request patterns.
- **Detection Mode**: Flags requests that deviate from the baseline as anomalies.

It logs full request metadata, including IP address, headers, query parameters, and body size, and supports an API interface for retrieving logs and anomalies.

---

## Project Structure

```
├── app.py                     # Main Flask application
├── config.json                # Configuration file
├── waf_core/
│   ├── detector.py            # Anomaly detection logic
│   ├── profiler.py            # Traffic profiling
│   └── logger.py              # Request logging
├── templates/
│   └── dashboard.html         # Optional dashboard template
├── logs/
│   ├── requests.json          # Logged HTTP requests
│   ├── anomalies.json         # Detected anomalies
│   └── baseline.json          # Trained traffic baseline
````

---

## Configuration

Edit `config.json` to control mode and log file paths:

```json
{
  "MODE": "detect",
  "LOG_FILE": "logs/requests.json",
  "ANOMALY_FILE": "logs/anomalies.json",
  "BASELINE_FILE": "logs/baseline.json"
}
````

* `train` – learn normal traffic
* `detect` – activate detection engine

---

## API Endpoints

| Endpoint         | Description                        |
| ---------------- | ---------------------------------- |
| `/`              | Status and mode display            |
| `/dashboard`     | (Optional) HTML dashboard view     |
| `/api/logs`      | Return captured traffic log (JSON) |
| `/api/anomalies` | Return anomaly records (JSON)      |
| `/test`          | Dummy endpoint for request testing |

---

## Example Log Entry

```json
{
  "timestamp": "2025-06-28T20:33:11+00:00",
  "method": "GET",
  "path": "/test",
  "params": {},
  "headers": {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
  },
  "ip": "127.0.0.1",
  "body": "",
  "status": 200
}
```