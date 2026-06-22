import pandas as pd
from pathlib import Path

# Input and output paths
input_path = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model\Data-raw\fuel_pathway_inputs.xlsx")

project_root = input_path.parents[1]
output_dir = project_root / "Data-processed"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "ci_results.csv"

# Read Excel
df = pd.read_excel(input_path)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Columns found:")
print(df.columns.tolist())

# Required columns
required_cols = [
    "pathway",
    "fuel_type",
    "feedstock",
    "market",
    "fuel_output_mj",
    "feedstock_emissions",
    "process_energy_emissions",
    "transport_emissions",
    "coproduct_credit",
    "avoided_methane_credit",
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Emission columns
emission_cols = [
    "feedstock_emissions",
    "process_energy_emissions",
    "transport_emissions",
    "coproduct_credit",
    "avoided_methane_credit",
]

# Convert numeric fields
for col in emission_cols + ["fuel_output_mj"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# QA/QC checks
df["qa_status"] = "Pass"

df.loc[df["fuel_output_mj"].isna(), "qa_status"] = "Review - missing fuel output"
df.loc[df["fuel_output_mj"] <= 0, "qa_status"] = "Review - fuel output must be positive"
df.loc[df["market"].isna(), "qa_status"] = "Review - missing market"
df.loc[df["feedstock"].isna(), "qa_status"] = "Review - missing feedstock"

# CI calculation
df["total_lifecycle_emissions_gco2e"] = df[emission_cols].sum(axis=1)
df["ci_gco2e_per_mj"] = df["total_lifecycle_emissions_gco2e"] / df["fuel_output_mj"]

# Risk flag
df["risk_flag"] = "Pass - screening estimate"

df.loc[
    df["ci_gco2e_per_mj"] < 0,
    "risk_flag"
] = "Review - negative CI, verify avoided methane credit"

df.loc[
    (df["avoided_methane_credit"] < 0) & (~df["fuel_type"].str.lower().str.contains("rng", na=False)),
    "risk_flag"
] = "Review - avoided methane credit used for non-RNG pathway"

# Save results
df.to_csv(output_path, index=False)

print("\nCI results:")
print(df[["pathway", "fuel_type", "market", "ci_gco2e_per_mj", "qa_status", "risk_flag"]])

print(f"\nSaved results to: {output_path}")