# Customer Segmentation Lab — CRISP-DM Report

## Business understanding

The business question is: how can marketing and customer-success teams prioritize actions when customers have different value and engagement patterns? The output is a segment label plus a profile and recommended treatment. The goal is interpretability and useful campaign differentiation, not a prediction leaderboard.

## Data understanding

The project uses the public Kaggle Mall Customers dataset schema: `CustomerID`, `Gender`, `Age`, `Annual Income (k$)`, and `Spending Score (1-100)`. The app supports the original CSV and includes a deterministic fallback with the same schema so the demo is reproducible without credentials. A production analysis should document the collection period, sampling bias, and the meaning of the spending score.

## Data preparation

Column names are normalized, required columns are validated, numeric fields are coerced, incomplete rows are removed, and duplicates are dropped. Age, income, and spending score are standardized. Gender is one-hot encoded. Standardization matters because K-Means uses Euclidean distance and income otherwise dominates the scale.

## Modeling

K-Means is fitted with `n_init=20` and `random_state=42`. Candidate values from 2 through 8 are evaluated. Inertia supports the elbow method; silhouette score measures separation and cohesion. The highest silhouette score is used as the default, while the sidebar lets a user explore another k.

## Evaluation and interpretation

Each cluster is profiled with customer count, share, average age, income, and spending. Heuristic names translate the two strongest business dimensions into four archetypes: Premium Champions, Affluent Cautious, Emerging Enthusiasts, and Value Conservers. These names should be reviewed with domain owners and validated against campaign outcomes.

## Deployment

The Streamlit app presents the full flow from raw data to cleaned features, model selection charts, labeled customers, cluster profiles, and targeted actions. A CSV download supports activation in a CRM or campaign workflow.

## Business actions

- **Premium Champions:** loyalty tiers, early access, high-touch service, and referral programs.
- **Affluent Cautious:** education, bundles, guarantees, and trust-building offers.
- **Emerging Enthusiasts:** personalized discovery, social proof, and limited-time offers.
- **Value Conservers:** value packs, essentials, price-sensitive promotions, and reactivation.

## Limitations and next steps

The Mall Customers dataset is small and its spending score is an already-aggregated behavioral proxy. Add recency, frequency, monetary value, margin, product affinity, geography, and channel engagement before production use. Test cluster stability across random seeds and time windows, then measure incremental campaign lift rather than assuming segment value.

