import pandas as pd
import numpy as np

np.random.seed(42)
n = 10000

# ── GENERATE DATASET ──────────────────────────────────────────────────────────
df = pd.DataFrame({
    "user_id": [f"user_{i:05d}" for i in range(n)],

    # A/B variant assignment
    "variant": np.random.choice(["A", "B"], size=n),

    # User segments
    "user_segment": np.random.choice(
        ["Free", "Premium"],
        size=n, p=[0.7, 0.3]
    ),
    "age_group": np.random.choice(
        ["18-24", "25-34", "35-44", "45+"],
        size=n, p=[0.35, 0.30, 0.20, 0.15]
    ),
    "region": np.random.choice(
        ["North America", "Europe", "Latin America", "Asia Pacific"],
        size=n, p=[0.40, 0.30, 0.20, 0.10]
    ),

    # Email behavior
    "send_time": np.random.choice(["Morning", "Afternoon", "Evening"], size=n),
    "subject_line": np.where(
        np.random.choice(["A", "B"], size=n) == "A",
        "Your Weekly Music Recap is Here",
        "We picked these songs just for you"
    ),
})

# ── SIMULATE REALISTIC BEHAVIOR ───────────────────────────────────────────────
# Variant B has better open rate (+8%) and click rate (+5%)
# These are realistic email marketing lift numbers

base_open_rate  = 0.22
base_click_rate = 0.08
base_conversion = 0.04

# Open rate — variant B is better
df["opened"] = np.where(
    df["variant"] == "B",
    np.random.binomial(1, base_open_rate + 0.08, n),
    np.random.binomial(1, base_open_rate, n)
)

# Click rate — only users who opened can click
df["clicked"] = np.where(
    (df["opened"] == 1) & (df["variant"] == "B"),
    np.random.binomial(1, base_click_rate + 0.05, n),
    np.where(
        df["opened"] == 1,
        np.random.binomial(1, base_click_rate, n),
        0
    )
)

# Conversion (upgrade to Premium) — only users who clicked
df["converted"] = np.where(
    (df["clicked"] == 1) & (df["variant"] == "B"),
    np.random.binomial(1, base_conversion + 0.02, n),
    np.where(
        df["clicked"] == 1,
        np.random.binomial(1, base_conversion, n),
        0
    )
)

# Premium users have higher engagement
df["opened"] = np.where(
    df["user_segment"] == "Premium",
    np.minimum(df["opened"] + np.random.binomial(1, 0.1, n), 1),
    df["opened"]
)

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("Dataset generated successfully")
print(f"Total users: {len(df):,}")
print(f"\nVariant split:")
print(df["variant"].value_counts())
print(f"\nOpen rates by variant:")
print(df.groupby("variant")["opened"].mean().mul(100).round(1).astype(str) + "%")
print(f"\nClick rates by variant:")
print(df.groupby("variant")["clicked"].mean().mul(100).round(1).astype(str) + "%")
print(f"\nConversion rates by variant:")
print(df.groupby("variant")["converted"].mean().mul(100).round(2).astype(str) + "%")

# ── SAVE ──────────────────────────────────────────────────────────────────────
df.to_csv("spotify_ab_data.csv", index=False)
print("\nSaved: spotify_ab_data.csv")
print("Run 02_analysis.py next.")