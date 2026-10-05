"""
src/generate_data.py
Synthetic Compensation & People Analytics Data Generator
Author: MSc Data Science Graduate / BI Analyst Portfolio
Version: 1.0.0
Description:
    Generates realistic, reproducible employee compensation benchmarking data
    for ~1,250 employees across multiple departments, job levels, and locations.
    Simulates real-world compensation structures (salary bands, compa-ratios,
    market positioning, FTE adjustments, and subtle demographic distributions).
"""

import os
import csv
import math
import random
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURATION & REPRODUCIBILITY
# ==============================================================================
RANDOM_SEED = 42
TOTAL_EMPLOYEES = 1250
EVALUATION_DATE = datetime(2025, 1, 15)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
EMPLOYEE_DATA_PATH = os.path.join(OUTPUT_DIR, "compensation_data.csv")
SALARY_BANDS_PATH = os.path.join(OUTPUT_DIR, "salary_bands.csv")

# ==============================================================================
# MARKET SALARY BANDS BY JOB FAMILY AND LEVEL (Annualized GBP / EUR / USD)
# Structure: Min = Midpoint * 0.80, Max = Midpoint * 1.20 (50% spread = (Max-Min)/Min)
# ==============================================================================
# Levels:
#   L1: Associate / Junior (1-2 yrs)
#   L2: Mid-Level Professional (3-5 yrs)
#   L3: Senior Specialist (5-8 yrs)
#   L4: Lead / Staff / Principal (8-12 yrs)
#   L5: Manager / Director (10+ yrs)

SALARY_STRUCTURE = {
    "Software Engineering": {
        "function": "Technology",
        "department": "Engineering",
        "titles": {
            "L1": "Junior Software Engineer",
            "L2": "Software Engineer",
            "L3": "Senior Software Engineer",
            "L4": "Staff Software Engineer",
            "L5": "Engineering Manager"
        },
        "midpoints": {"L1": 42000, "L2": 62000, "L3": 85000, "L4": 112000, "L5": 135000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.15, "L5": 0.20}
    },
    "Data & Analytics": {
        "function": "Technology",
        "department": "Engineering",
        "titles": {
            "L1": "Junior Data Analyst",
            "L2": "BI / Data Analyst",
            "L3": "Senior Data Scientist / BI Engineer",
            "L4": "Lead Analytics Specialist",
            "L5": "Data & Analytics Manager"
        },
        "midpoints": {"L1": 38000, "L2": 56000, "L3": 78000, "L4": 102000, "L5": 125000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.15, "L5": 0.20}
    },
    "Product Management": {
        "function": "Product",
        "department": "Product",
        "titles": {
            "L1": "Associate Product Manager",
            "L2": "Product Manager",
            "L3": "Senior Product Manager",
            "L4": "Principal Product Manager",
            "L5": "Director of Product"
        },
        "midpoints": {"L1": 40000, "L2": 60000, "L3": 82000, "L4": 108000, "L5": 132000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.15, "L5": 0.20}
    },
    "Enterprise Sales": {
        "function": "Commercial",
        "department": "Sales",
        "titles": {
            "L1": "Sales Development Rep (SDR)",
            "L2": "Account Executive",
            "L3": "Senior Enterprise AE",
            "L4": "Strategic Sales Lead",
            "L5": "Sales Director"
        },
        "midpoints": {"L1": 36000, "L2": 54000, "L3": 76000, "L4": 98000, "L5": 122000},
        "target_bonus_pct": {"L1": 0.20, "L2": 0.35, "L3": 0.40, "L4": 0.45, "L5": 0.50}
    },
    "Customer Success": {
        "function": "Commercial",
        "department": "Customer Success",
        "titles": {
            "L1": "Customer Support Specialist",
            "L2": "Customer Success Manager",
            "L3": "Senior CSM",
            "L4": "Principal CSM",
            "L5": "Head of Customer Success"
        },
        "midpoints": {"L1": 32000, "L2": 46000, "L3": 64000, "L4": 82000, "L5": 105000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.12, "L5": 0.18}
    },
    "Marketing & Growth": {
        "function": "Commercial",
        "department": "Marketing",
        "titles": {
            "L1": "Marketing Coordinator",
            "L2": "Growth Marketing Specialist",
            "L3": "Senior Brand & Performance Manager",
            "L4": "Principal Campaign Strategist",
            "L5": "Marketing Director"
        },
        "midpoints": {"L1": 33000, "L2": 48000, "L3": 68000, "L4": 88000, "L5": 112000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.12, "L5": 0.18}
    },
    "People & Culture": {
        "function": "Corporate",
        "department": "Human Resources",
        "titles": {
            "L1": "HR Coordinator",
            "L2": "People Experience Specialist",
            "L3": "Senior HR Business Partner",
            "L4": "Lead People Operations Partner",
            "L5": "Head of People & Culture"
        },
        "midpoints": {"L1": 31000, "L2": 45000, "L3": 62000, "L4": 80000, "L5": 104000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.07, "L3": 0.10, "L4": 0.12, "L5": 0.15}
    },
    "Finance & Accounting": {
        "function": "Corporate",
        "department": "Finance",
        "titles": {
            "L1": "Accounts Assistant",
            "L2": "Financial Analyst / Accountant",
            "L3": "Senior FP&A Analyst",
            "L4": "Lead Financial Controller",
            "L5": "Finance Director"
        },
        "midpoints": {"L1": 34000, "L2": 50000, "L3": 72000, "L4": 94000, "L5": 118000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.15, "L5": 0.20}
    },
    "Business Operations": {
        "function": "Operations",
        "department": "Operations",
        "titles": {
            "L1": "Operations Associate",
            "L2": "Operations Specialist",
            "L3": "Senior Operations Manager",
            "L4": "Lead Systems & Process Architect",
            "L5": "Director of Operations"
        },
        "midpoints": {"L1": 30000, "L2": 44000, "L3": 62000, "L4": 80000, "L5": 102000},
        "target_bonus_pct": {"L1": 0.05, "L2": 0.07, "L3": 0.10, "L4": 0.12, "L5": 0.15}
    }
}

