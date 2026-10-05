# Compensation Analytics & Pay Equity Methodology

## 1. Core Compensation Concepts & Frameworks

### 1.1 The Market-Anchored Salary Band System
A modern corporate salary band structure is designed around external market benchmark midpoints:
- **Range Midpoint (100%):** Represents the competitive median market rate for an experienced, fully proficient performer in that specific job family and level.
- **Range Minimum (80%):** The band entry floor. Typically assigned to new hires who meet minimum qualifications or recent internal promotees developing into the role.
- **Range Maximum (120%):** The compensation ceiling. Reserved for sustained top performers, technical fellows, or critical retainees.
- **Range Spread:** Calculated as `(Maximum - Minimum) / Minimum`. In our model, a standard 50% spread is maintained across all levels:
  $$\text{Spread} = \frac{1.20 - 0.80}{0.80} = 50.0\%$$
- **Band Overlap:** Consecutive levels overlap deliberately (e.g., an exceptional L2 developer can earn up to £74,400, which exceeds the entry rate for an L3 developer at £68,000). This avoids forcing technical contributors into management simply to attain market compensation.

---

### 1.2 Compa-Ratio (Comparative Ratio)
Compa-ratio is the standard human capital metric for evaluating an employee's salary positioning against the market:
$$\text{Compa-Ratio} = \frac{\text{Annualized Base Salary}}{\text{Salary Range Midpoint}}$$

#### Interpretation Bands:
| Compa-Ratio Range | Category | Business Implication | HR Recommended Action |
|---|---|---|---|
| **< 0.80 (<80%)** | **Below Range ("Green-Circled")** | Severe retention flight risk; potential equal pay compliance vulnerability. | Immediate equity adjustment or promotion review; investigate if manager is underpaying talent. |
| **0.80 – 0.90** | **Developing / Early in Role** | Normal for recent college grads or new promotees still mastering core competencies. | Standard merit progression; planned step-increases. |
| **0.90 – 1.10** | **Competitive Market Target** | Healthy operational target for the vast majority of experienced staff. | Market-rate annual cost-of-living and performance adjustments. |
| **1.10 – 1.20** | **Upper Band / Top Contributor** | Seasoned, high-performing experts delivering exceptional sustained business value. | Slower salary growth; prioritize incentive bonuses over base raises. |
| **> 1.20 (>120%)** | **Above Range ("Red-Circled")** | Budget inefficiency; salary cap risk; potential internal friction. | Freeze base salary increases; transition compensation to one-off lump-sum bonuses or promote to next level. |

---

### 1.3 FTE Normalization (Full-Time Equivalent)
A critical error in amateur people analytics is comparing raw contractual earnings across employees with different working hours. 
- An employee working 3 days a week (0.6 FTE) earning £36,000 actually has an **annualized base salary rate of £60,000** ($\frac{£36,000}{0.6}$).
- If evaluated on raw cash received, this employee appears to suffer a 40% pay penalty. Because part-time arrangements in many industries have higher female representation, failing to normalize for FTE severely biases gender pay gap analyses.
- **Rule:** All market benchmarking, compa-ratio calculations, and pay equity evaluations **must** use `Annualized_Base_Salary`. `Actual_Paid_Base_Salary` is reserved strictly for financial payroll budgeting and headcount cash expenditure reporting.

---

### 1.4 Median vs. Mean in Compensation Analysis
- **Mean (Average):** Highly sensitive to executive salaries and extreme positive skewness. A single C-level salary of £300,000 pulls the department average upwards, masking widespread underpayment at lower tiers.
- **Median (50th Percentile):** Robust against outliers and non-normal distributions. Regulatory standards (such as UK Government Gender Pay Gap regulations) require median figures as the primary benchmark because they accurately represent the typical employee's experience.
- **Guideline:** This dashboard reports **both**, but uses **Median** as the primary executive KPI.

---

## 2. Pay Equity & The Gender Pay Gap: Descriptive vs. Causal

### 2.1 The Critical Distinction: Raw Gap vs. Like-for-Like Gap
In business intelligence, conflating a raw pay disparity with unlawful discrimination is statistically flawed and legally irresponsible.

1. **Raw (Unadjusted) Gender Pay Gap:**
   $$\text{Raw Gap} = \frac{\text{Median Male Salary} - \text{Median Female Salary}}{\text{Median Male Salary}} \times 100$$
   - Measures the difference in overall median earnings across the entire company without controlling for job role, career level, or department.
   - A positive raw gap usually reflects **occupational segregation** or **unequal senior representation** (the "broken rung" phenomenon where more senior roles are held by men, and high-paying engineering disciplines have lower female participation).

2. **Like-for-Like (Adjusted) Pay Disparity:**
   $$\text{Within-Tier Gap} = \frac{\text{Median Male Salary}_{(\text{Family } j, \text{Level } l)} - \text{Median Female Salary}_{(\text{Family } j, \text{Level } l)}}{\text{Median Male Salary}_{(\text{Family } j, \text{Level } l)}} \times 100$$
   - Compares individuals performing substantially similar work at the same career level within the same job family.
   - If a significant disparity remains after controlling for job family, seniority, and performance rating, it warrants immediate investigation by People Operations.

### 2.2 Simpson's Paradox in HR Analytics
Simpson's paradox occurs when an apparent pay gap appears at the aggregated company level, but reverses or disappears when data is partitioned by job level and job family. Our synthetic dataset realistically models this:
- Aggregated raw median gap is **~4.9%** across the 1,250 employees.
- When disaggregated by level (e.g., L2 Mid-level), the disparity shrinks significantly to within normal variance (~1–3%), proving that organizational composition is the primary driver of top-level divergence.

---

## 3. Synthetic Data Generation Architecture

The dataset is generated via `src/generate_data.py` using a fixed random seed (`RANDOM_SEED = 42`):
- **Reproducibility:** Every run produces identical data points, enabling deterministic testing, SQL verification, and DAX auditability.
- **Gaussian Noise Modeling:** Individual compa-ratios are sampled from $\mathcal{N}(\mu=0.98, \sigma=0.075)$, with mild positive regression coefficients for tenure and performance rating.
- **Controlled Outliers:** Exactly ~4.8% below range and ~4.7% above range are injected to mirror typical enterprise compensation distributions without creating unexplainable artifacts.
- **Demographic Weights:** Gender distributions across technical, sales, and corporate job families reflect contemporary UK tech industry employment statistics.
