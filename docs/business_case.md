# Business Case: Compensation Benchmarking & Pay Equity Analytics

## 1. Executive Summary
**Organization:** Meridian Technologies Ltd (Fictional Mid-Sized Enterprise, ~1,250 employees)  
**Industry:** B2B Software & Digital Services  
**Sponsor:** HR Director & Head of Total Rewards / Compensation  
**Project Lead:** Business Intelligence Analyst (People Analytics)

Meridian Technologies has scaled rapidly from 400 to 1,250 employees across 5 UK locations over the past 3 years. Rapid hiring, off-cycle counteroffers, multiple acquisitions, and disparate departmental compensation practices have resulted in pay fragmentation, potential wage inequities, and lack of visibility into salary-band adherence.

This project delivers an end-to-end People Analytics & Compensation Intelligence platform to establish pay transparency, enforce salary-band governance, track compa-ratios, and audit demographic pay equity without misrepresenting statistical disparities.

---

## 2. Strategic Business Problem
Prior to this initiative, Meridian relied on ad-hoc spreadsheets maintained independently by HR Business Partners (HRBPs) and Finance. This caused three major business risks:

1. **Compensation Drift & Budget Inefficiencies:**
   - No central tracking of employees sitting **above range** ("red-circled", leading to uncontrolled payroll creep) or **below range** ("green-circled", posing critical attrition and legal risks).
   - Managers negotiating hire salaries without empirical market midpoint reference points.

2. **Compliance & Pay Equity Scrutiny:**
   - UK Gender Pay Gap Regulations require public reporting on median and mean hourly pay differences.
   - Internal employee dissatisfaction and retention risk driven by perceptions of non-transparent compensation decisions.

3. **Inconsistent Compensation Metric Standards:**
   - Failure to standardize on **FTE-Adjusted Annualized Base Pay** caused part-time workers (predominantly women in certain functions) to artificially distort base pay comparisons.
   - Conflation of **mean** (distorted by executive outliers) and **median** (robust market standard) metrics in leadership reviews.

---

## 3. Key Stakeholders & Business Questions

| Stakeholder Role | Primary Objectives | Key Decisions Supported |
|---|---|---|
| **Head of Compensation & Benefits** | Enforce salary-band governance; manage annual merit cycles; monitor market alignment. | Salary band adjustments; budgeting for out-of-band market corrections; annual bonus pool allocation. |
| **Chief People Officer (CPO) / HR Director** | Present workforce health and compliance reports to the Board; manage attrition risk. | Board-level pay equity declarations; HR compliance risk mitigation; compensation philosophy design. |
| **HR Business Partners (HRBPs)** | Advise departmental VPs on hiring offers, promotions, and off-cycle salary adjustments. | Approving/rejecting hire offers; identifying retention flight risks for below-range high performers. |
| **Finance & FP&A Director** | Forecast headcount costs and payroll run-rates; monitor variable bonus spend. | Accrual forecasting; payroll growth caps; financial impact analysis of salary adjustment cycles. |
| **Department Heads (Engineering, Sales, etc.)** | Ensure competitive compensation for talent retention while remaining within budget. | Team merit review allocation; internal promotion equity checks. |

---

## 4. Core Business Questions Answered

1. **Market Positioning & Health:**
   - What proportion of the workforce is positioned below range (<80% compa-ratio), within target (80%–120%), or above range (>120%)?
   - Which departments or job families suffer from the highest rate of out-of-band compensation?

2. **Pay Competitiveness:**
   - How does our company-wide and departmental median compa-ratio compare against our target of 100% (market parity)?
   - Are tenured employees suffering from "salary compression" (where newer hires earn more than veteran contributors in the same band)?

3. **Pay Equity & Demographics:**
   - What is the raw, unadjusted gender pay gap across Meridian Technologies?
   - How much of this raw difference is explained by **compositional effects** (unequal gender distribution across seniority levels and high-paying tech disciplines) vs. **like-for-like** within-level disparities?

---

## 5. Scope & Success Metrics
- **Phase 1 Deliverables:** Reproducible synthetic compensation dataset (1,250 records), salary-band architecture, documented methodology, and git repository.
- **Phase 2 Deliverables:** Robust Power Query transformation pipeline, Star Schema data model, 15+ validated DAX measures, and analytical SQL validation queries.
- **Phase 3 Deliverables:** Executive Power BI dashboard (Executive Overview, Salary Positioning, Pay Equity, Workforce Details), UX design system, and business recommendations.
- **Phase 4 Deliverables:** Quantitative cross-validation report, portfolio documentation,