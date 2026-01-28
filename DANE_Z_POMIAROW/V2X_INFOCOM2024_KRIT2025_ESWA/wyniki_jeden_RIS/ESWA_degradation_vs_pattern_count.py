import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# =========================
# CONFIG
# =========================
input_folder = "jeden_ris_wyniki"
output_folder = "jeden_ris_wyniki"

POINT_MIN = 4
POINT_MAX = 22

os.makedirs(output_folder, exist_ok=True)


# =========================
# HELPERS
# =========================
def extract_point_number(file_name):
    m = re.search(r"_(\d+)\.csv$", file_name)
    return int(m.group(1)) if m else None


def load_all_points(folder):
    rows = []
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".csv"):
            continue

        pt = extract_point_number(f)
        if pt is None:
            continue

        df = pd.read_csv(
            os.path.join(folder, f),
            sep=";",
            header=None,
            names=["Pattern", "Timestamp", "Frequency", "Power"],
        )
        df["Point"] = pt
        rows.append(df)

    return pd.concat(rows, ignore_index=True)


# =========================
# MAIN
# =========================
data = load_all_points(input_folder)

# --- punkty 4–22 ---
data = data[data["Point"].between(POINT_MIN, POINT_MAX)]

# --- przenumerowanie 4–22 → 1–19 ---
old_points = sorted(data["Point"].unique())
point_map = {old: new for new, old in enumerate(old_points, start=1)}
data["Point"] = data["Point"].map(point_map)

points = sorted(data["Point"].unique())

# =========================
# GLOBAL MAX (baseline - wszystkie wzorce)
# =========================
idx_max = data.groupby("Point")["Power"].idxmax()
max_vals = data.loc[idx_max]
global_max = max_vals.set_index("Point")["Power"].reindex(points)

# Średnia mocy dla globalnego maksimum (baseline)
baseline_mean = global_max.mean()
print(f"Baseline (all patterns): {baseline_mean:.2f} dB")

# =========================
# RANKING WZORCÓW WG ŚREDNIEJ
# =========================
pattern_mean = data.groupby("Pattern")["Power"].mean().sort_values(ascending=False)
all_patterns = pattern_mean.index.tolist()
total_patterns = len(all_patterns)

print(f"Total patterns: {total_patterns}")
print(f"Pattern ranking (by avg): {all_patterns}")

# =========================
# OBLICZ DEGRADACJĘ DLA RÓŻNYCH K
# =========================
k_values = list(range(1, total_patterns + 1))
degradations = []

for k in k_values:
    # Wybierz TOP-K wzorców
    top_patterns = pattern_mean.head(k).index.tolist()

    # Filtruj dane tylko do tych wzorców
    topk_data = data[data["Pattern"].isin(top_patterns)]

    # Dla każdego punktu wybierz najlepszy z TOP-K
    idx_topk = topk_data.groupby("Point")["Power"].idxmax()
    topk_vals = topk_data.loc[idx_topk]
    best_of_topk = topk_vals.set_index("Point")["Power"].reindex(points)

    # Oblicz degradację względem global max (per punkt)
    diff = best_of_topk - global_max
    mean_degradation = diff.mean()

    degradations.append(mean_degradation)

    if k in [1, 3, 5, 7, 10, 15, 20, total_patterns]:
        print(f"K={k:2d}: mean degradation = {mean_degradation:.3f} dB")

# =========================
# PLOT (styl jak na obrazku)
# =========================
plt.figure(figsize=(12, 8))

plt.plot(
    k_values,
    degradations,
    "o--",
    color="steelblue",
    linewidth=2.5,
    markersize=8,
    markerfacecolor="white",
    markeredgecolor="steelblue",
    markeredgewidth=2,
)

# Oś X odwrócona (od max do 0)
plt.xlim(total_patterns + 1, 0)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Etykiety
plt.xlabel("Pattern count", fontsize=20)
plt.ylabel("Degradation [dB]", fontsize=20)
plt.title("Degradation vs. pattern count", fontsize=22)

plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# Zapis
out = os.path.join(output_folder, "Degradation_vs_pattern_count.png")
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.show()

print(f"\n[OK] Wykres zapisany: {out}")
