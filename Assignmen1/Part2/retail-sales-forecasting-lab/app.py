import sys
from pathlib import Path
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from src.data import clean_sales, load_sales
from src.forecast import fit_forecast

st.set_page_config(page_title="Retail Sales Forecasting Lab", page_icon="chart", layout="wide")
st.markdown("# Retail Sales Forecasting Lab")
st.caption("CRISP-DM time-series forecasting: learn from weekly retail history and plan the next few weeks.")
raw, source = load_sales()
with st.sidebar:
    st.header("Forecast controls")
    st.caption(source)
    stores = sorted(clean_sales(raw).Store.dropna().unique().tolist())
    store = st.selectbox("Store", stores)
    horizon = st.slider("Forecast horizon (weeks)", 4, 26, 12)
df = clean_sales(raw)
selected = df[df.Store == store].copy()
history, future, metrics = fit_forecast(selected, horizon)
cols = st.columns(4)
cols[0].metric("History", f"{len(selected):,} weeks")
cols[1].metric("Forecast horizon", f"{horizon} weeks")
cols[2].metric("Model MAE", f"${metrics['model_mae']:,.0f}")
improvement = (metrics["baseline_mae"] - metrics["model_mae"]) / metrics["baseline_mae"] * 100
cols[3].metric("Vs seasonal baseline", f"{improvement:+.1f}%")
tab1, tab2, tab3, tab4 = st.tabs(["Forecast", "Explore history", "Business insights", "CRISP-DM"])
with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=selected.Date, y=selected.Weekly_Sales, name="Historical sales", mode="lines", line=dict(color="#2e7d5b")))
    fig.add_trace(go.Scatter(x=history.Date, y=history.Predicted, name="Holdout predicted", mode="lines", line=dict(color="#d98b38", dash="dot")))
    fig.add_trace(go.Scatter(x=future.Date, y=future.Forecast, name="Future forecast", mode="lines+markers", line=dict(color="#496fc1", width=3)))
    fig.update_layout(title=f"Store {store}: actuals, validation predictions, and future forecast", template="simple_white", yaxis_title="Weekly sales ($)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Actual versus predicted on the chronological holdout")
    st.dataframe(history.tail(20).round(0), hide_index=True, use_container_width=True)
with tab2:
    monthly = selected.assign(Month=selected.Date.dt.month_name()).groupby("Month", sort=False).Weekly_Sales.mean().reset_index()
    st.plotly_chart(go.Figure(go.Bar(x=monthly.Month, y=monthly.Weekly_Sales, marker_color="#59a87a")).update_layout(title="Average sales by month", template="simple_white"), use_container_width=True)
    st.dataframe(selected.tail(20), hide_index=True, use_container_width=True)
with tab3:
    high = future.nlargest(3, "Forecast")
    low = future.nsmallest(3, "Forecast")
    left, right = st.columns(2)
    with left:
        st.subheader("Expected high-sales periods")
        st.dataframe(high[["Date", "Forecast", "Holiday_Flag"]].round(0), hide_index=True, use_container_width=True)
        st.write("Prepare extra inventory, labor, and promotion capacity around these weeks.")
    with right:
        st.subheader("Expected low-sales periods")
        st.dataframe(low[["Date", "Forecast", "Holiday_Flag"]].round(0), hide_index=True, use_container_width=True)
        st.write("Use quieter weeks for maintenance, targeted offers, and leaner replenishment.")
    st.download_button("Download forecast", future.to_csv(index=False).encode(), "retail_sales_forecast.csv", "text/csv")
with tab4:
    st.markdown("### CRISP-DM trace")
    st.markdown("**Business understanding:** forecast weekly sales for inventory, staffing, and promotions.\n\n**Data understanding:** use Walmart-style weekly sales with store, date, holiday, and economic context.\n\n**Data preparation:** parse dates, coerce sales, remove invalid rows and duplicate store-weeks, then create calendar and lag features.\n\n**Modeling:** compare transparent Ridge regression with a seasonal-naive lag-4 baseline using a chronological holdout.\n\n**Evaluation:** use MAE and RMSE; avoid random splits because they leak future information.\n\n**Deployment:** select a store, choose a horizon, compare predictions, and review high/low periods.")
