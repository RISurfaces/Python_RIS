import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "wykresy"
HEIGHTS = [10, 20, 30, 40, 50]
CSV_COLUMNS = ["measurement", "pattern", "frequency", "power"]
# Combined Tx/Rx off-axis loss obtained from the measured antenna patterns for
# the link geometry at each UAV-RIS altitude. The values are additive in dB.
ANTENNA_PATTERN_CORRECTION_DB = {
    10: 19.2645,
    20: 2.0277,
    30: 0.1498,
    40: 1.2104,
    50: 2.2259,
}
LANGUAGE_TEXT = {
    "EN": {
        "mean_label": "Mean ± SD across RIS patterns",
        "best_label": "Best RIS pattern",
        "measured_mean_label": "Measured mean",
        "corrected_mean_label": "Antenna-corrected mean ± SD",
        "pattern_prefix": "pat.",
        "measured_optimum": "Highest measured mean",
        "corrected_optimum": "Highest corrected mean",
        "measured_title": "Influence of UAV–RIS altitude on received power",
        "corrected_title": "Effect of antenna-pattern correction",
        "x_label": "UAV–RIS altitude [m]",
        "y_label": "Received power [dBm]",
        "filename": "received_power_vs_altitude_EN.png",
        "corrected_filename": "received_power_vs_altitude_corrected_EN.png",
    },
    "PL": {
        "mean_label": "Średnia ± SD dla patternów RIS",
        "best_label": "Najlepszy pattern RIS",
        "measured_mean_label": "Średnia zmierzona",
        "corrected_mean_label": "Średnia po korekcji antenowej ± SD",
        "pattern_prefix": "pat.",
        "measured_optimum": "Najwyższa zmierzona średnia",
        "corrected_optimum": "Najwyższa skorygowana średnia",
        "measured_title": "Wpływ wysokości UAV–RIS na moc odbieraną",
        "corrected_title": "Wpływ korekcji charakterystyki anten",
        "x_label": "Wysokość UAV–RIS [m]",
        "y_label": "Moc odebrana [dBm]",
        "filename": "received_power_vs_altitude_PL.png",
        "corrected_filename": "received_power_vs_altitude_corrected_PL.png",
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
    summary["antenna_correction_db"] = summary["height"].map(
        ANTENNA_PATTERN_CORRECTION_DB
    )
    if summary["antenna_correction_db"].isna().any():
        missing_heights = summary.loc[
            summary["antenna_correction_db"].isna(), "height"
        ].tolist()
        raise ValueError(
            f"Missing antenna-pattern correction for heights: {missing_heights}"
        )
    summary["corrected_mean"] = (
        summary["mean"] + summary["antenna_correction_db"]
    )
    summary["corrected_maximum"] = (
        summary["maximum"] + summary["antenna_correction_db"]
    )
    return summary


def generate_altitude_summary_figure(data, language="EN", output_dir=OUTPUT_DIR):
    """Generate measured and antenna-corrected altitude figures."""
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
    corrections = summary["antenna_correction_db"].to_numpy()
    corrected_means = summary["corrected_mean"].to_numpy()
    best_patterns = summary["best_pattern"].to_numpy()

    output_dir.mkdir(parents=True, exist_ok=True)

    # Figure 1: directly measured statistics, without antenna correction.
    measured_fig, measured_ax = plt.subplots(figsize=(8.8, 5.5))
    measured_ax.errorbar(
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
    measured_ax.plot(
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
        measured_ax.annotate(
            f"{text['pattern_prefix']} {pattern}",
            xy=(height, maximum),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#a51d1d",
        )

    measured_optimum_index = int(np.argmax(means))
    measured_optimum_height = heights[measured_optimum_index]
    measured_optimum_mean = means[measured_optimum_index]
    measured_ax.axvspan(
        measured_optimum_height - 2.3,
        measured_optimum_height + 2.3,
        color="#2ca02c",
        alpha=0.09,
        zorder=0,
    )
    measured_ax.annotate(
        f"{text['measured_optimum']}: {measured_optimum_height:.0f} m",
        xy=(measured_optimum_height, measured_optimum_mean),
        xytext=(31, -61),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#2a7f2a", "lw": 1.2},
        color="#2a7f2a",
        fontsize=10,
        fontweight="bold",
    )

    measured_ax.set_title(text["measured_title"], fontsize=14)
    measured_ax.set_xlabel(text["x_label"], fontsize=11)
    measured_ax.set_ylabel(text["y_label"], fontsize=11)
    measured_ax.set_xticks(heights)
    measured_ax.set_ylim(-100, -50)
    measured_ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.45)
    measured_ax.legend(loc="lower left", frameon=True, fontsize=9.5)
    measured_fig.tight_layout()

    measured_path = output_dir / text["filename"]
    measured_fig.savefig(
        measured_path,
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(measured_fig)

    # Figure 2: mean power before and after the altitude-specific antenna loss
    # correction. The standard deviation is unchanged by an additive offset.
    corrected_fig, corrected_ax = plt.subplots(figsize=(8.8, 5.5))
    corrected_ax.plot(
        heights,
        means,
        marker="o",
        linestyle="-",
        color="#7f7f7f",
        linewidth=1.8,
        markersize=6.5,
        label=text["measured_mean_label"],
        zorder=3,
    )
    corrected_ax.errorbar(
        heights,
        corrected_means,
        yerr=standard_deviations,
        fmt="o--",
        markerfacecolor="white",
        markeredgewidth=1.8,
        color="#2ca02c",
        ecolor="#2ca02c",
        linewidth=2,
        elinewidth=1.3,
        capsize=4,
        markersize=7,
        label=text["corrected_mean_label"],
        zorder=4,
    )

    for height, measured_mean, corrected_mean, standard_deviation, correction in zip(
        heights,
        means,
        corrected_means,
        standard_deviations,
        corrections,
    ):
        corrected_ax.vlines(
            height,
            measured_mean,
            corrected_mean,
            color="#9a9a9a",
            linestyle=":",
            linewidth=1,
            alpha=0.7,
            zorder=1,
        )
        corrected_ax.annotate(
            f"+{correction:.2f} dB",
            xy=(height, corrected_mean + standard_deviation),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#237a23",
        )

    corrected_optimum_index = int(np.argmax(corrected_means))
    corrected_optimum_height = heights[corrected_optimum_index]
    corrected_optimum_mean = corrected_means[corrected_optimum_index]
    corrected_ax.axvspan(
        corrected_optimum_height - 2.3,
        corrected_optimum_height + 2.3,
        color="#2ca02c",
        alpha=0.09,
        zorder=0,
    )
    corrected_ax.annotate(
        f"{text['corrected_optimum']}: {corrected_optimum_height:.0f} m",
        xy=(corrected_optimum_height, corrected_optimum_mean),
        xytext=(15, -50.5),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#2a7f2a", "lw": 1.2},
        color="#2a7f2a",
        fontsize=10,
        fontweight="bold",
    )

    corrected_ax.set_title(text["corrected_title"], fontsize=14)
    corrected_ax.set_xlabel(text["x_label"], fontsize=11)
    corrected_ax.set_ylabel(text["y_label"], fontsize=11)
    corrected_ax.set_xticks(heights)
    corrected_ax.set_ylim(-100, -45)
    corrected_ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.45)
    corrected_ax.legend(loc="lower left", frameon=True, fontsize=9.5)
    corrected_fig.tight_layout()

    corrected_path = output_dir / text["corrected_filename"]
    corrected_fig.savefig(
        corrected_path,
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(corrected_fig)

    print(f"Saved measured altitude figure: {measured_path}")
    print(f"Saved corrected altitude figure: {corrected_path}")
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.2f}"))
    return (measured_path, corrected_path), summary


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
