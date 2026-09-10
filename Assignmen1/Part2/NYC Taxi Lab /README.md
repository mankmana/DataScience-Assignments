# NYC Taxi Lab

An end-to-end NYC taxi fare estimation lab built around the Kaggle NYC Taxi Fare Prediction schema. It includes a responsive estimator, interactive Leaflet map, data-science dashboard, reproducible training script, model artifact, CRISP-DM research report, and a small production-ready Flask API.

> The included dataset is synthetic and schema-compatible. Metrics are pipeline-validation metrics, not Kaggle leaderboard results.
>
## YT video link
https://youtu.be/TXgWhE6zZDc

Screenshots of the website are uploaded under screenshots folder

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py
python app.py
```

Open http://127.0.0.1:5000.

## API

`POST /api/predict`

```json
{"pickup_latitude":40.758,"pickup_longitude":-73.985,"dropoff_latitude":40.730,"dropoff_longitude":-73.995,"passenger_count":2,"pickup_datetime":"2026-09-08T18:30"}
```

## Project map

- `app.py` — Flask API and static-file server
- `train.py` — reproducible synthetic data generation, baseline comparison, and Ridge-style model fitting
- `model.json` — exported coefficients and validation metadata
- `static/` — frontend estimator and admin dashboard
- `reports/CRISP_DM_REPORT.md` — research report and autoresearch hill-climbing log

