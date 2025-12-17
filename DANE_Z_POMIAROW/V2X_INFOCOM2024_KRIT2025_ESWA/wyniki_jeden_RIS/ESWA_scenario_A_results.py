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

    # --- MAXIMUM ---
    maximum = data.groupby("Point")["Power"].max().reindex(points)

    # --- MINIMUM ---
    minimum = data.groupby("Point")["Power"].min().reindex(points)

    # --- PATTERN 10 ---
    p10 = (
        data[data["Pattern"] == PATTERN_10].set_index("Point")["Power"].reindex(points)
    )

    # --- PATTERN 20 ---
    p20 = (
        data[data["Pattern"] == PATTERN_20].set_index("Point")["Power"].reindex(points)
    )

    # =========================
    # PLOT
    # =========================
    plt.figure(figsize=(14, 7))
    plt.xticks(points)
    plt.plot(points, maximum, "o-", color="red", label="Maximum", linewidth=2)
    plt.plot(points, minimum, "o-", color="blue", label="Minimum", linewidth=2)
    plt.plot(points, p10, "o--", color="green", label="Pattern 10", linewidth=2)
    plt.plot(points, p20, "o--", color="black", label="Pattern 20", linewidth=2)
    plt.xlabel("Measurement Point")
    plt.ylabel("Received Power [dB]")
    plt.title("Received Power vs Measurement Point")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    out = os.path.join(output_folder, "Power_vs_Point_Max_Min_Pattern10_20.png")
    plt.savefig(out, dpi=300)
    plt.show()

    print(f"[OK] Wykres zapisany: {out}")


# =========================
# MAIN
# =========================
data = load_all_points(input_folder)
data = data[data["Point"].between(1, 22)]
generate_plot(data, output_folder)

print("Zakończono.")