# ==============================================================================
# DEMOGRAPHIC AND WORKFORCE WEIGHTS
# ==============================================================================
# Job family employee distribution weight (proportions across company)
JOB_FAMILY_WEIGHTS = {
    "Software Engineering": 0.26,
    "Data & Analytics": 0.12,
    "Product Management": 0.08,
    "Enterprise Sales": 0.16,
    "Customer Success": 0.12,
    "Marketing & Growth": 0.09,
    "People & Culture": 0.05,
    "Finance & Accounting": 0.06,
    "Business Operations": 0.06
}

# Level distribution (Pyramid shape: more juniors and mids, fewer directors)
LEVEL_WEIGHTS = {
    "L1": 0.20,
    "L2": 0.38,
    "L3": 0.26,
    "L4": 0.11,
    "L5": 0.05
}

# Office Locations with Cost of Labor / Market Adjustment Index
LOCATIONS = [
    {"name": "London (HQ)", "weight": 0.44, "geo_factor": 1.10},
    {"name": "Manchester", "weight": 0.20, "geo_factor": 0.95},
    {"name": "Edinburgh", "weight": 0.14, "geo_factor": 0.95},
    {"name": "Bristol", "weight": 0.10, "geo_factor": 0.96},
    {"name": "Remote (UK)", "weight": 0.12, "geo_factor": 1.00}
]

# Gender probability distribution by Job Family (reflects industry pipeline realities)
# Not cartoonish; represents real-world STEM / Sales / HR talent pools
GENDER_RATIOS = {
    "Software Engineering": {"Male": 0.70, "Female": 0.28, "Non-Binary": 0.02},
    "Data & Analytics": {"Male": 0.60, "Female": 0.38, "Non-Binary": 0.02},
    "Product Management": {"Male": 0.54, "Female": 0.44, "Non-Binary": 0.02},
    "Enterprise Sales": {"Male": 0.58, "Female": 0.40, "Non-Binary": 0.02},
    "Customer Success": {"Male": 0.42, "Female": 0.56, "Non-Binary": 0.02},
    "Marketing & Growth": {"Male": 0.38, "Female": 0.60, "Non-Binary": 0.02},
    "People & Culture": {"Male": 0.24, "Female": 0.74, "Non-Binary": 0.02},
    "Finance & Accounting": {"Male": 0.48, "Female": 0.50, "Non-Binary": 0.02},
    "Business Operations": {"Male": 0.46, "Female": 0.52, "Non-Binary": 0.02}
}

