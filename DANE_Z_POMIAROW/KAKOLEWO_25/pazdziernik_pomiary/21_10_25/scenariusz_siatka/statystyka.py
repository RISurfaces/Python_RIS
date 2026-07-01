import argparse
from pathlib import Path
import re

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "wykresy_statystyczne"
CSV_COLUMNS = ["measurement", "pattern", "frequency", "power"]
HEIGHTS = [8.7, 13.7]
POINTS = np.arange(1, 10)
HEIGHT_COLORS = {8.7: "#1f77b4", 13.7: "#ff7f0e"}

LANGUAGE_TEXT = {
    "EN": {
        "distribution_title": "(a) Distribution of pattern-averaged power",
        "best_title": "(b) Best RIS pattern at each receiver point",
        "x_label": "Receiver point (PT)",
        "y_label": "Received power [dBm]",
        "height_label": "H = {height:.1f} m",
        "pattern_prefix": "pat.",
        "filename": "statistical_summary_point_height_EN.png",
    },
    "PL": {
        "distribution_title": "(a) Rozkład średniej mocy patternów",
        "best_title": "(b) Najlepszy pattern RIS w każdym punkcie",
        "x_label": "Punkt odbiorczy (PT)",
        "y_label": "Moc odebrana [dBm]",
        "height_label": "H = {height:.1f} m",
        "pattern_prefix": "pat.",
        "filename": "statistical_summary_point_height_PL.png",
    },
}


def extract_point_and_height(path):
    """Extract the receiver point and UAV--RIS height from a CSV filename."""
    match = re.search(r"PKT_(\d+)_H_(8_7|13_7)m", path.name)
    if match is None:
        raise ValueError(f"Cannot extract point and height from {path.name}")

    point = int(match.group(1))
    height = float(match.group(2).replace("_", "."))
    return point, height


def load_grid_data():
    """Load all point-grid measurements for both UAV--RIS heights."""
    frames = []
    for path in sorted(SCRIPT_DIR.glob("PKT_*.csv*")):
        point, height = extract_point_and_height(path)
        frame = pd.read_csv(
            path,
            sep=";",
            header=None,
            names=CSV_COLUMNS,
        )
        frame["point"] = point
        frame["height"] = height
        frames.append(frame)

    if not frames:
        raise FileNotFoundError(f"No point-grid CSV files found in {SCRIPT_DIR}")
    return pd.concat(frames, ignore_index=True)


def calculate_pattern_statistics(data):
    """Calculate repeat statistics for every point, height, and RIS pattern."""
    return (
        data.groupby(["point", "height", "pattern"])["power"]
        .agg(mean="mean", std="std", samples="size")
        .reset_index()
        .sort_values(["point", "height", "pattern"])
    )


def select_best_patterns(pattern_statistics):
    """Select the pattern with the highest repeat-averaged power."""
    best_indices = pattern_statistics.groupby(["point", "height"])["mean"].idxmax()
    return pattern_statistics.loc[best_indices].sort_values(["point", "height"])


def _style_boxplot(boxplot, color):
    for box in boxplot["boxes"]:
        box.set_facecolor(color)
        box.set_edgecolor(color)
        box.set_alpha(0.55)
    for whisker in boxplot["whiskers"]:
        whisker.set_color(color)
    for cap in boxplot["caps"]:
        cap.set_color(color)
    for median in boxplot["medians"]:
        median.set_color("#202020")
        median.set_linewidth(1.4)


def generate_statistical_summary(data, language="EN", output_dir=OUTPUT_DIR):
    """Generate a two-panel statistical summary in English or Polish."""
    language = language.upper()
    if language not in LANGUAGE_TEXT:
        supported = ", ".join(LANGUAGE_TEXT)
        raise ValueError(f"Unsupported language: {language}. Choose: {supported}.")
    text = LANGUAGE_TEXT[language]

    pattern_statistics = calculate_pattern_statistics(data)
    best_patterns = select_best_patterns(pattern_statistics)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), sharey=True)
    offsets = {8.7: -0.19, 13.7: 0.19}

    for height in HEIGHTS:
        distributions = [
            pattern_statistics.loc[
                (pattern_statistics["point"] == point)
                & (pattern_statistics["height"] == height),
                "mean",
            ].to_numpy()
            for point in POINTS
        ]
        boxplot = axes[0].boxplot(
            distributions,
            positions=POINTS + offsets[height],
            widths=0.31,
            patch_artist=True,
            manage_ticks=False,
            showfliers=True,
            flierprops={
                "marker": ".",
                "markersize": 3,
                "markerfacecolor": HEIGHT_COLORS[height],
                "markeredgecolor": HEIGHT_COLORS[height],
                "alpha": 0.55,
            },
        )
        _style_boxplot(boxplot, HEIGHT_COLORS[height])

    legend_handles = [
        Patch(
            facecolor=HEIGHT_COLORS[height],
            edgecolor=HEIGHT_COLORS[height],
            alpha=0.55,
            label=text["height_label"].format(height=height),
        )
        for height in HEIGHTS
    ]
    axes[0].legend(handles=legend_handles, loc="upper right", fontsize=9)
    axes[0].set_title(text["distribution_title"], fontsize=12.5)
    axes[0].set_xlabel(text["x_label"], fontsize=11)
    axes[0].set_ylabel(text["y_label"], fontsize=11)

    for height in HEIGHTS:
        height_data = best_patterns[best_patterns["height"] == height]
        x_values = height_data["point"].to_numpy() + offsets[height]
        axes[1].errorbar(
            x_values,
            height_data["mean"],
            yerr=height_data["std"],
            fmt="o",
            color=HEIGHT_COLORS[height],
            ecolor=HEIGHT_COLORS[height],
            capsize=4,
            elinewidth=1.3,
            markersize=6,
            label=text["height_label"].format(height=height),
            zorder=3,
        )

        for x_value, row in zip(x_values, height_data.itertuples()):
            if int(row.point) == 8 and height == 13.7:
                label_y = row.mean - row.std
                label_offset = -4
                vertical_alignment = "top"
            else:
                label_y = row.mean + row.std
                label_offset = 4
                vertical_alignment = "bottom"

            axes[1].annotate(
                f"{text['pattern_prefix']} {int(row.pattern)}",
                xy=(x_value, label_y),
                xytext=(0, label_offset),
                textcoords="offset points",
                ha="center",
                va=vertical_alignment,
                fontsize=7.8,
                color=HEIGHT_COLORS[height],
            )

    axes[1].set_title(text["best_title"], fontsize=12.5)
    axes[1].set_xlabel(text["x_label"], fontsize=11)
    axes[1].legend(loc="upper right", fontsize=9)
    axes[1].tick_params(axis="y", labelleft=True)

    for ax in axes:
        ax.set_xticks(POINTS)
        ax.set_xlim(0.5, 9.5)
        ax.set_ylim(-85, -50)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.7, alpha=0.45)
        ax.tick_params(axis="both", labelsize=9.5)

    fig.tight_layout(w_pad=2.5)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / text["filename"]
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    best_output_path = output_dir / "best_pattern_summary.csv"
    best_patterns.to_csv(best_output_path, sep=";", index=False)
    print(f"Saved statistical summary figure: {output_path}")
    print(f"Saved best-pattern statistics: {best_output_path}")
    return output_path, best_patterns


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate grid statistics.")
    parser.add_argument(
        "--language",
        choices=sorted(LANGUAGE_TEXT),
        default="EN",
        help="Figure language (default: EN).",
    )
    arguments = parser.parse_args()
    grid_data = load_grid_data()
    generate_statistical_summary(grid_data, language=arguments.language)
