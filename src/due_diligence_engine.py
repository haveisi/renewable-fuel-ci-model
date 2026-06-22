import pandas as pd
from pathlib import Path

BASE = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model")

comparison_path = BASE / "GREET" / "comparison" / "python_vs_greet_comparison.csv"
output_dir = BASE / "Data-processed"
output_path = output_dir / "due_diligence_flags.csv"

df = pd.read_csv(comparison_path)

def risk_level(row):
    risk = 0

    # Negative CI needs verification because avoided emissions are high value but high scrutiny
    if row["python_screening_ci_gco2e_per_mj"] < 0:
        risk += 3

    # Large model difference creates methodology risk
    if abs(row["difference_percent"]) > 25:
        risk += 3
    elif abs(row["difference_percent"]) > 10:
        risk += 2
    else:
        risk += 1

    # Market-specific risk
    market = str(row["market"]).upper()
    if "RED" in market:
        risk += 2
    if "CFR" in market:
        risk += 1
    if "LCFS" in market:
        risk += 1

    if risk >= 6:
        return "High"
    elif risk >= 4:
        return "Medium"
    else:
        return "Low"
    fuel_type = str(row["fuel_type"]).upper()
    if "RNG" in fuel_type:
        risk += 1

def recommendation(row):
    pathway = row["pathway"]

    if row["python_screening_ci_gco2e_per_mj"] < 0:
        return "Verify avoided methane assumptions, project boundary, methane capture data, and pathway eligibility before commercial use."

    if abs(row["difference_percent"]) > 10:
        return "Review GREET assumptions, allocation method, energy inputs, transport distance, and feedstock treatment."

    return "Screening estimate is directionally consistent; proceed to deeper pathway documentation and verification review."

df["due_diligence_risk"] = df.apply(risk_level, axis=1)
df["commercial_recommendation"] = df.apply(recommendation, axis=1)

df.to_csv(output_path, index=False)

print("\nDue diligence flags:")
print(df[["pathway", "market", "due_diligence_risk", "commercial_recommendation"]])

print(f"\nSaved due diligence output to: {output_path}")