FIRST_NAMES = {
    "Male": ["James", "Oliver", "Harry", "Jack", "George", "Noah", "Charlie", "Jacob", "Alfie", "Freddie",
             "William", "Thomas", "Oscar", "Alexander", "Daniel", "Matthew", "Lucas", "Henry", "Samuel", "David"],
    "Female": ["Olivia", "Amelia", "Isla", "Ava", "Emily", "Sophia", "Grace", "Mia", "Poppy", "Ella",
               "Charlotte", "Lily", "Chloe", "Alice", "Hannah", "Zoe", "Eleanor", "Jessica", "Maya", "Sophie"],
    "Non-Binary": ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Robin", "Rowan", "Riley", "Casey", "Cameron"]
}

LAST_NAMES = [
    "Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies", "Robinson", "Wright",
    "Thompson", "Evans", "Walker", "White", "Roberts", "Green", "Hall", "Thomas", "Clarke", "Patel",
    "Jackson", "Wood", "Turner", "Martin", "Cooper", "Hill", "Ward", "Morris", "Moore", "Clark"
]


def weighted_choice(choices_dict, rng):
    """Selects an item based on weights."""
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    total = sum(weights)
    r = rng.uniform(0, total)
    upto = 0
    for item, w in zip(items, weights):
        if upto + w >= r:
            return item
        upto += w
    return items[-1]


def build_salary_bands_table():
    """Generates the salary bands reference dimension table."""
    bands = []
    for family, info in SALARY_STRUCTURE.items():
        for level, mid in info["midpoints"].items():
            # Standard HR range spread: Min = Mid * 0.80, Max = Mid * 1.20
            r_min = round(mid * 0.80)
            r_max = round(mid * 1.20)
            spread_pct = round(((r_max - r_min) / r_min) * 100, 1)
            bands.append({
                "Band_ID": f"BAND-{family[:3].upper()}-{level}",
                "Job_Family": family,
                "Job_Level": level,
                "Range_Minimum": r_min,
                "Range_Midpoint": mid,
                "Range_Maximum": r_max,
                "Range_Spread_Pct": spread_pct,
                "Currency": "GBP"
            })
    return bands


