import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# =========================
# CONFIG
# =========================
input_folder = "jeden_ris_wyniki"
output_folder = "jeden_ris_wyniki"

SELECTED_PATTERNS = [5, 10]  # <<< JEDYNE MIEJSCE ZMIANY

os.makedirs(output_folder, exist_ok=True)


# =========================
# HELPERS
# =========================
def extract_point_number(file_name):
    m = re.search(r"_(\d+)\.csv$", file_name)
    return int(m.group(1)) if m else None


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
# PLOT
# =========================
def generate_plot(data):

    points = sorted(data["Point"].unique())

    # ---- MAX / MIN ----
    max_vals = data.loc[data.groupby("Point")["Power"].idxmax()]
    min_vals = data.loc[data.groupby("Point")["Power"].idxmin()]

    maximum = max_vals.set_index("Point")["Power"].reindex(points)
    minimum = min_vals.set_index("Point")["Power"].reindex(points)

    max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)
    min_patterns = min_vals.set_index("Point")["Pattern"].reindex(points)

    # ---- SELECTED PATTERNS ----
    pattern_curves = {}
    for pat in SELECTED_PATTERNS:
        pattern_curves[pat] = (
            data[data["Pattern"] == pat].set_index("Point")["Power"].reindex(points)
        )

    # =========================
    # FIGURE
    # =========================
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xticks(points)

    ax.plot(points, maximum, "o-", color="red", label="Maximum", lw=2)
    ax.plot(points, minimum, "o-", color="blue", label="Minimum", lw=2)

    # automatyczne kolory dla patternów
    colors = ["green", "black", "purple", "orange", "brown"]

    for i, (pat, curve) in enumerate(pattern_curves.items()):
        ax.plot(
            points,
            curve,
            "o--",
            color=colors[i % len(colors)],
            label=f"Pattern {pat}",
            lw=2,
        )

    # =========================
    # ETYKIETY
    # =========================
    for x in points:

        # MAX
        ax.text(
            x,
            maximum.loc[x] + 0.8,
            f"{int(max_patterns.loc[x])}",
            color="red",
            ha="center",
            va="bottom",
            fontsize=10,
            clip_on=False,
        )

        # MIN
        y = minimum.loc[x]
        pat = int(min_patterns.loc[x])

        if x == 4:
            ax.text(
                x, y - 2.5, f"{pat}", color="blue", ha="center", va="top", fontsize=10
            )

        elif x == 10:
            ax.text(
                x,
                -0.10,
                f"{pat}",
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="top",
                color="blue",
                fontsize=10,
                clip_on=False,
            )

        elif x == 14:
            ax.text(
                x,
                y + 2.5,
                f"{pat}",
                color="blue",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        else:
            ax.text(
                x, y - 0.8, f"{pat}", color="blue", ha="center", va="top", fontsize=10
            )

    # =========================
    # STYLING
    # =========================
    ax.set_xlabel("Measurement Point", fontsize=16)
    ax.set_ylabel("Received Power [dB]", fontsize=16)
    ax.set_title("Received Power vs Measurement Point", fontsize=18)

    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=13)

    fig.tight_layout()
    out = os.path.join(output_folder, "Power_vs_Point_FINAL.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"[OK] Saved: {out}")


# =========================
# MAIN
# =========================
data = load_all_points(input_folder)

# pliki 4–22 → 19 punktów
data = data[data["Point"].between(4, 22)]
mapping = {old: new for new, old in enumerate(sorted(data["Point"].unique()), start=1)}
data["Point"] = data["Point"].map(mapping)

generate_plot(data)
print("Zakończono.")
