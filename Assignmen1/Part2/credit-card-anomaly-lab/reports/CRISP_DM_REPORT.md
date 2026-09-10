# Credit Card Anomaly Lab — CRISP-DM Report

## Business understanding

Fraud teams need to prioritize a small review queue from a very large transaction stream. The objective is to identify unusual behavior with an unsupervised model, keep the review rate explicit, and compare results with confirmed fraud labels after scoring.

## Data understanding

The Kaggle Credit Card Fraud Detection dataset contains 284,807 transactions, 492 known frauds, anonymized PCA features V1–V28, elapsed Time, Amount, and Class. The positive class is extremely rare. The repository supports the original `creditcard.csv` and a deterministic schema-compatible fallback for demonstrations.

## Data preparation

The pipeline validates the required schema, coerces numeric fields, removes incomplete and duplicate rows, and standardizes all model inputs. Class is retained only for post-hoc evaluation; it is not passed to Isolation Forest fitting.

## Modeling

Isolation Forest isolates observations using random partitioning. Transactions that are isolated with shorter paths receive higher anomaly scores. The contamination parameter is exposed as an investigation-rate control and defaults to the observed fraud prior for the loaded data or a practical demo prior.

## Evaluation

The dashboard reports precision, recall, F1, ROC-AUC, PR-AUC, false positives, true frauds detected, and a confusion matrix. Accuracy is not emphasized because a model can achieve near-perfect accuracy by predicting every transaction as normal. PR-AUC and the analyst queue burden should guide operating-point selection.

## Deployment and operations

Streamlit provides the local interactive dashboard. The queue can be downloaded as CSV. In production, store scores and analyst outcomes, monitor score drift and fraud prevalence, track precision at a fixed review capacity, and retrain or recalibrate when behavior changes.

## Business interpretation

An anomaly flag is a triage signal, not proof of fraud. High-score transactions should receive step-up authentication or human review depending on policy. Combine model output with transaction velocity, merchant category, device fingerprint, geography, and account history before declining a payment. False positives carry customer-friction cost; false negatives carry loss and trust cost.

## Limitations

Anonymized PCA features limit direct explanation. The dataset is historical and may not represent current fraud tactics. Thresholds must be tuned to operational capacity and calibrated on time-based validation, with leakage controls and subgroup fairness checks before live use.