def generate_workforce(n=TOTAL_EMPLOYEES, seed=RANDOM_SEED):
    """
    Generates employee records with mathematically realistic compensation parameters.
    """
    rng = random.Random(seed)
    employees = []

    for i in range(1, n + 1):
        emp_id = f"EMP-{1000 + i}"
        
        # 1. Select Job Family, Function & Department
        family = weighted_choice(JOB_FAMILY_WEIGHTS, rng)
        fam_info = SALARY_STRUCTURE[family]
        department = fam_info["department"]
        business_function = fam_info["function"]

        # 2. Select Level
        level = weighted_choice(LEVEL_WEIGHTS, rng)
        job_title = fam_info["titles"][level]

        # 3. Select Location
        loc_choice = rng.choices(LOCATIONS, weights=[loc["weight"] for loc in LOCATIONS])[0]
        location = loc_choice["name"]
        geo_factor = loc_choice["geo_factor"]

        # 4. Gender (derived with realistic representation)
        gender_weights = GENDER_RATIOS[family]
        gender = weighted_choice(gender_weights, rng)

        # Name generation
        fname = rng.choice(FIRST_NAMES[gender])
        lname = rng.choice(LAST_NAMES)
        full_name = f"{fname} {lname}"

        # 5. Tenure and Hire Date
        # L1s are newer, L4/L5 have longer tenure on average
        level_tenure_mu = {"L1": 1.1, "L2": 2.8, "L3": 4.5, "L4": 6.2, "L5": 7.5}
        tenure_mu = level_tenure_mu[level]
        tenure_years = max(0.2, round(rng.gauss(tenure_mu, 1.2), 1))
        hire_date = EVALUATION_DATE - timedelta(days=int(tenure_years * 365.25))

        # 6. Performance Rating (1 to 5 scale, 3 is Meets Expectations)
        # Normal distribution centered around 3.3
        perf_score = min(5, max(1, round(rng.gauss(3.35, 0.75))))

        # 7. Employment Type and FTE
        # Majority 1.0 (Full-time), ~7% Part-time (0.6, 0.7, 0.8)
        is_part_time = (rng.random() < 0.075)
        if is_part_time:
            employment_type = "Part-Time"
            fte = rng.choice([0.5, 0.6, 0.8])
        else:
            employment_type = "Full-Time"
            fte = 1.0

        # 8. Salary Band Parameters for this role
        midpoint = fam_info["midpoints"][level]
        range_min = round(midpoint * 0.80)
        range_max = round(midpoint * 1.20)

        # 9. Compa-Ratio Modeling
        # Compa-Ratio = Base Salary / Range Midpoint
        # Healthy organizations center around 1.00 (100%), with SD ~ 0.09.
        # Tenure and Performance push compa-ratio slightly up.
        tenure_boost = min(0.08, (tenure_years / 10.0) * 0.08)
        perf_boost = (perf_score - 3.0) * 0.025
        
        # Base individual compa-ratio target
        base_cr = rng.gauss(0.98, 0.075) + tenure_boost + perf_boost

        # Add controlled realistic outliers:
        # ~5% below range (e.g., promoted quickly or newly hired without adjustment)
        # ~4% above range (e.g., red-circled, retained high performer or market legacy)
        rand_outlier = rng.random()
        if rand_outlier < 0.045:
            # Below band (0.72 - 0.79 CR)
            target_cr = rng.uniform(0.72, 0.79)
        elif rand_outlier > 0.965:
            # Above band (1.21 - 1.28 CR)
            target_cr = rng.uniform(1.21, 1.28)
        else:
            target_cr = base_cr

        # Apply geo factor slightly (adjusts salary expectation by location)
        # In modern comp policies, ranges are national or geo-factored:
        annualized_base_salary = round((midpoint * target_cr * (0.95 + 0.05 * geo_factor)) / 500) * 500
        
        # Recalculate true actual compa-ratio against the standard national benchmark midpoint
        actual_cr = round(annualized_base_salary / midpoint, 4)

        # Actual Paid Base Salary (accounting for Part-Time FTE)
        actual_paid_salary = round(annualized_base_salary * fte)

        # Salary Positioning Category
        if annualized_base_salary < range_min:
            positioning = "Below Range (<80%)"
        elif annualized_base_salary > range_max:
            positioning = "Above Range (>120%)"
        elif annualized_base_salary < midpoint:
            positioning = "Lower Half (80-100%)"
        else:
            positioning = "Upper Half (100-120%)"

        # 10. Bonus Calculation
        target_bonus_rate = fam_info["target_bonus_pct"][level]
        # Actual bonus payout depends on company factor & performance score
        perf_multiplier = {1: 0.0, 2: 0.6, 3: 1.0, 4: 1.25, 5: 1.5}[perf_score]
        actual_bonus = round(annualized_base_salary * target_bonus_rate * perf_multiplier * fte)
        total_compensation = actual_paid_salary + actual_bonus

        employees.append({
            "Employee_ID": emp_id,
            "Full_Name": full_name,
            "Gender": gender,
            "Department": department,
            "Business_Function": business_function,
            "Job_Family": family,
            "Job_Title": job_title,
            "Job_Level": level,
            "Location": location,
            "Employment_Type": employment_type,
            "FTE": fte,
            "Hire_Date": hire_date.strftime("%Y-%m-%d"),
            "Tenure_Years": tenure_years,
            "Performance_Rating": perf_score,
            "Annualized_Base_Salary": annualized_base_salary,
            "Actual_Paid_Base_Salary": actual_paid_salary,
            "Salary_Range_Minimum": range_min,
            "Salary_Range_Midpoint": midpoint,
            "Salary_Range_Maximum": range_max,
            "Compa_Ratio": actual_cr,
            "Compa_Ratio_Pct": round(actual_cr * 100, 1),
            "Positioning_Status": positioning,
            "Target_Bonus_Pct": round(target_bonus_rate * 100, 1),
            "Actual_Bonus_Paid": actual_bonus,
            "Total_Direct_Compensation": total_compensation,
            "Currency": "GBP"
        })

    return employees


