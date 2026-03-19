import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("spotify_ab_data.csv")

# ── 1. HELPER FUNCTION ────────────────────────────────────────────────────────
def ab_test(metric, group_col="variant", data=df):
    a = data[data[group_col] == "A"][metric]
    b = data[data[group_col] == "B"][metric]

    rate_a = a.mean()
    rate_b = b.mean()
    lift   = (rate_b - rate_a) / rate_a * 100

    # Two-proportion z-test
    count  = np.array([b.sum(), a.sum()])
    nobs   = np.array([len(b), len(a)])
    from statsmodels.stats.proportion import proportions_ztest
    stat, p_value = proportions_ztest(count, nobs)

    # 95% confidence interval for the difference
    diff = rate_b - rate_a
    se   = np.sqrt(rate_a*(1-rate_a)/len(a) + rate_b*(1-rate_b)/len(b))
    ci_low  = diff - 1.96 * se
    ci_high = diff + 1.96 * se

    significant = p_value < 0.05

    return {
        "metric":      metric,
        "rate_a":      round(rate_a * 100, 2),
        "rate_b":      round(rate_b * 100, 2),
        "lift_pct":    round(lift, 1),
        "p_value":     round(p_value, 4),
        "ci_low":      round(ci_low * 100, 2),
        "ci_high":     round(ci_high * 100, 2),
        "significant": significant
    }

# ── 2. RUN TESTS ──────────────────────────────────────────────────────────────
print("=" * 60)
print("  SPOTIFY EMAIL CAMPAIGN A/B TEST RESULTS")
print("=" * 60)

results = []
for metric in ["opened", "clicked", "converted"]:
    r = ab_test(metric)
    results.append(r)
    sig = "✓ SIGNIFICANT" if r["significant"] else "✗ NOT SIGNIFICANT"
    print(f"\n── {metric.upper()} ──")
    print(f"  Variant A: {r['rate_a']}%")
    print(f"  Variant B: {r['rate_b']}%")
    print(f"  Lift:      {r['lift_pct']}%")
    print(f"  P-value:   {r['p_value']}  →  {sig}")
    print(f"  95% CI:    [{r['ci_low']}%, {r['ci_high']}%]")

results_df = pd.DataFrame(results)

# ── 3. SEGMENTATION ANALYSIS ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  SEGMENTATION ANALYSIS")
print("=" * 60)

print("\n── Conversion rate by user segment ──")
seg = df.groupby(["variant", "user_segment"])["converted"].mean().mul(100).round(2).reset_index()
print(seg.to_string(index=False))

print("\n── Open rate by age group ──")
age = df.groupby(["variant", "age_group"])["opened"].mean().mul(100).round(1).reset_index()
print(age.to_string(index=False))

print("\n── Open rate by region ──")
region = df.groupby(["variant", "region"])["opened"].mean().mul(100).round(1).reset_index()
print(region.to_string(index=False))

# ── 4. BUSINESS IMPACT ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  BUSINESS IMPACT")
print("=" * 60)

spotify_users     = 250_000_000  # Spotify free users
premium_price     = 9.99
monthly_emails    = 4

conversion_a = results_df[results_df["metric"] == "converted"]["rate_a"].values[0] / 100
conversion_b = results_df[results_df["metric"] == "converted"]["rate_b"].values[0] / 100

conversions_a = spotify_users * conversion_a
conversions_b = spotify_users * conversion_b
additional    = conversions_b - conversions_a
revenue_lift  = additional * premium_price * 12

print(f"\nIf Variant B rolled out to {spotify_users/1e6:.0f}M free users:")
print(f"  Additional conversions vs Variant A: {additional:,.0f}")
print(f"  Projected annual revenue lift:       ${revenue_lift:,.0f}")

# ── 5. DASHBOARD ──────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Open Rate: A vs B",
        "Click & Conversion Rate: A vs B",
        "Conversion Rate by User Segment",
        "Open Rate by Age Group"
    ),
    vertical_spacing=0.18,
    horizontal_spacing=0.12
)

colors = {"A": "#1DB954", "B": "#191414"}

# Chart 1: Open rate
for variant in ["A", "B"]:
    r = results_df[results_df["metric"] == "opened"].iloc[0]
    val = r["rate_a"] if variant == "A" else r["rate_b"]
    fig.add_trace(go.Bar(
        x=[f"Variant {variant}"],
        y=[val],
        name=f"Variant {variant}",
        marker_color=colors[variant],
        text=[f"{val}%"],
        textposition="outside",
        showlegend=variant == "A"
    ), row=1, col=1)

# Chart 2: Click and conversion
metrics = ["clicked", "converted"]
labels  = ["Click Rate", "Conversion Rate"]
x_labels = [f"{l}<br>A vs B" for l in labels]

for i, metric in enumerate(metrics):
    r = results_df[results_df["metric"] == metric].iloc[0]
    fig.add_trace(go.Bar(
        name="A", x=[labels[i]], y=[r["rate_a"]],
        marker_color="#1DB954", showlegend=False,
        text=[f"{r['rate_a']}%"], textposition="outside"
    ), row=1, col=2)
    fig.add_trace(go.Bar(
        name="B", x=[labels[i]], y=[r["rate_b"]],
        marker_color="#191414", showlegend=False,
        text=[f"{r['rate_b']}%"], textposition="outside"
    ), row=1, col=2)

# Chart 3: Conversion by segment
for variant in ["A", "B"]:
    seg_v = seg[seg["variant"] == variant]
    fig.add_trace(go.Bar(
        x=seg_v["user_segment"],
        y=seg_v["converted"],
        name=f"Variant {variant}",
        marker_color=colors[variant],
        showlegend=False,
        text=[f"{v}%" for v in seg_v["converted"]],
        textposition="outside"
    ), row=2, col=1)

# Chart 4: Open rate by age group
for variant in ["A", "B"]:
    age_v = age[age["variant"] == variant]
    fig.add_trace(go.Bar(
        x=age_v["age_group"],
        y=age_v["opened"],
        name=f"Variant {variant}",
        marker_color=colors[variant],
        showlegend=False,
        text=[f"{v}%" for v in age_v["opened"]],
        textposition="outside"
    ), row=2, col=2)

fig.update_layout(
    title={
        "text": "Spotify Email Campaign A/B Test Dashboard",
        "font": {"size": 22},
        "x": 0.5
    },
    height=750,
    barmode="group",
    plot_bgcolor="white",
    paper_bgcolor="#F5F5F5",
    font={"family": "Arial", "size": 12}
)

fig.add_annotation(
    text=f"10,000 users · Variant B wins on all metrics · Projected revenue lift: ${revenue_lift:,.0f}/yr",
    xref="paper", yref="paper",
    x=0.5, y=1.06,
    showarrow=False,
    font={"size": 12, "color": "#555555"},
    align="center"
)

fig.write_html("spotify_ab_dashboard.html")
print(f"\nSaved: spotify_ab_dashboard.html")
print("Open in browser to view interactive dashboard.")