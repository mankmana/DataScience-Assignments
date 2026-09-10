import sys
from pathlib import Path
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from src.data import load_baskets
from src.market_basket import association_rules, item_counts, pair_counts

st.set_page_config(page_title="Grocery Market Basket Lab", page_icon="shopping cart", layout="wide")
st.markdown("# Grocery Market Basket Lab")
st.caption("CRISP-DM retail analytics: discover which items are commonly bought together.")
baskets, source = load_baskets()
counts, pairs = item_counts(baskets), pair_counts(baskets)
with st.sidebar:
    st.header("Analysis controls")
    st.caption(source)
    min_support = st.slider("Minimum pair support", 0.01, 0.20, 0.03, 0.01)
    min_conf = st.slider("Minimum confidence", 0.05, 0.90, 0.20, 0.05)
rules = association_rules(baskets, min_support, min_conf)
c = st.columns(4)
c[0].metric("Baskets", f"{len(baskets):,}")
c[1].metric("Unique items", f"{len(counts):,}")
c[2].metric("Item pairs", f"{len(pairs):,}")
c[3].metric("Useful rules", f"{len(rules):,}")
st.info("A rule such as whole milk -> rolls/buns means rolls/buns often appears when whole milk is in a basket. Lift above 1 means the pair occurs more often than chance.")
t1, t2, t3, t4 = st.tabs(["Popular items", "Shopping patterns", "Store recommendations", "CRISP-DM"])
with t1:
    fig = px.bar(counts.head(15).sort_values("baskets"), x="baskets", y="item", orientation="h", title="Most common grocery items", template="simple_white", color="baskets", color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(counts.head(30), hide_index=True, use_container_width=True)
with t2:
    left, right = st.columns([1.2, 1])
    with left:
        view = pairs.head(20).copy()
        view["pair"] = view.item_a + " + " + view.item_b
        fig = px.bar(view.sort_values("baskets"), x="baskets", y="pair", orientation="h", title="Most common item combinations", template="simple_white", color="baskets", color_continuous_scale="Teal")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Association rules")
        if rules.empty:
            st.info("Lower the support or confidence threshold to see more rules.")
        else:
            shown = rules.head(20).copy()
            shown["rule"] = shown.if_item + " -> " + shown.then_item
            shown["support"] = shown.support.round(3)
            shown["confidence"] = shown.confidence.round(3)
            shown["lift"] = shown.lift.round(2)
            st.dataframe(shown[["rule", "support", "confidence", "lift"]], hide_index=True, use_container_width=True)
with t3:
    st.subheader("Simple actions a store can test")
    for title, body in [("Cross-merchandise frequent pairs", "Place commonly paired products closer together or display a recipe card."), ("Create complementary bundles", "Offer a light discount on a high-lift pair while protecting margin."), ("Plan replenishment together", "Use frequent items to prioritize shelf availability."), ("Personalize suggestions", "Recommend the right-hand item when a customer adds the left-hand item online.")]:
        st.markdown(f"**{title}** — {body}")
    st.download_button("Download association rules", rules.to_csv(index=False).encode(), "grocery_association_rules.csv", "text/csv")
with t4:
    st.markdown("### CRISP-DM trace")
    st.markdown("**Business understanding:** improve merchandising, bundles, recommendations, and availability.\n\n**Data understanding:** inspect grocery basket frequency and item coverage.\n\n**Data preparation:** normalize names, remove empty values, and deduplicate items per basket.\n\n**Modeling:** count pairs and calculate support, confidence, and lift.\n\n**Evaluation:** review stability, margin, seasonality, and business usefulness.\n\n**Deployment:** use this dashboard to test store actions and download rules.")
