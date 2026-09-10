# Credit Card Anomaly Lab

An end-to-end anomaly detection project based on Kaggle's **Credit Card Fraud Detection** dataset. It follows CRISP-DM and uses an unsupervised Isolation Forest to flag suspicious transactions, then compares the flags with the known `Class` fraud label for evaluation.

The app runs immediately with a deterministic, schema-compatible fallback. To use the original data, download `creditcard.csv` from [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it at `data/creditcard.csv`.


#Prompt used
ok, now we will work on another Data science technique called anomaly detection. Use Kaggle data set  called Credit card fraud detection dataset and follow below prompt



Build an end-to-end anomaly detection data science project using the Kaggle Credit Card Fraud Detection dataset.

Follow the CRISP-DM framework.

Use unsupervised anomaly detection, preferably Isolation Forest, to identify suspicious or anomalous credit card transactions.

The project should include:

- data loading and cleaning
- exploratory data analysis
- handling the highly imbalanced dataset
- preprocessing/scaling
- Isolation Forest anomaly detection
- comparison of detected anomalies with the known fraud labels
- evaluation using suitable metrics such as precision, recall, F1-score, ROC-AUC or PR-AUC
- visualizations of normal vs anomalous transactions
- an interactive dashboard showing anomaly statistics and suspicious transactions
- business interpretation of the results
- README with methodology, dataset, model, results, architecture, and run instructions

Keep the implementation practical, visually clear, also run it on a cloud for me to walk through.


# YT VIdeo link
https://youtu.be/FeuIl1hakcM


## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Methodology

- Load and validate `Time`, `V1`–`V28`, `Amount`, and optional `Class`.
- Inspect missing values, duplicate rows, fraud rate, and amount distribution.
- Standardize `Amount` and `Time`; PCA features are already anonymized numeric features.
- Fit Isolation Forest without using the fraud label during training.
- Set the contamination prior from the observed fraud rate for a practical benchmark.
- Compare anomaly flags with `Class` using precision, recall, F1, ROC-AUC, and PR-AUC.

## Important evaluation note

This is unsupervised detection: labels are held out from model fitting and used only for post-hoc evaluation. Because fraud is highly imbalanced, PR-AUC, recall at an investigation capacity, and the false-positive burden are often more useful than accuracy. The fallback data is synthetic and does not represent real bank performance.

## Architecture

`app.py` is the Streamlit dashboard. `src/data.py` loads Kaggle data or creates a deterministic fallback. `src/anomaly.py` owns cleaning, scaling, Isolation Forest, metrics, profiling, and suspicious-transaction selection. `cloud/index.html` is a browser-native walkthrough deployed separately for cloud access.

