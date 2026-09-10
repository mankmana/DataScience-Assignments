from pathlib import Path
import numpy as np
import pandas as pd


def demo_transactions(n=6000, seed=42):
    rng = np.random.default_rng(seed)
    fraud = rng.random(n) < 0.018
    features = {f"V{i}": rng.normal(0, 1, n) for i in range(1, 29)}
    amount = np.exp(rng.normal(3.3, 1.05, n)).clip(0.5, 2500)
    amount[fraud] *= rng.uniform(1.5, 4.5, fraud.sum())
    for i in [3, 7, 14, 17, 21]:
        features[f"V{i}"][fraud] += rng.normal(3.2, 0.8, fraud.sum())
    return pd.DataFrame({"Time": np.arange(n) * 31, **features, "Amount": amount.round(2), "Class": fraud.astype(int)})


def load_transactions(path="data/creditcard.csv"):
    file = Path(path)
    if file.exists():
        return pd.read_csv(file), "Kaggle creditcard.csv"
    return demo_transactions(), "Deterministic demo fallback (creditcard.csv schema)"

