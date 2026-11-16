-- ==============================================================================
-- Meridian Technologies - Compensation & Pay Equity Analysis SQL Workbench
-- Target Database: PostgreSQL / DuckDB / SQLite / BigQuery compatible
-- Author: BI Analyst Portfolio
-- Purpose: Independent analytical cross-validation against Power BI DAX KPIs
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Executive KPI Summary
-- Business Purpose: Single-row audit card verifying Headcount, FTE, Salary stats,
-- and out-of-band anomalies across the enterprise.
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_headcount,
    ROUND(SUM(FTE), 1) AS total_fte,
    ROUND(AVG(Annualized_Base_Salary), 2) AS mean_annualized_salary,
    -- In standard SQL (Postgres/DuckDB), PERCENTILE_CONT(0.5) computes the true median:
    -- In SQLite, median can be derived via sorted subqueries or window functions.
    ROUND(AVG(Compa_Ratio) * 100, 2) AS mean_compa_ratio_pct,
    SUM(CASE WHEN Compa_Ratio < 0.80 THEN 1 ELSE 0 END) AS employees_below_range,
    ROUND(SUM(CASE WHEN Compa_Ratio < 0.80 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS pct_below_range,
    SUM(CASE WHEN Compa_Ratio > 1.20 THEN 1 ELSE 0 END) AS employees_above_range,
    ROUND(SUM(CASE WHEN Compa_Ratio > 1.20 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS pct_above_range,
    ROUND(SUM(Actual_Paid_Base_Salary), 2) AS total_actual_base_payroll,
    ROUND(SUM(Actual_Bonus_Paid), 2) AS total_bonus_payroll,
    ROUND(SUM(Total_Direct_Compensation), 2) AS total_payroll_expenditure
FROM compensation_data;

-- ------------------------------------------------------------------------------
-- QUERY 2: Departmental Compensation & Compa-Ratio Health Check
-- Business Purpose: Identifies departments with budget creep (>102% compa-ratio)
-- or high attrition risk (>5% below band).
-- ------------------------------------------------------------------------------
SELECT 
    Department,
    COUNT(*) AS headcount,
    ROUND(SUM(FTE), 1) AS total_fte,
    ROUND(AVG(Annualized_Base_Salary), 0) AS avg_annualized_salary,
    ROUND(AVG(Compa_Ratio) * 100, 1) AS avg_compa_ratio_pct,
    SUM(CASE WHEN Compa_Ratio < 0.80 THEN 1 ELSE 0 END) AS count_below_range,
    ROUND(SUM(CASE WHEN Compa_Ratio < 0.80 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_below_range,
    SUM(CASE WHEN Compa_Ratio > 1.20 THEN 1 ELSE 0 END) AS count_above_range,
    ROUND(SUM(CASE WHEN Compa_Ratio > 1.20 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_above_range
FROM compensation_data
GROUP BY Department
ORDER BY avg_annualized_salary DESC;

-- ------------------------------------------------------------------------------
-- QUERY 3: Seniority Level Headcount & Salary Distribution
-- Business Purpose: Verifies corporate career pyramid shape and salary progression.
-- ------------------------------------------------------------------------------
SELECT 
    Job_Level,
    COUNT(*) AS headcount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM compensation_data), 1) AS pct_of_workforce,
    ROUND(AVG(Annualized_Base_Salary), 0) AS avg_salary,
    MIN(Annualized_Base_Salary) AS min_salary_observed,
    MAX(Annualized_Base_Salary) AS max_salary_observed,
    ROUND(AVG(Tenure_Years), 1) AS avg_tenure_years,
    ROUND(AVG(Compa_Ratio) * 100, 1) AS avg_compa_ratio_pct
FROM compensation_data
GROUP BY Job_Level
ORDER BY 
    CASE Job_Level 
        WHEN 'L1' THEN 1 
        WHEN 'L2' THEN 2 
        WHEN 'L3' THEN 3 
        WHEN 'L4' THEN 4 
        WHEN 'L5' THEN 5 
    END;

-- ------------------------------------------------------------------------------
-- QUERY 4: Demographic Representation & Raw Pay Gap by Level
-- Business Purpose: Demonstrates like-for-like analysis. Highlights that raw gap
-- is heavily influenced by representation at senior tiers (L4/L5).
-- ------------------------------------------------------------------------------
WITH LevelGenderStats AS (
    SELECT 
        Job_Level,
        Gender,
        COUNT(*) AS headcount,
        AVG(Annualized_Base_Salary) AS mean_salary,
        AVG(Compa_Ratio) AS mean_compa_ratio
    FROM compensation_data
    WHERE Gender IN ('Male', 'Female')
    GROUP BY Job_Level, Gender
)
SELECT 
    m.Job_Level,
    m.headcount AS male_count,
    f.headcount AS female_count,
    ROUND(m.headcount * 100.0 / (m.headcount + f.headcount), 1) AS male_pct_share,
    ROUND(f.headcount * 100.0 / (m.headcount + f.headcount), 1) AS female_pct_share,
    ROUND(m.mean_salary, 0) AS male_avg_salary,
    ROUND(f.mean_salary, 0) AS female_avg_salary,
    ROUND((m.mean_salary - f.mean_salary) / m.mean_salary * 100, 2) AS mean_gender_pay_gap_pct,
    ROUND((m.mean_compa_ratio - f.mean_compa_ratio) * 100, 2) AS compa_ratio_gap_pct
FROM LevelGenderStats m
JOIN LevelGenderStats f 
    ON m.Job_Level = f.Job_Level 
    AND m.Gender = 'Male' 
    AND f.Gender = 'Female'
ORDER BY 
    CASE m.Job_Level 
        WHEN 'L1' THEN 1 
        WHEN 'L2' THEN 2 
        WHEN 'L3' THEN 3 
        WHEN 'L4' THEN 4 
        WHEN 'L5' THEN 5 
    END;

-- ------------------------------------------------------------------------------
-- QUERY 5: Top Priority Out-of-Band Audit (Actionable HR Exception List)
-- Business Purpose: Generates operational hit-list of employees requiring
-- immediate HRBP intervention (either below 80% or above 120%).
-- ------------------------------------------------------------------------------
SELECT 
    Employee_ID,
    Full_Name,
    Department,
    Job_Family,
    Job_Level,
    Job_Title,
    Location,
    Tenure_Years,
    Performance_Rating,
    Annualized_Base_Salary,
    Salary_Range_Minimum,
    Salary_Range_Midpoint,
    Salary_Range_Maximum,
    ROUND(Compa_Ratio * 100, 1) AS compa_ratio_pct,
    Positioning_Status,
    CASE 
        WHEN Compa_Ratio < 0.80 THEN Salary_Range_Minimum - Annualized_Base_Salary
        WHEN Compa_Ratio > 1.20 THEN Annualized_Base_Salary - Salary_Range_Maximum
        ELSE 0 
    END AS variance_to_boundary_gbp,
    CASE 
        WHEN Compa_Ratio < 0.80 THEN 'High Priority: Retention risk / Adjust to band minimum'
        WHEN Compa_Ratio > 1.20 THEN 'Review: Salary capped / Transition merit to lump-sum bonus'
        ELSE 'Normal'
    END AS hr_recommended_action
FROM compensation_data
WHERE Compa_Ratio < 0.80 OR Compa_Ratio > 1.20
ORDER BY Compa_Ratio ASC;
