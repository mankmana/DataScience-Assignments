import io
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from src.data import load_customers
from src.segmentation import clean_customers, fit_segmentation

st.set_page_config(page_title="Customer Segmentation Lab", page_icon="◈", layout="wide")
st.markdown("""<style>.block-container{padding-top:2rem;max-width:1250px}.hero{padding:2rem 0 1rem}.eyebrow{color:#19a974;font-weight:800;letter-spacing:.14em;font-size:.75rem}.hero h1{font-family:Georgia,serif;font-size:3.5rem;margin:.4rem 0}.pill{background:#d6f5e5;border-radius:20px;padding:.45rem .75rem;font-weight:700}</style>""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="eyebrow">CRISP-DM / CUSTOMER INTELLIGENCE</div><h1>Who are your customers, really?</h1><p>Turn demographics and behavior into segment-specific decisions with transparent, unsupervised learning.</p></div>', unsafe_allow_html=True)
raw, source = load_customers()
with st.sidebar:
    st.header("Controls")
    st.caption(source)
    auto_k = st.checkbox("Use best silhouette k", True)
    requested = None if auto_k else st.slider("Number of clusters", 2, 8, 5)
    show_raw = st.checkbox("Show raw data", False)

try:
    customers = clean_customers(raw)
    labeled, scores, best_k, profiles, model, transformer = fit_segmentation(customers, requested_k=requested)
except ValueError as exc:
    st.error(str(exc)); st.stop()

st.info(f"Using **k={best_k}** clusters. The default is selected by the highest silhouette score; use the sidebar to explore alternatives.")
metric_cols = st.columns(4)
metric_cols[0].metric("Customers", f"{len(labeled):,}")
metric_cols[1].metric("Segments", best_k)
metric_cols[2].metric("Best silhouette", f"{scores.loc[scores.silhouette.idxmax(), 'silhouette']:.3f}")
metric_cols[3].metric("Missing values", int(raw.isna().sum().sum()))

tab1, tab2, tab3, tab4 = st.tabs(["Segment explorer", "Model selection", "Data quality", "CRISP-DM"])
with tab1:
    left, right = st.columns([1.45, 1])
    with left:
        fig = px.scatter(labeled, x="Annual Income (k$)", y="Spending Score (1-100)", color="segment", size="Age", hover_data=["CustomerID", "Gender", "Age"], template="simple_white", title="Customer segments by income and spending")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Segment profiles")
        display = profiles.copy(); display["avg_age"] = display.avg_age.round(1); display["avg_income"] = display.avg_income.round(1); display["avg_spend"] = display.avg_spend.round(1); display["share_pct"] = display.share_pct.round(1)
        st.dataframe(display[["segment", "customers", "share_pct", "avg_age", "avg_income", "avg_spend"]].rename(columns={"segment":"Segment", "customers":"Customers", "share_pct":"Share %", "avg_age":"Age", "avg_income":"Income", "avg_spend":"Spend"}), hide_index=True, use_container_width=True)
        selected = st.selectbox("Inspect a segment", profiles.segment.tolist())
        row = profiles[profiles.segment == selected].iloc[0]
        st.markdown(f"**{selected}** — {row.action}")
    bar = px.bar(profiles, x="segment", y="customers", color="segment", title="Segment size", template="simple_white")
    st.plotly_chart(bar, use_container_width=True)
    st.download_button("Download labeled customers", labeled.to_csv(index=False).encode(), "customer_segments.csv", "text/csv")
with tab2:
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.line(scores, x="k", y="inertia", markers=True, title="Elbow method: inertia", template="simple_white"), use_container_width=True)
    with c2: st.plotly_chart(px.line(scores, x="k", y="silhouette", markers=True, title="Silhouette score", template="simple_white"), use_container_width=True)
    st.dataframe(scores.round(4), hide_index=True, use_container_width=True)
with tab3:
    st.subheader("Raw data preview")
    st.dataframe(raw.head(20), use_container_width=True, hide_index=True)
    st.write("Duplicate rows:", int(raw.duplicated().sum()))
    if show_raw: st.dataframe(raw, use_container_width=True, hide_index=True)
with tab4:
    st.markdown("""### Business understanding\nDefine a practical goal: prioritize customer marketing while avoiding one-size-fits-all campaigns.\n\n### Data understanding\nUse the Kaggle Mall Customers schema: gender, age, annual income, and spending score. The dashboard displays whether the original CSV or the deterministic fallback is active.\n\n### Data preparation\nStandardize numeric features, one-hot encode gender, coerce numeric fields, remove incomplete rows and duplicates, and validate required columns.\n\n### Modeling and evaluation\nEvaluate K-Means for k=2..8 using inertia and silhouette score. Select the maximum silhouette score, then profile each cluster by size, age, income, and spending.\n\n### Deployment\nStreamlit provides an interactive local dashboard. Download the labeled dataset for downstream activation.\n\n### Action\nSegment names are heuristic interpretations, not immutable customer identities. Revalidate them over time, monitor drift, and add purchase frequency, recency, margin, and channel behavior before production activation.""")
