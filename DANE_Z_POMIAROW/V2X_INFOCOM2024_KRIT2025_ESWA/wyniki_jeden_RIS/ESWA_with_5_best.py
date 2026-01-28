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
TOP_K_1 = 7  # mniejszy set
TOP_K_2 = 10  # większy set

os.makedirs(output_folder, exist_ok=True)


# =========================
# HELPERS
# =========================
def extract_point_number(file_name):
    m = re.search(r"_(\d+)\.csv$", file_name)
    return int(m.group(1)) if m else None


def compute_best_of_topk(data, pattern_mean, top_k, points):
    """Oblicza best-of-TOP-K dla danego K."""
    top_patterns = pattern_mean.head(top_k).index.tolist()
    topk_data = data[data["Pattern"].isin(top_patterns)]
    idx_topk = topk_data.groupby("Point")["Power"].idxmax()
    topk_vals = topk_data.loc[idx_topk]
    power = topk_vals.set_index("Point")["Power"].reindex(points)
    patterns = topk_vals.set_index("Point")["Pattern"].reindex(points)
    return power, patterns, top_patterns


# =========================
# LOAD DATA
# =========================
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
# GLOBAL MAX (27)
# =========================
idx_max = data.groupby("Point")["Power"].idxmax()
max_vals = data.loc[idx_max]

global_max = max_vals.set_index("Point")["Power"].reindex(points)
global_max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)

# =========================
# TOP-K BY AVERAGE (ranking wzorców)
# =========================
pattern_mean = data.groupby("Pattern")["Power"].mean().sort_values(ascending=False)

# --- TOP-K_1 (mniejszy set, np. 5) ---
best_of_topk1, patterns_topk1, top_patterns_1 = compute_best_of_topk(
    data, pattern_mean, TOP_K_1, points
)
print(f"TOP-{TOP_K_1} patterns: {top_patterns_1}")

# --- TOP-K_2 (większy set, np. 15) ---
best_of_topk2, patterns_topk2, top_patterns_2 = compute_best_of_topk(
    data, pattern_mean, TOP_K_2, points
)
print(f"TOP-{TOP_K_2} patterns: {top_patterns_2}")

# =========================
# PLOT
# =========================
plt.figure(figsize=(15, 8))
plt.xticks(points, fontsize=16)
plt.yticks(fontsize=16)

# Global Maximum
plt.plot(
    points,
    global_max,
    "o-",
    color="red",
    linewidth=2.5,
    markersize=7,
    label="Maximum",
)

# Best of TOP-K_2 (większy set)
plt.plot(
    points,
    best_of_topk2,
    "s--",
    color="blue",
    linewidth=2.5,
    markersize=7,
    label=f"Best of TOP-{TOP_K_2}",
)

# Best of TOP-K_1 (mniejszy set)
plt.plot(
    points,
    best_of_topk1,
    "^:",
    color="green",
    linewidth=2.5,
    markersize=7,
    label=f"Best of TOP-{TOP_K_1}",
)

# =========================
# ANNOTACJE (NUMERY WZORCÓW) z clip_on
# =========================
# Pobierz granice Y dla ograniczenia etykiet
y_min = min(global_max.min(), best_of_topk1.min(), best_of_topk2.min())
y_max = max(global_max.max(), best_of_topk1.max(), best_of_topk2.max())
y_margin = (y_max - y_min) * 0.15  # 15% marginesu

ax = plt.gca()

for x in points:
    # MAX (czerwony, nad punktem)
    y_pos_max = global_max.loc[x] + 0.6
    # Ogranicz do górnej granicy
    y_pos_max = min(y_pos_max, y_max + y_margin - 0.3)
    ax.annotate(
        f"{int(global_max_patterns.loc[x])}",
        xy=(x, global_max.loc[x]),
        xytext=(x, y_pos_max),
        color="red",
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="bottom",
        annotation_clip=True,
    )

    # TOP-K_2 (niebieski, lekko poniżej)
    y_pos_k2 = best_of_topk2.loc[x] - 0.4
    y_pos_k2 = max(y_pos_k2, y_min - y_margin + 0.5)
    ax.annotate(
        f"{int(patterns_topk2.loc[x])}",
        xy=(x, best_of_topk2.loc[x]),
        xytext=(x, y_pos_k2),
        color="blue",
        fontsize=10,
        ha="center",
        va="top",
        annotation_clip=True,
    )

    # TOP-K_1 (zielony, jeszcze niżej)
    y_pos_k1 = best_of_topk1.loc[x] - 1.0
    y_pos_k1 = max(y_pos_k1, y_min - y_margin + 0.2)
    ax.annotate(
        f"{int(patterns_topk1.loc[x])}",
        xy=(x, best_of_topk1.loc[x]),
        xytext=(x, y_pos_k1),
        color="green",
        fontsize=10,
        ha="center",
        va="top",
        annotation_clip=True,
    )

# =========================
# STYLING
# =========================
# Ustaw limity Y z marginesem na etykiety
plt.ylim(y_min - y_margin, y_max + y_margin)

plt.xlabel("Measurement Point", fontsize=20)
plt.ylabel("Received Power [dB]", fontsize=20)
plt.title(
    f"Received Power vs Measurement Point",
    fontsize=22,
)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=16, loc="upper left", bbox_to_anchor=(1.02, 1))

plt.subplots_adjust(right=0.82)

out = os.path.join(output_folder, f"Max_vs_{TOP_K_1}_vs_Top_{TOP_K_2}.png")
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.show()

print(f"[OK] Wykres zapisany: {out}")
