# Grocery Market Basket Lab — CRISP-DM Report

## Business understanding

The store wants to understand which products are bought together. Useful outputs are product placement ideas, bundles, online recommendations, and replenishment priorities.

## Data understanding

The Kaggle Groceries Market Basket Dataset records grocery baskets. Depending on the file version, a row may contain several items or a transaction identifier plus one item. The loader detects both common layouts.

## Data preparation

Item names are converted to lowercase, whitespace is trimmed, empty values are removed, and duplicate products inside a basket are collapsed. This prevents repeated cells from inflating frequency.

## Modeling

For each basket, the project counts unique items and all unordered item pairs. It calculates support, confidence, and lift for rules in both directions. Support is the share of baskets containing both items; confidence is the share containing Y among baskets containing X; lift compares that confidence with Y's overall popularity.

## Evaluation

Rules should be filtered by support and confidence, then checked for lift, stability, margin, seasonality, and usefulness. A rule with high lift but very few baskets should not drive a store-wide change without validation.

## Business interpretation

Frequent pairs can be placed closer together or used in recipe signage. High-lift pairs can power online “often bought together” recommendations. Popular individual items deserve strong availability because their absence can break many baskets.

## Limitations and next steps

Co-occurrence does not prove that one product causes another purchase. Add dates, prices, promotions, store location, and privacy-safe customer IDs to study seasonality and personalize responsibly. Test recommendations with conversion, basket size, margin, and customer satisfaction metrics.

