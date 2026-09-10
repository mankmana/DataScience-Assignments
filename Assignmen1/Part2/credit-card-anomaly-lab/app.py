import sys
from pathlib import Path
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from src.data import load_transactions
from src.anomaly import clean_transactions, fit_detector, metrics

st.set_page_config(page_title="Credit Card Anomaly Lab", page_icon="◉", layout="wide")
st.markdown("""<style>.block-container{padding-top:2rem;max-width:1250px}.hero{padding-bottom:1rem}.eyebrow{color:#cf4d4d;font-weight:800;letter-spacing:.14em;font-size:.72rem}.hero h1{font:3.5rem Georgia,serif;margin:.35rem 0}.alert{background:#fff1f1;border:1px solid #ffd1d1;padding:12px 15px;border-radius:10px}</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">CRISP-DM / FRAUD OPERATIONS</div><h1>Find the transactions that do not belong.</h1><p>Use unsupervised Isolation Forest detection to prioritize suspicious payments for human review.</p></div>', unsafe_allow_html=True)
raw, source = load_transactions()
with st.sidebar:
    st.header("Detector controls")
    st.caption(source)
    contamination = st.slider("Investigation rate", 0.005, 0.10, 0.018, 0.001, help="Expected share routed for review. The model never uses Class during fitting.")
try:
    clean = clean_transactions(raw)
    labeled, model, scaler, used = fit_detector(clean, contamination)
except ValueError as exc:
    st.error(str(exc)); st.stop()
m = metrics(labeled)
cols = st.columns(5)
cols[0].metric("Transactions", f"{len(labeled):,}")
cols[1].metric("Flagged", f"{m.get('detected', int(labeled.anomaly.sum())):,}")
cols[2].metric("Precision", f"{m.get('precision', 0):.1%}")
cols[3].metric("Recall", f"{m.get('recall', 0):.1%}")
cols[4].metric("PR-AUC", f"{m.get('pr_auc', 0):.3f}")
st.markdown(f'<div class="alert">The dashboard routes approximately <b>{used:.1%}</b> of transactions for review. Labels are used only to evaluate the unsupervised detector after scoring.</div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Risk overview", "Suspicious queue", "Evaluation", "CRISP-DM"])
with tab1:
    a, b = st.columns(2)
    with a:
        fig = px.histogram(labeled, x="Amount", color=labeled["anomaly"].map({0:"Normal",1:"Anomaly"}), nbins=50, log_x=True, title="Transaction amounts by detector result", template="simple_white")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.scatter(labeled.sample(min(2500, len(labeled)), random_state=42), x="V14", y="V17", color=labeled.sample(min(2500, len(labeled)), random_state=42)["anomaly"].map({0:"Normal",1:"Anomaly"}), size="Amount", hover_data=["Time", "Amount", "anomaly_score"], title="Anonymized feature space", template="simple_white")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Known-label comparison")
    if "Class" in labeled: st.dataframe(labeled.groupby(["Class", "anomaly"]).size().rename("transactions").reset_index(), hide_index=True, use_container_width=True)
with tab2:
    queue = labeled.sort_values("anomaly_score", ascending=False).head(100)
    st.write("Highest-scoring transactions recommended for analyst review.")
    st.dataframe(queue[["Time", "Amount", "anomaly_score", "risk_band"] + (["Class"] if "Class" in queue else [])], hide_index=True, use_container_width=True)
    st.download_button("Download review queue", queue.to_csv(index=False).encode(), "suspicious_transactions.csv", "text/csv")
with tab3:
    if m:
        st.dataframe({"Metric":["Precision","Recall","F1","ROC-AUC","PR-AUC","False positives","Known frauds"],"Value":[f"{m['precision']:.3f}",f"{m['recall']:.3f}",f"{m['f1']:.3f}",f"{m['roc_auc']:.3f}",f"{m['pr_auc']:.3f}",m['false_positives'],m['true_frauds']]}, hide_index=True, use_container_width=True)
        st.write("Confusion matrix [actual rows: normal, fraud; predicted columns: normal, anomaly]")
        st.write(m["confusion_matrix"])
    st.info("Accuracy is intentionally omitted: with extreme class imbalance it can look excellent while missing fraud. PR-AUC and the review queue burden are more decision-relevant.")
with tab4:
    st.markdown("""### Business understanding\nPrioritize suspicious card transactions for investigation while controlling analyst workload.\n\n### Data understanding\nThe Kaggle dataset contains anonymized PCA features V1–V28, Time, Amount, and the known fraud label Class.\n\n### Data preparation\nValidate schema, coerce numeric fields, remove incomplete/duplicate records, and standardize Time and Amount alongside the anonymized features.\n\n### Modeling\nFit Isolation Forest without Class. The investigation-rate control becomes the contamination prior.\n\n### Evaluation\nCompare flags with Class after scoring using precision, recall, F1, ROC-AUC, PR-AUC, false positives, and a confusion matrix.\n\n### Action\nUse the score as a triage signal, not an automatic decline decision. Combine it with velocity, merchant context, device signals, and analyst feedback. Monitor drift and recalibrate the investigation rate as fraud tactics change.""")

