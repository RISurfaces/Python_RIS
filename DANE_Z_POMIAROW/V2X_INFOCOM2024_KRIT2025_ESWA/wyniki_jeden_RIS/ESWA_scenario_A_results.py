import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# =========================
# CONFIG
# =========================
input_folder = "jeden_ris_wyniki"
output_folder = "jeden_ris_wyniki"

PATTERN_10 = 10
PATTERN_20 = 20

os.makedirs(output_folder, exist_ok=True)


# =========================
# HELPERS
# =========================
def extract_point_number(file_name):
    match = re.search(r"_(\d+)\.csv$", file_name)
    return int(match.group(1)) if match else None


def label_offset_max(y_prev, y_curr, y_next, offset=0.8):
    if y_prev is not None and y_next is not None:
        if y_curr > y_prev and y_curr > y_next:
            return offset, "bottom"
    if y_prev is not None and y_curr < y_prev:
        return offset, "bottom"
    return -offset, "top"


def label_offset_min(y_prev, y_curr, y_next, offset=0.8):
    if y_prev is not None and y_next is not None:
        if y_curr < y_prev and y_curr < y_next:
            return -offset, "top"
    if y_prev is not None and y_curr < y_prev:
        return -offset, "top"
    return offset, "bottom"


# =========================
# LOAD DATA
# =========================
def load_all_points(input_folder):
    rows = []

    for file_name in sorted(os.listdir(input_folder)):
        if not file_name.endswith(".csv"):
            continue

        point = extract_point_number(file_name)
        if point is None:
            continue

        file_path = os.path.join(input_folder, file_name)

        df = pd.read_csv(
            file_path,
            sep=";",
            header=None,
            names=["Pattern", "Timestamp", "Frequency", "Power"],
        )

        df["Point"] = point
        rows.append(df)

    return pd.concat(rows, ignore_index=True)


# =========================
# PLOT
# =========================
def generate_plot(data, output_folder):

    points = sorted(data["Point"].unique())

    max_vals = data.loc[data.groupby("Point")["Power"].idxmax()]
    min_vals = data.loc[data.groupby("Point")["Power"].idxmin()]

    maximum = max_vals.set_index("Point")["Power"].reindex(points)
    minimum = min_vals.set_index("Point")["Power"].reindex(points)

    max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)
    min_patterns = min_vals.set_index("Point")["Pattern"].reindex(points)

    p10 = (
        data[data["Pattern"] == PATTERN_10].set_index("Point")["Power"].reindex(points)
    )
    p20 = (
        data[data["Pattern"] == PATTERN_20].set_index("Point")["Power"].reindex(points)
    )

    plt.figure(figsize=(14, 7))
    plt.xticks(points, fontsize=12)
    plt.yticks(fontsize=12)

    plt.plot(points, maximum, "o-", color="red", label="Maximum", linewidth=2)
    plt.plot(points, minimum, "o-", color="blue", label="Minimum", linewidth=2)
    plt.plot(points, p10, "o--", color="green", label="Pattern 10", linewidth=2)
    plt.plot(points, p20, "o--", color="black", label="Pattern 20", linewidth=2)

    for i, x in enumerate(points):

        # ===== MAXIMUM =====
        y = maximum.loc[x]
        pat = int(max_patterns.loc[x])

        y_prev = maximum.loc[points[i - 1]] if i > 0 else None
        y_next = maximum.loc[points[i + 1]] if i < len(points) - 1 else None

        dy, va = label_offset_max(y_prev, y, y_next)

        plt.text(x, y + dy, f"{pat}", color="red", fontsize=10, ha="center", va=va)

        # ===== MINIMUM =====
        y = minimum.loc[x]
        pat = int(min_patterns.loc[x])

        # 🔧 PROSTE, JASNE PRZESUNIĘCIA
        if x == 4:
            dy, va = -1.2, "top"
        elif x == 10:
            dy, va = -2.0, "top"
        elif x == 14:
            dy, va = 1.2, "bottom"
        else:
            y_prev = minimum.loc[points[i - 1]] if i > 0 else None
            y_next = minimum.loc[points[i + 1]] if i < len(points) - 1 else None
            dy, va = label_offset_min(y_prev, y, y_next)

        plt.text(x, y + dy, f"{pat}", color="blue", fontsize=10, ha="center", va=va)

    plt.xlabel("Measurement Point", fontsize=16)
    plt.ylabel("Received Power [dB]", fontsize=16)
    plt.title("Received Power vs Measurement Point", fontsize=18)

    plt.grid(True, linestyle="--", alpha=0.6)

    plt.legend(fontsize=13, loc="upper left", bbox_to_anchor=(1.02, 1))

    plt.tight_layout()

    out = os.path.join(
        output_folder, "Power_vs_Point_Max_Min_Pattern10_20_Annotated.png"
    )
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"[OK] Wykres zapisany: {out}")


# =========================
# MAIN
# =========================
data = load_all_points(input_folder)

data = data[data["Point"].between(4, 22)]
mapping = {old: new for new, old in enumerate(sorted(data["Point"].unique()), start=1)}
data["Point"] = data["Point"].map(mapping)

generate_plot(data, output_folder)
print("Zakończono.")
