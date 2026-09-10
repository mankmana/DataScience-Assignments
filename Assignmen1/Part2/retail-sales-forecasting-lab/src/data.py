from pathlib import Path
import numpy as np
import pandas as pd


def demo_sales(seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2017-01-06", periods=156, freq="W-FRI")
    rows = []
    for store in [1, 2, 3]:
        base = {1: 210000, 2: 185000, 3: 142000}[store]
        for i, date in enumerate(dates):
            seasonal = 1 + .16 * np.sin(2 * np.pi * i / 52) + .09 * np.cos(4 * np.pi * i / 52)
            holiday = int(date.month in [11, 12] and date.day > 15)
            sales = base * (1 + i * .0012) * seasonal * (1 + .11 * holiday) + rng.normal(0, base * .035)
            rows.append({"Store": store, "Date": date, "Weekly_Sales": round(max(50000, sales), 2), "Holiday_Flag": holiday, "Temperature": 55 + 25 * np.sin(i / 52 * 2 * np.pi), "Fuel_Price": 2.8 + i * .002, "CPI": 210 + i * .05, "Unemployment": 7.5 - i * .004})
    return pd.DataFrame(rows)


def load_sales(path="data/train.csv"):
    file = Path(path)
    if file.exists():
        return pd.read_csv(file), "Kaggle Walmart train.csv"
    return demo_sales(), "Deterministic demo fallback (Walmart schema)"


def clean_sales(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    required = ["Store", "Date", "Weekly_Sales"]
    missing = [c for c in required if c not in df.columns]
    if missing: raise ValueError("Missing columns: " + ", ".join(missing))
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Weekly_Sales"] = pd.to_numeric(df["Weekly_Sales"], errors="coerce")
    df["Store"] = pd.to_numeric(df["Store"], errors="coerce").astype("Int64")
    if "Holiday_Flag" not in df: df["Holiday_Flag"] = 0
    df["Holiday_Flag"] = pd.to_numeric(df["Holiday_Flag"], errors="coerce").fillna(0)
    return df.dropna(subset=required).drop_duplicates(subset=["Store", "Date"]).sort_values(["Store", "Date"]).reset_index(drop=True)

