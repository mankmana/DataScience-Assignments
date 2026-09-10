import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler


def clean_transactions(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    required = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing[:5])}")
    for col in required + (["Class"] if "Class" in df else []):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=required).drop_duplicates().reset_index(drop=True)


def fit_detector(df, contamination=None):
    clean = clean_transactions(df)
    features = [f"V{i}" for i in range(1, 29)] + ["Time", "Amount"]
    X = clean[features].to_numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    prior = float(clean["Class"].mean()) if "Class" in clean else 0.01
    contamination = float(np.clip(contamination or prior, 0.005, 0.20))
    model = IsolationForest(n_estimators=180, contamination=contamination, random_state=42, n_jobs=-1)
    model.fit(X_scaled)
    clean["anomaly_score"] = -model.score_samples(X_scaled)
    clean["anomaly"] = (model.predict(X_scaled) == -1).astype(int)
    clean["risk_band"] = pd.cut(clean["anomaly_score"], bins=[-np.inf, clean.anomaly_score.quantile(.75), clean.anomaly_score.quantile(.95), np.inf], labels=["Low", "Review", "High"])
    return clean, model, scaler, contamination


def metrics(df):
    if "Class" not in df:
        return {}
    y, p, score = df["Class"], df["anomaly"], df["anomaly_score"]
    return {"precision": precision_score(y, p, zero_division=0), "recall": recall_score(y, p, zero_division=0), "f1": f1_score(y, p, zero_division=0), "roc_auc": roc_auc_score(y, score), "pr_auc": average_precision_score(y, score), "false_positives": int(((p == 1) & (y == 0)).sum()), "true_frauds": int(y.sum()), "detected": int(p.sum()), "confusion_matrix": confusion_matrix(y, p).tolist()}