def save_to_csv(data, filepath):
    """Helper to write list of dicts to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not data:
        return
    keys = data[0].keys()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def compute_summary_statistics(employees):
    """
    Computes quick analytical sanity check on the generated workforce.
    Prints distributions that validate business realism.
    """
    n = len(employees)
    salaries = [e["Annualized_Base_Salary"] for e in employees]
    salaries.sort()
    
    median_sal = salaries[n // 2] if n % 2 != 0 else (salaries[n // 2 - 1] + salaries[n // 2]) / 2
    mean_sal = sum(salaries) / n

    cr_values = [e["Compa_Ratio"] for e in employees]
    mean_cr = sum(cr_values) / n
    cr_values.sort()
    median_cr = cr_values[n // 2]

    below_cnt = sum(1 for e in employees if e["Positioning_Status"] == "Below Range (<80%)")
    above_cnt = sum(1 for e in employees if e["Positioning_Status"] == "Above Range (>120%)")
    
    # Gender split
    male_emps = [e for e in employees if e["Gender"] == "Male"]
    fem_emps = [e for e in employees if e["Gender"] == "Female"]
    nb_emps = [e for e in employees if e["Gender"] == "Non-Binary"]

    male_salaries = sorted([e["Annualized_Base_Salary"] for e in male_emps])
    fem_salaries = sorted([e["Annualized_Base_Salary"] for e in fem_emps])

    male_med = male_salaries[len(male_salaries) // 2]
    fem_med = fem_salaries[len(fem_salaries) // 2]
    
    raw_gap = ((male_med - fem_med) / male_med) * 100

    # Within-level median gap for L2 (illustrates like-for-like vs raw)
    l2_male = sorted([e["Annualized_Base_Salary"] for e in male_emps if e["Job_Level"] == "L2"])
    l2_fem = sorted([e["Annualized_Base_Salary"] for e in fem_emps if e["Job_Level"] == "L2"])
    l2_m_med = l2_male[len(l2_male) // 2] if l2_male else 0
    l2_f_med = l2_fem[len(l2_fem) // 2] if l2_fem else 0
    l2_gap = ((l2_m_med - l2_f_med) / l2_m_med) * 100 if l2_m_med else 0

    return {
        "Total Headcount": n,
        "Total FTE": round(sum(e["FTE"] for e in employees), 1),
        "Mean Annualized Salary": f"£{mean_sal:,.0f}",
        "Median Annualized Salary": f"£{median_sal:,.0f}",
        "Mean Compa-Ratio": f"{mean_cr:.2%}",
        "Median Compa-Ratio": f"{median_cr:.2%}",
        "Below Range Count (%)": f"{below_cnt} ({below_cnt / n:.1%})",
        "Above Range Count (%)": f"{above_cnt} ({above_cnt / n:.1%})",
        "Gender Representation": f"Male: {len(male_emps)} ({len(male_emps)/n:.1%}) | Female: {len(fem_emps)} ({len(fem_emps)/n:.1%}) | NB: {len(nb_emps)} ({len(nb_emps)/n:.1%})",
        "Raw Median Salary (Male)": f"£{male_med:,.0f}",
        "Raw Median Salary (Female)": f"£{fem_med:,.0f}",
        "Raw Company-Wide Gender Pay Gap": f"{raw_gap:.1f}%",
        "Within-Level (L2) Like-for-Like Gap": f"{l2_gap:.1f}%"
    }


def main():
    print(f"=== Synthetic Compensation Data Generator ===")
    print(f"Random Seed: {RANDOM_SEED}")
    print(f"Target Headcount: {TOTAL_EMPLOYEES}")
    print("Generating market salary bands...")
    bands = build_salary_bands_table()
    save_to_csv(bands, SALARY_BANDS_PATH)
    print(f"-> Saved {len(bands)} salary band benchmarks to: {SALARY_BANDS_PATH}")

    print("Generating workforce compensation records...")
    employees = generate_workforce(TOTAL_EMPLOYEES, RANDOM_SEED)
    save_to_csv(employees, EMPLOYEE_DATA_PATH)
    print(f"-> Saved {len(employees)} employee records to: {EMPLOYEE_DATA_PATH}")

    print("\n--- SANITY CHECK & COMPENSATION BENCHMARK AUDIT ---")
    stats = compute_summary_statistics(employees)
    for k, v in stats.items():
        print(f"  {k:36}: {v}")
    print("\nGeneration completed successfully.")


if __name__ == "__main__":
    main()