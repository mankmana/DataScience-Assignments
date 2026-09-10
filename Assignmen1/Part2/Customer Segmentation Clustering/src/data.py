from pathlib import Path
import numpy as np
import pandas as pd


def demo_customers(n=300, seed=42):
    """Create a deterministic Mall_Customers-shaped fallback dataset."""
    rng = np.random.default_rng(seed)
    groups = rng.choice([0, 1, 2, 3, 4], n, p=[.20, .20, .20, .20, .20])
    age = np.clip(rng.normal([24, 46, 29, 55, 35][0] if False else 38, 14, n), 18, 70).round().astype(int)
    income = np.clip(rng.normal(60, 22, n), 15, 140).round().astype(int)
    spend = np.clip(rng.normal(50, 24, n), 1, 99).round().astype(int)
    age += np.select([groups == 0, groups == 1, groups == 2, groups == 3, groups == 4], [-8, 10, -7, 14, 0], default=0)
    income += np.select([groups == 0, groups == 1, groups == 2, groups == 3, groups == 4], [15, 12, -10, 8, -3], default=0)
    spend += np.select([groups == 0, groups == 1, groups == 2, groups == 3, groups == 4], [30, -25, 25, -30, 0], default=0)
    return pd.DataFrame({"CustomerID": np.arange(1, n + 1), "Gender": rng.choice(["Male", "Female"], n), "Age": np.clip(age, 18, 70), "Annual Income (k$)": np.clip(income, 15, 140), "Spending Score (1-100)": np.clip(spend, 1, 99)})


def load_customers(path="data/Mall_Customers.csv"):
    file = Path(path)
    if file.exists():
        return pd.read_csv(file), "Kaggle Mall Customers CSV"
    return demo_customers(), "Deterministic demo fallback (Mall Customers schema)"

