from itertools import combinations
from collections import Counter
import pandas as pd


def item_counts(baskets):
    counts = Counter(item for basket in baskets for item in set(basket))
    return pd.DataFrame(counts.most_common(), columns=["item", "baskets"])


def pair_counts(baskets):
    counts = Counter(pair for basket in baskets for pair in combinations(sorted(set(basket)), 2))
    return pd.DataFrame([(a, b, n) for (a, b), n in counts.most_common()], columns=["item_a", "item_b", "baskets"])


def association_rules(baskets, min_support=0.02, min_confidence=0.15):
    n = len(baskets)
    singles = Counter(item for basket in baskets for item in set(basket))
    pairs = Counter(pair for basket in baskets for pair in combinations(sorted(set(basket)), 2))
    rows = []
    for (a, b), count in pairs.items():
        support = count / n
        if support < min_support: continue
        for source, target in [(a, b), (b, a)]:
            confidence = count / singles[source]
            lift = confidence / (singles[target] / n)
            if confidence >= min_confidence:
                rows.append({"if_item": source, "then_item": target, "support": support, "confidence": confidence, "lift": lift, "pair_baskets": count})
    cols = ["if_item", "then_item", "support", "confidence", "lift", "pair_baskets"]
    return pd.DataFrame(rows, columns=cols).sort_values(["lift", "confidence"], ascending=False) if rows else pd.DataFrame(columns=cols)

