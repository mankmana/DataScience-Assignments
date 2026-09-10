# Grocery Market Basket Lab

An easy-to-explain end-to-end project that discovers which grocery products are purchased together. It follows CRISP-DM and presents item popularity, pair co-occurrence, simple association rules, and store recommendations in an interactive Streamlit dashboard.


##Prompt used
We will build another project now.

Build a simple end-to-end data science project using the Kaggle Groceries Dataset.
The goal is to find which grocery items are commonly bought together.
Follow the CRISP-DM framework.

Clean the data, explore the most common items, and identify useful shopping patterns such as people who buy milk also often buy eggs.
Create a simple dashboard that shows the most common items, common item combinations, and a few useful recommendations for a store.
Keep the project easy to understand and easy to explain in a student presentation.

Include a README with the dataset, what the project does, the main results, and how to run it locally.

##YT Link
https://youtu.be/6Fq1HVba1gA


## Dataset

The app accepts common versions of the Kaggle Groceries Market Basket Dataset. Place the downloaded file at `data/groceries.csv`. It supports one row per basket with item names in columns such as `Item 1`, `Item 2`, or one row per purchase with a basket identifier and item column. If no CSV is present, a deterministic demo dataset is used.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## What it does

1. Loads and cleans grocery baskets.
2. Counts the most common items.
3. Finds item pairs purchased in the same basket.
4. Calculates support, confidence, and lift for `X -> Y` rules.
5. Gives store actions such as cross-merchandising, bundles, and replenishment priorities.

The demo highlights familiar patterns such as whole milk with rolls/buns, yogurt with tropical fruit, and sausage with root vegetables. Replace the fallback with the Kaggle CSV before making claims about the real dataset.

