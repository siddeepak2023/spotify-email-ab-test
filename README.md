# spotify-email-ab-test[spotify_README (1).md](https://github.com/user-attachments/files/26105068/spotify_README.1.md)
# Spotify Email Campaign A/B Test Analysis

A statistical analysis of a simulated Spotify email marketing A/B test across 10,000 users. Tests whether a personalized subject line drives higher open rates, click rates, and Premium conversions than a generic one.

---

## Business Problem

Spotify sends hundreds of millions of emails monthly to convert free users to Premium. A 1% improvement in conversion rate across 250M free users generates millions in additional revenue. This project tests two email subject lines and uses statistical hypothesis testing to determine which performs better — and whether the results are statistically significant.

---

## Hypothesis

- **H₀ (Null):** There is no difference in conversion rate between Variant A and Variant B
- **H₁ (Alternative):** Variant B has a higher conversion rate than Variant A
- **Significance level:** α = 0.05

---

## Variants Tested

| Variant | Subject Line |
|---|---|
| A (Control) | "Your Weekly Music Recap is Here" |
| B (Treatment) | "We picked these songs just for you" |

---

## Results

| Metric | Variant A | Variant B | Lift | P-Value | Significant? |
|---|---|---|---|---|---|
| Open Rate | 25.2% | 32.1% | +27.5% | < 0.001 | ✅ Yes |
| Click Rate | 1.7% | 3.7% | +118.8% | < 0.001 | ✅ Yes |
| Conversion Rate | 0.06% | 0.34% | +469.6% | 0.0017 | ✅ Yes |

**Conclusion: Reject H₀. Variant B wins on all three metrics with statistical significance.**

---

## Business Impact

If Variant B is rolled out to all 250M Spotify free users:
- **Additional conversions:** ~700,000 new Premium subscribers
- **Projected annual revenue lift: $83,916,000**

---

## Dashboard

Open `spotify_ab_dashboard.html` in your browser for the interactive version.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data generation & analysis |
| SciPy, Statsmodels | Statistical hypothesis testing |
| Plotly | Interactive dashboard |

---

## Dataset

**Type:** Synthetic dataset generated to simulate realistic Spotify email campaign behavior  
**Size:** 10,000 users (5,013 Variant A / 4,987 Variant B)  
**Benchmarks used:** Mailchimp 2023 industry averages (21.33% avg open rate for music/entertainment)  
**Features:** variant, user_segment, age_group, region, send_time, opened, clicked, converted

---

## Project Structure

```
spotify_ab_test/
│
├── 01_generate_data.py      # Synthetic dataset generation with realistic parameters
├── 02_analysis.py           # Statistical tests, segmentation & business impact
│
├── spotify_ab_data.csv      # Generated dataset (10,000 users)
├── spotify_ab_dashboard.html # Interactive results dashboard
│
└── README.md
```

---

## Statistical Methodology

Two-proportion z-test was used for all metrics since we're comparing proportions between two independent groups:

```python
from statsmodels.stats.proportion import proportions_ztest

count = np.array([b.sum(), a.sum()])
nobs  = np.array([len(b), len(a)])
stat, p_value = proportions_ztest(count, nobs)

# 95% confidence interval for the difference
diff    = rate_b - rate_a
se      = np.sqrt(rate_a*(1-rate_a)/len(a) + rate_b*(1-rate_b)/len(b))
ci_low  = diff - 1.96 * se
ci_high = diff + 1.96 * se
```

**95% Confidence Interval for conversion rate difference: [0.11%, 0.46%]**  
The interval does not contain 0, confirming statistical significance.

---

## Segmentation Findings

- Variant B outperforms across **all age groups** — strongest lift in 25-34 segment
- Variant B outperforms across **all regions** — strongest lift in Asia Pacific (+9.5%)
- Both Free and Premium users respond better to Variant B — personalization works universally

---

## Business Recommendations

1. **Roll out Variant B immediately** — all three metrics are statistically significant with p < 0.05 and the projected revenue lift is $83.9M annually.

2. **Prioritize the 25-34 segment** — highest open rate lift from personalization. Consider further segmenting this group for even more targeted messaging.

3. **Test deeper personalization** — if a personalized subject line drives 470% conversion lift, testing personalized email body content could compound these gains further.

4. **Monitor long-term** — run a follow-up test after 90 days to check if the lift holds or if users habituate to the personalized style.

---

*Built by Siddharth Deepak | Business Analytics & AI, UT Dallas*
