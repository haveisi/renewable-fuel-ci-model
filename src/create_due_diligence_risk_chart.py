import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model")

risk_path = BASE / "Data-processed" / "due_diligence_flags.csv"
output_dir = BASE / "outputs" / "charts"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "due_diligence_risk_chart.png"

df = pd.read_csv(risk_path)

# Convert risk categories to numeric score for charting
risk_score_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

df["risk_score"] = df["due_diligence_risk"].map(risk_score_map)

fig, ax = plt.subplots(figsize=(11, 7))

ax.bar(df["pathway"], df["risk_score"])

ax.set_ylabel("Due Diligence Risk Score")
ax.set_xlabel("Renewable Fuel Pathway", labelpad=12)

ax.set_title(
    "Due Diligence Risk by Renewable Fuel Pathway",
    fontsize=13,
    pad=18
)

ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Low", "Medium", "High"])

ax.tick_params(axis="x", rotation=25)

fig.text(
    0.5,
    0.035,
    "Risk score reflects screening-level review of CI uncertainty, GREET comparison differences, market exposure, and verification needs.",
    ha="center",
    fontsize=9
)

fig.subplots_adjust(bottom=0.28, top=0.88)

fig.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Saved chart to: {output_path}")