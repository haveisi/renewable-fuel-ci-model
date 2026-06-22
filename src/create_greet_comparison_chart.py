import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"C:\Users\hveis\OneDrive\Hadi_Work\LCA\stx_renewable_fuel_ci_model")

comparison_path = BASE / "GREET" / "comparison" / "python_vs_greet_comparison.csv"
output_dir = BASE / "outputs" / "charts"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "python_vs_greet_ci_comparison.png"

df = pd.read_csv(comparison_path)

fig, ax = plt.subplots(figsize=(11, 7))

x = range(len(df))
width = 0.35

ax.bar(
    [i - width / 2 for i in x],
    df["python_screening_ci_gco2e_per_mj"],
    width,
    label="Python screening CI"
)

ax.bar(
    [i + width / 2 for i in x],
    df["greet_ci_gco2e_per_mj"],
    width,
    label="GREET-style CI"
)

ax.axhline(0, linewidth=1)

ax.set_ylabel("Carbon Intensity (gCO2e/MJ)")
ax.set_xlabel("Renewable Fuel Pathway", labelpad=12)

ax.set_title(
    "Python Screening CI vs GREET-Style CI by Fuel Pathway",
    fontsize=13,
    pad=18
)

ax.set_xticks(list(x))
ax.set_xticklabels(df["pathway"], rotation=25, ha="right")

ax.legend()

fig.text(
    0.5,
    0.035,
    "Synthetic portfolio values; GREET-style values are manually entered placeholders for comparison workflow demonstration.",
    ha="center",
    fontsize=9
)

fig.subplots_adjust(bottom=0.28, top=0.88)

fig.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Saved chart to: {output_path}")