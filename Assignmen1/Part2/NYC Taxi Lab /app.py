from datetime import datetime
import json
import math
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).parent
app = Flask(__name__, static_folder="static", static_url_path="/static")

with open(ROOT / "model.json", encoding="utf-8") as f:
    MODEL = json.load(f)


def haversine_miles(lat1, lon1, lat2, lon2):
    radius = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return radius * 2 * math.asin(math.sqrt(a))


def predict(payload):
    required = ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]
    if any(key not in payload for key in required):
        raise ValueError("pickup and dropoff coordinates are required")
    lat1, lon1 = float(payload["pickup_latitude"]), float(payload["pickup_longitude"])
    lat2, lon2 = float(payload["dropoff_latitude"]), float(payload["dropoff_longitude"])
    distance = max(0.2, haversine_miles(lat1, lon1, lat2, lon2))
    passengers = max(1, min(6, int(payload.get("passenger_count", 1))))
    stamp = payload.get("pickup_datetime") or datetime.now().isoformat(timespec="minutes")
    hour = datetime.fromisoformat(stamp.replace("Z", "")).hour
    rush = 1.0 if hour in {7, 8, 9, 16, 17, 18, 19} else 0.0
    weekend = 1.0 if datetime.fromisoformat(stamp.replace("Z", "")).weekday() >= 5 else 0.0
    amount = MODEL["intercept"] + MODEL["distance"] * distance + MODEL["passengers"] * passengers + MODEL["rush"] * rush + MODEL["weekend"] * weekend
    amount = max(3.0, round(amount, 2))
    duration = max(4, round(distance * (3.6 + 1.4 * rush) + 2.5))
    uncertainty = round(max(1.8, amount * 0.13), 2)
    return {"fare": amount, "low": round(amount - uncertainty, 2), "high": round(amount + uncertainty, 2), "distance_miles": round(distance, 2), "duration_minutes": duration, "rush_hour": bool(rush), "model": MODEL["name"]}


@app.get("/")
def index():
    return send_from_directory(ROOT / "static", "index.html")


@app.post("/api/predict")
def api_predict():
    try:
        return jsonify(predict(request.get_json(force=True)))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.get("/api/metrics")
def metrics():
    return jsonify(MODEL["metrics"])


@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "model": MODEL["name"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

