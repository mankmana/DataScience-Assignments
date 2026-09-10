from pathlib import Path
import numpy as np
import pandas as pd


def demo_baskets(n=500, seed=42):
    rng = np.random.default_rng(seed)
    items = ["whole milk", "vegetables", "rolls/buns", "yogurt", "sausage", "tropical fruit", "soda", "coffee", "bottled water", "pastry", "root vegetables", "whipped/sour cream"]
    baskets = []
    for _ in range(n):
        basket = set(rng.choice(items[:8], size=rng.integers(2, 6), replace=False).tolist())
        if "whole milk" in basket and rng.random() < .65: basket.add("rolls/buns")
        if "yogurt" in basket and rng.random() < .55: basket.add("tropical fruit")
        if "sausage" in basket and rng.random() < .45: basket.add("root vegetables")
        baskets.append(sorted(basket))
    return baskets, "Deterministic demo baskets"


def load_baskets(path="data/groceries.csv"):
    file = Path(path)
    if not file.exists(): return demo_baskets()
    df = pd.read_csv(file, sep=None, engine="python")
    df.columns = [str(c).strip() for c in df.columns]
    lower = {c.lower(): c for c in df.columns}
    item_col = next((lower[k] for k in ["item", "product", "item description"] if k in lower), None)
    basket_col = next((lower[k] for k in ["basket", "basketid", "transaction", "transactionid", "member number"] if k in lower), None)
    if item_col and basket_col:
        grouped = df.dropna(subset=[item_col]).groupby(basket_col)[item_col].apply(lambda s: sorted(set(str(x).strip().lower() for x in s if str(x).strip()))).tolist()
        return [x for x in grouped if x], "Kaggle CSV (transaction rows)"
    baskets = []
    for _, row in df.iterrows():
        values = [str(v).strip().lower() for v in row.tolist() if pd.notna(v) and str(v).strip()]
        if values: baskets.append(sorted(set(values)))
    return baskets, "Kaggle CSV (basket rows)"

