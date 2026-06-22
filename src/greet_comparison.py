import pandas as pd
from pathlib import Path

BASE = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model")

python_results_path = BASE / "Data-processed" / "ci_results.csv"
greet_results_path = BASE / "GREET" / "exports" / "greet_results_manual.xlsx"

output_dir = BASE / "GREET" / "comparison"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "python_vs_greet_comparison.csv"

# Read files
python_df = pd.read_csv(python_results_path)
greet_df = pd.read_excel(greet_results_path)

# Clean columns
python_df.columns = python_df.columns.str.strip().str.lower()
greet_df.columns = greet_df.columns.str.strip().str.lower()

# Keep only needed Python result columns
python_small = python_df[
    [
        "pathway",
        "fuel_type",
        "market",
        "ci_gco2e_per_mj",
        "risk_flag",
    ]
].copy()

python_small = python_small.rename(
    columns={"ci_gco2e_per_mj": "python_screening_ci_gco2e_per_mj"}
)

# Merge
comparison = python_small.merge(greet_df, on="pathway", how="left")

# Difference
comparison["ci_difference_python_minus_greet"] = (
    comparison["python_screening_ci_gco2e_per_mj"]
    - comparison["greet_ci_gco2e_per_mj"]
)

comparison["difference_percent"] = (
    comparison["ci_difference_python_minus_greet"]
    / comparison["greet_ci_gco2e_per_mj"].abs()
    * 100
)

# Interpretation
def interpret(row):
    if pd.isna(row["greet_ci_gco2e_per_mj"]):
        return "No GREET result available yet."
    diff = abs(row["difference_percent"])
    if diff <= 10:
        return "Close match for screening model."
    elif diff <= 25:
        return "Moderate difference; review allocation, energy, transport, and coproduct assumptions."
    else:
        return "Large difference; screening model assumptions need review before using for decision support."

comparison["interpretation"] = comparison.apply(interpret, axis=1)

comparison.to_csv(output_path, index=False)

print("\nPython vs GREET comparison:")
print(
    comparison[
        [
            "pathway",
            "python_screening_ci_gco2e_per_mj",
            "greet_ci_gco2e_per_mj",
            "ci_difference_python_minus_greet",
            "difference_percent",
            "interpretation",
        ]
    ]
)

print(f"\nSaved comparison to: {output_path}")