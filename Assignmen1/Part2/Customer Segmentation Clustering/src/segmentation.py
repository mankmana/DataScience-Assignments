import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import silhouette_score


def clean_customers(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    aliases = {"Annual Income (k$) ": "Annual Income (k$)", "Spending Score (1-100) ": "Spending Score (1-100)"}
    df = df.rename(columns=aliases)
    required = ["Gender", "Age", "Annual Income (k$)", "Spending Score (1-100)"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    for col in ["Age", "Annual Income (k$)", "Spending Score (1-100)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Gender"] = df["Gender"].astype(str).str.title().replace({"Nan": "Unknown"})
    df = df.dropna(subset=required).drop_duplicates().reset_index(drop=True)
    return df


def build_features(df):
    numeric = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    categorical = ["Gender"]
    preprocessor = ColumnTransformer([("num", StandardScaler(), numeric), ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical)])
    matrix = preprocessor.fit_transform(df)
    return matrix, preprocessor, numeric + ["Gender"]


def evaluate_k(matrix, k_values=range(2, 9)):
    rows = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(matrix)
        rows.append({"k": k, "inertia": model.inertia_, "silhouette": silhouette_score(matrix, labels)})
    scores = pd.DataFrame(rows)
    best_k = int(scores.loc[scores["silhouette"].idxmax(), "k"])
    return scores, best_k


def fit_segmentation(df, requested_k=None):
    clean = clean_customers(df)
    matrix, preprocessor, _ = build_features(clean)
    scores, best_k = evaluate_k(matrix)
    k = requested_k or best_k
    model = KMeans(n_clusters=int(k), random_state=42, n_init=20)
    clean["cluster"] = model.fit_predict(matrix)
    clean["segment"] = name_segments(clean)
    profiles = profile_segments(clean)
    return clean, scores, int(k), profiles, model, preprocessor


def name_segments(df):
    med = df.groupby("cluster")[["Annual Income (k$)", "Spending Score (1-100)"]].median()
    income_mid, spend_mid = df["Annual Income (k$)"].median(), df["Spending Score (1-100)"].median()
    names = {}
    for cluster, row in med.iterrows():
        high_i, high_s = row.iloc[0] >= income_mid, row.iloc[1] >= spend_mid
        names[cluster] = {(True, True): "Premium Champions", (True, False): "Affluent Cautious", (False, True): "Emerging Enthusiasts", (False, False): "Value Conservers"}[(high_i, high_s)]
    return df["cluster"].map(names)


def profile_segments(df):
    profile = df.groupby(["cluster", "segment"]).agg(customers=("CustomerID", "count"), avg_age=("Age", "mean"), avg_income=("Annual Income (k$)", "mean"), avg_spend=("Spending Score (1-100)", "mean")).reset_index()
    profile["share_pct"] = profile["customers"] / len(df) * 100
    profile["action"] = profile["segment"].map({"Premium Champions": "Retain with loyalty tiers, early access, and high-touch service.", "Affluent Cautious": "Use education, bundles, and trust-building offers to unlock spend.", "Emerging Enthusiasts": "Use personalized discovery, social proof, and limited-time offers.", "Value Conservers": "Lead with value packs, essentials, and low-friction reactivation."})
    return profile
