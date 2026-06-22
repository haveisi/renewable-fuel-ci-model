import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model")

results_path = BASE / "Data-processed" / "ci_results.csv"
output_dir = BASE / "outputs" / "charts"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "ci_comparison_chart.png"

df = pd.read_csv(results_path)

fig, ax = plt.subplots(figsize=(11, 7))

ax.bar(df["pathway"], df["ci_gco2e_per_mj"])
ax.axhline(0, linewidth=1)

ax.set_ylabel("Carbon Intensity (gCO2e/MJ)")
ax.set_xlabel("Renewable Fuel Pathway", labelpad=12)

ax.set_title(
    "Screening-Level Renewable Fuel Carbon Intensity by Pathway",
    fontsize=13,
    pad=18
)

ax.tick_params(axis="x", rotation=25)

# Disclaimer note, placed safely inside the figure
fig.text(
    0.5,
    0.035,
    "Synthetic portfolio values; not verified LCFS, CFR, RED, ISCC, or official GREET results.",
    ha="center",
    fontsize=9
)

# Make room at bottom for disclaimer
fig.subplots_adjust(bottom=0.28, top=0.88)

fig.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Saved chart to: {output_path}")