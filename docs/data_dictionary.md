# Data Dictionary: Compensation & Workforce Dataset

## 1. Table: `compensation_data.csv` (Primary Employee Fact Table)
Represents the current snapshot of active employees as of January 15, 2025. Total rows: 1,250.

| Field Name | Data Type | Example Value | Description & Business Rules |
|---|---|---|---|
| `Employee_ID` | Text (PK) | `EMP-1001` | Unique employee identifier. Formatted as `EMP-XXXX`. |
| `Full_Name` | Text | `Eleanor Smith` | Anonymized synthetic employee name. |
| `Gender` | Text | `Female`, `Male`, `Non-Binary` | Self-reported gender identity. Used for pay gap and demographic composition analysis. |
| `Department` | Text | `Engineering`, `Sales`, `Finance` | High-level organizational department. |
| `Business_Function` | Text | `Technology`, `Commercial`, `Corporate` | Macro operational category grouping related departments. |
| `Job_Family` | Text | `Software Engineering`, `Data & Analytics` | Specialized career track defining the market compensation benchmark band. |
| `Job_Title` | Text | `Senior Data Analyst` | Specific functional role title. |
| `Job_Level` | Text | `L1`, `L2`, `L3`, `L4`, `L5` | Career seniority tier: `L1` (Junior/Assoc), `L2` (Mid), `L3` (Senior), `L4` (Lead/Staff), `L5` (Manager/Director). |
| `Location` | Text | `London (HQ)`, `Manchester`, `Remote (UK)` | Employee primary working location. |
| `Employment_Type` | Text | `Full-Time`, `Part-Time` | Working arrangement indicator. |
| `FTE` | Decimal | `1.0`, `0.8`, `0.6`, `0.5` | Full-Time Equivalent factor. 1.0 represents standard 37.5 - 40 hr work week. |
| `Hire_Date` | Date | `2021-08-14` | Original company start date (ISO 8601: `YYYY-MM-DD`). |
| `Tenure_Years` | Decimal | `3.4` | Completed years of service calculated as of `2025-01-15`. |
| `Performance_Rating` | Integer | `3`, `4`, `5` | Most recent annual performance appraisal rating on a 1–5 scale (3 = Meets Expectations). |
| `Annualized_Base_Salary` | Currency (GBP) | `75,000` | Full-time equivalent base salary rate before FTE scaling and bonus. Essential for like-for-like pay benchmarking. |
| `Actual_Paid_Base_Salary` | Currency (GBP) | `60,000` | Actual contractual base compensation paid to employee: `Annualized_Base_Salary * FTE`. |
| `Salary_Range_Minimum` | Currency (GBP) | `62,400` | 80% of Job Family & Level midpoint (`Midpoint * 0.80`). Band entry floor. |
| `Salary_Range_Midpoint` | Currency (GBP) | `78,000` | 100% of competitive market rate (the target benchmark for fully proficient employees). |
| `Salary_Range_Maximum` | Currency (GBP) | `93,600` | 120% of Job Family & Level midpoint (`Midpoint * 1.20`). Band ceiling. |
| `Compa_Ratio` | Decimal | `0.9615` | Compensation Ratio: `Annualized_Base_Salary / Salary_Range_Midpoint`. Values < 0.80 = Below Range; > 1.20 = Above Range. |
| `Compa_Ratio_Pct` | Decimal | `96.2` | Compa-ratio expressed as a percentage: `Compa_Ratio * 100`. |
| `Positioning_Status` | Text | `Lower Half (80-100%)` | Categorical positioning relative to band: `Below Range (<80%)`, `Lower Half (80-100%)`, `Upper Half (100-120%)`, `Above Range (>120%)`. |
| `Target_Bonus_Pct` | Decimal | `10.0` | Target incentive bonus opportunity as a percentage of annualized base salary. |
| `Actual_Bonus_Paid` | Currency (GBP) | `7,500` | Annual variable compensation payout reflecting company performance and personal rating. |
| `Total_Direct_Compensation` | Currency (GBP) | `67,500` | Total direct cash remuneration: `Actual_Paid_Base_Salary + Actual_Bonus_Paid`. |
| `Currency` | Text | `GBP` | Reporting currency code. |

---

## 2. Table: `salary_bands.csv` (Market Benchmark Reference Table)
Represents official market benchmarks across 9 Job Families and 5 Career Levels (45 total benchmark bands).

| Field Name | Data Type | Example Value | Description |
|---|---|---|---|
| `Band_ID` | Text (PK) | `BAND-DAT-L3` | Unique identifier for benchmark band. Key used in star schema dimension join. |
| `Job_Family` | Text | `Data & Analytics` | Job family name matching employee fact table. |
| `Job_Level` | Text | `L3` | Career seniority tier. |
| `Range_Minimum` | Currency (GBP) | `62,400` | 80% of midpoint. Floor of acceptable pay range. |
| `Range_Midpoint` | Currency (GBP) | `78,000` | Competitive external market median pay rate. |
| `Range_Maximum` | Currency (GBP) | `93,600` | 120% of midpoint. Ceiling of acceptable pay range. |
| `Range_Spread_Pct` | Decimal | `50.0` | Range spread percentage: `(Range_Maximum - Range_Minimum) / Range_Minimum * 100`. Standard is 50%. |
| `Currency` | Text | `GBP` | Currency code (`GBP`). |
