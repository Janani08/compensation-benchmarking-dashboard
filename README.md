# Compensation Benchmarking & Pay Analysis Dashboard

![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Analytics-CC292B?style=for-the-badge&logo=sqlite&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-Advanced_Measures-005FB8?style=for-the-badge)
![Status](https://img.shields.io/badge/Portfolio-Phase_1_Complete-success?style=for-the-badge)

An end-to-end People Analytics and Business Intelligence project simulating enterprise compensation benchmarking, salary-band positioning, compa-ratio governance, and pay equity analysis for a mid-sized technology enterprise (~1,250 employees).

---

## 📌 Executive Overview & Business Problem

Rapid organizational growth, decentralized hiring, and legacy off-cycle salary negotiations often create compensation drift, salary compression, and potential pay equity compliance vulnerabilities.

This project designs and delivers a production-grade compensation intelligence solution for **Meridian Technologies Ltd**, empowering the **Head of Total Rewards**, **HR Director**, and **HR Business Partners** to:
1. **Audit Salary Positioning:** Identify "green-circled" employees paid below range (<80% compa-ratio, retention risk) and "red-circled" employees above range (>120%, budget risk).
2. **Standardize Compensation Benchmarks:** Establish market-anchored salary bands across 9 job families and 5 seniority tiers.
3. **Analyze Pay Equity with Rigor:** Quantify raw vs. like-for-like gender pay gaps, isolating compositional workforce effects from direct role-for-role disparities.
4. **Normalize for Working Hours:** Ensure all benchmarks use FTE-adjusted annualized base pay to prevent part-time distortion.

---

## 🏗️ Project Architecture & Pipeline

```text
Business Problem & Stakeholder Requirements
           ↓
Synthetic Compensation Data Generation (Python, Seed: 42)
           ↓
Power Query ETL & Normalization Pipeline (Phase 2)
           ↓
Star Schema Data Model & DAX KPI Layer (Phase 2)
           ↓
Interactive Power BI Dashboard (3-4 Pages) (Phase 3)
           ↓
Business Validation, Governance & Portfolio Case Study (Phase 4)
```

---

## 📂 Repository Structure

```text
├── data/
│   └── raw/
│       ├── compensation_data.csv       # Employee-level fact data (1,250 records)
│       └── salary_bands.csv            # Market benchmark structure (45 bands)
├── docs/
│   ├── business_case.md                # Organizational background, stakeholders & KPIs
│   ├── data_dictionary.md              # Field-level metadata and business rules
│   ├── methodology.md                  # Compensation theory, compa-ratios, pay gap math
│   ├── kpi_definitions.md              # (Phase 2) DAX metric specifications
│   ├── dashboard_design.md             # (Phase 3) Design system and UX standards
│   └── validation.md                   # (Phase 4) Cross-platform validation report
├── sql/
│   └── compensation_analysis.sql       # (Phase 2) Analytical SQL queries for cross-validation
├── src/
│   ├── generate_data.py                # Reproducible synthetic data generation script
│   └── App.tsx                         # Portfolio companion web dashboard / viewer
├── .gitignore                          # Clean exclusions (environments, caches, temp files)
└── README.md                           # Project documentation entry point
```

---

## ⚡ Quick Start: Environment Setup & Data Generation

### 1. Create and Activate Conda Environment
```bash
# Create dedicated environment
conda create -n comp-analytics python=3.10 -y

# Activate environment
conda activate comp-analytics

# Install analysis libraries
pip install pandas numpy
```

### 2. Generate the Dataset
The data generator uses a fixed random seed (`42`) to guarantee 100% deterministic reproducibility across systems:
```bash
python src/generate_data.py
```

### 3. Baseline Data Sanity Check Output
Running the generator produces:
- **Total Headcount:** 1,250 active employees (1,221.2 FTE)
- **Median Annualized Base Salary:** £59,500 (Mean: £64,412)
- **Median Compa-Ratio:** 101.56% (Well-calibrated market parity)
- **Below Range (<80%):** 60 employees (4.8%) — retention alert
- **Above Range (>120%):** 59 employees (4.7%) — budget review
- **Raw Gender Pay Gap:** 4.9% median gap (driven by seniority and technical family representation)

---

## 🎯 Next Step: Phase 2 (Power Query, Data Model, DAX & SQL)
In Phase 2, we ingest `compensation_data.csv` and `salary_bands.csv` into Power BI, design a star schema data model, author 15+ production DAX measures, and cross-validate metrics with SQL queries.
