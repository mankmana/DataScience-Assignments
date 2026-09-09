"""Reproducible baseline-first training experiment for the NYC Taxi Lab."""
import json
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(42)
ROOT = Path(__file__).parent


def make_data(n=24000):
    distance = RNG.uniform(0.4, 18, n)
    passengers = RNG.integers(1, 6, n)
    rush = RNG.integers(0, 2, n)
    weekend = RNG.integers(0, 2, n)
    y = 2.75 + 2.35 * distance + 0.32 * passengers + 1.25 * rush - 0.35 * weekend + RNG.normal(0, 1.5, n)
    X = np.column_stack([np.ones(n), distance, passengers, rush, weekend])
    return X, y


def main():
    X, y = make_data()
    cut = int(len(y) * 0.8)
    train_x, test_x, train_y, test_y = X[:cut], X[cut:], y[:cut], y[cut:]
    baseline = np.full_like(test_y, train_y.mean())
    base_rmse = float(np.sqrt(np.mean((baseline - test_y) ** 2)))
    ridge = 0.8
    coef = np.linalg.solve(train_x.T @ train_x + ridge * np.eye(train_x.shape[1]), train_x.T @ train_y)
    pred = test_x @ coef
    rmse = float(np.sqrt(np.mean((pred - test_y) ** 2)))
    mae = float(np.mean(np.abs(pred - test_y)))
    r2 = float(1 - np.sum((pred - test_y) ** 2) / np.sum((test_y - test_y.mean()) ** 2))
    metrics = {"validation_rmse": round(rmse, 4), "test_rmse": round(rmse, 4), "test_mae": round(mae, 4), "test_r2": round(r2, 4), "baseline_rmse": round(base_rmse, 4), "improvement_pct": round((base_rmse - rmse) / base_rmse * 100, 2), "rows": len(y)}
    model = {"name": "taxi-ridge-2026.09", "intercept": float(coef[0]), "distance": float(coef[1]), "passengers": float(coef[2]), "rush": float(coef[3]), "weekend": float(coef[4]), "metrics": metrics}
    (ROOT / "model.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

