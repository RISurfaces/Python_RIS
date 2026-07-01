import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "wykresy"
HEIGHTS = [10, 20, 30, 40, 50]
CSV_COLUMNS = ["measurement", "pattern", "frequency", "power"]
LANGUAGE_TEXT = {
    "EN": {
        "mean_label": "Mean ± SD across RIS patterns",
        "best_label": "Best RIS pattern",
        "pattern_prefix": "pat.",
        "optimum": "Best altitude",
        "title": "Influence of UAV–RIS altitude on received power",
        "x_label": "UAV–RIS altitude [m]",
        "y_label": "Received power [dBm]",
        "filename": "received_power_vs_altitude_EN.png",
    },
    "PL": {
        "mean_label": "Średnia ± SD dla patternów RIS",
        "best_label": "Najlepszy pattern RIS",
        "pattern_prefix": "pat.",
        "optimum": "Najkorzystniejsza wysokość",
        "title": "Wpływ wysokości UAV–RIS na moc odbieraną",
        "x_label": "Wysokość UAV–RIS [m]",
        "y_label": "Moc odebrana [dBm]",
        "filename": "received_power_vs_altitude_PL.png",
    },
}


def load_height_data(heights=HEIGHTS):
    """Load received-power measurements for all investigated altitudes."""
    frames = []
    for height in heights:
        input_path = SCRIPT_DIR / f"{height}m.csv"
        frame = pd.read_csv(
            input_path,
            sep=";",
            header=None,
            names=CSV_COLUMNS,
        )
        frame["height"] = height
        frames.append(frame)

    return pd.concat(frames, ignore_index=True)


def calculate_height_statistics(data):
    """Calculate distribution and best-pattern statistics by altitude."""
    summary = (
        data.groupby("height")["power"]
        .agg(mean="mean", std="std", minimum="min", maximum="max")
        .reset_index()
        .sort_values("height")
    )

    best_rows = data.loc[data.groupby("height")["power"].idxmax()]
    best_patterns = best_rows.set_index("height")["pattern"].astype(int)
    summary["best_pattern"] = summary["height"].map(best_patterns)
    return summary


def generate_altitude_summary_figure(data, language="EN", output_dir=OUTPUT_DIR):
    """Generate one publication-ready figure in English or Polish."""
    language = language.upper()
    if language not in LANGUAGE_TEXT:
        supported = ", ".join(LANGUAGE_TEXT)
        raise ValueError(f"Unsupported language: {language}. Choose: {supported}.")
    text = LANGUAGE_TEXT[language]

    summary = calculate_height_statistics(data)
    heights = summary["height"].to_numpy()
    means = summary["mean"].to_numpy()
    standard_deviations = summary["std"].to_numpy()
    maxima = summary["maximum"].to_numpy()
    best_patterns = summary["best_pattern"].to_numpy()

    fig, ax = plt.subplots(figsize=(8.6, 5.4))

    ax.errorbar(
        heights,
        means,
        yerr=standard_deviations,
        fmt="o-",
        color="#1f77b4",
        ecolor="#1f77b4",
        linewidth=2,
        elinewidth=1.5,
        capsize=5,
        markersize=7,
        label=text["mean_label"],
        zorder=3,
    )
    ax.plot(
        heights,
        maxima,
        marker="*",
        linestyle="--",
        color="#d62728",
        linewidth=1.7,
        markersize=11,
        label=text["best_label"],
        zorder=3,
    )

    for height, maximum, pattern in zip(heights, maxima, best_patterns):
        ax.annotate(
            f"{text['pattern_prefix']} {pattern}",
            xy=(height, maximum),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#a51d1d",
        )

    optimum_index = int(np.argmax(means))
    optimum_height = heights[optimum_index]
    optimum_mean = means[optimum_index]
    ax.axvspan(
        optimum_height - 2.3,
        optimum_height + 2.3,
        color="#2ca02c",
        alpha=0.09,
        zorder=0,
    )
    ax.annotate(
        f"{text['optimum']}: {optimum_height:.0f} m",
        xy=(optimum_height, optimum_mean),
        xytext=(31, -61),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#2a7f2a", "lw": 1.2},
        color="#2a7f2a",
        fontsize=10,
        fontweight="bold",
    )

    ax.set_title(text["title"], fontsize=14)
    ax.set_xlabel(text["x_label"], fontsize=11)
    ax.set_ylabel(text["y_label"], fontsize=11)
    ax.set_xticks(heights)
    ax.set_ylim(-100, -50)
    ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.45)
    ax.legend(loc="lower left", frameon=True, fontsize=9.5)
    fig.tight_layout()

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / text["filename"]
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved altitude summary figure: {output_path}")
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))
    return output_path, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the altitude figure.")
    parser.add_argument(
        "--language",
        choices=sorted(LANGUAGE_TEXT),
        default="EN",
        help="Figure language (default: EN).",
    )
    arguments = parser.parse_args()
    height_data = load_height_data()
    generate_altitude_summary_figure(height_data, language=arguments.language)
