import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import os
import re
from tqdm import tqdm

# Folder z plikami CSV
input_dir = (
    r"DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka"
)

# Folder na wykresy
output_dir = os.path.join(input_dir, "wykresy")
os.makedirs(output_dir, exist_ok=True)

# Publication export settings. The comparison heatmaps are reduced to page
# width in LaTeX, so both a high raster resolution and larger labels are used.
PUBLICATION_DPI = 600
ANNOTATION_FONTSIZE = 14.5
TITLE_FONTSIZE = 15
AXIS_LABEL_FONTSIZE = 13
TICK_LABEL_FONTSIZE = 12

# Lista plików CSV
file_list = [
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_1_H_8_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_1_H_13_7m_V_1_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_2_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_2_H_13_7m_V_2_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_3_H_8_7m_V_4_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_3_H_13_7m_V_3_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_4_H_8_7m_V_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_4_H_13_7m_V_2m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_5_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_5_H_13_7m_V_1_7m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_6_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_6_H_13_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_7_H_8_7m_V_3_5m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_7_H_13_7m_V_1_9m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_8_H_8_7m_V_3m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_8_H_13_7m_V_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_9_H_8_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_9_H_13_7m_V_3_2m.csv",
]

# Układ punktów w macierzy 3x3
pkt_grid_order = [7, 4, 1, 8, 5, 2, 9, 6, 3]  # od lewej do prawej, od góry do dołu


def extract_info(filepath):
    """Wyciąga numer punktu i wysokość H_x_xm"""
    filename = os.path.basename(filepath)
    match = re.search(r"PKT_(\d+)_H_(\d+_\d+)m", filename)
    if match:
        pkt_num = int(match.group(1))
        height = match.group(2)
        return pkt_num, height
    return None, None


def _draw_heatmap(
    ax,
    values,
    annotations=None,
    *,
    title="",
    xlabel="",
    ylabel="",
    vmin=-90,
    vmax=-50,
    cmap="viridis",
    norm=None,
    colorbar=False,
    colorbar_label="",
    figure=None,
    annotation_fontsize=ANNOTATION_FONTSIZE,
):
    """Draw a 3x3 heatmap using Matplotlib only."""
    image_kwargs = {"cmap": cmap, "aspect": "equal"}
    if norm is None:
        image_kwargs.update(vmin=vmin, vmax=vmax)
        text_norm = plt.Normalize(vmin=vmin, vmax=vmax)
    else:
        image_kwargs["norm"] = norm
        text_norm = norm

    image = ax.imshow(values, **image_kwargs)
    ax.set_xticks(range(3), labels=[1, 2, 3])
    ax.set_yticks(range(3), labels=[1, 2, 3])
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.7)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_title(title, fontsize=TITLE_FONTSIZE, pad=12)
    ax.set_xlabel(xlabel, fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_FONTSIZE)

    if annotations is not None:
        colormap = plt.get_cmap(cmap)
        for row in range(3):
            for column in range(3):
                value = values[row, column]
                red, green, blue, _ = colormap(text_norm(value))
                luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
                text_color = "white" if luminance < 0.5 else "#111111"
                ax.text(
                    column,
                    row,
                    annotations[row, column],
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=annotation_fontsize,
                    fontweight="semibold",
                )

    if colorbar:
        fig = figure if figure is not None else ax.figure
        bar = fig.colorbar(image, ax=ax)
        bar.set_label(colorbar_label, fontsize=AXIS_LABEL_FONTSIZE)
        bar.ax.tick_params(labelsize=TICK_LABEL_FONTSIZE)

    return image


def process_heatmaps(file_list):
    # Podział na grupy wg wysokości
    files_87 = [f for f in file_list if "H_8_7" in f]
    files_137 = [f for f in file_list if "H_13_7" in f]

    for group_name, group_files in [("H_8_7m", files_87), ("H_13_7m", files_137)]:
        min_texts_list = []
        min_nums_list = []
        max_texts_list = []
        max_nums_list = []

        print(f"\n📊 Przetwarzanie grupy: {group_name}")
        for pkt in tqdm(pkt_grid_order, desc=f"Grupa {group_name}", unit="pkt"):
            f_match = [f for f in group_files if f"PKT_{pkt}_" in f]
            if f_match:
                df = pd.read_csv(
                    f_match[0],
                    sep=";",
                    header=None,
                    names=["col1", "pattern", "freq", "power"],
                )
                min_idx = df["power"].idxmin()
                max_idx = df["power"].idxmax()
                min_val = df["power"].iloc[min_idx]
                max_val = df["power"].iloc[max_idx]
                min_pattern = df["pattern"].iloc[min_idx]
                max_pattern = df["pattern"].iloc[max_idx]

                # Tekst: moc, numer patternu, numer PKT
                min_texts_list.append(f"{min_val:.2f}\npat {min_pattern}\nPKT {pkt}")
                min_nums_list.append(min_val)
                max_texts_list.append(f"{max_val:.2f}\npat {max_pattern}\nPKT {pkt}")
                max_nums_list.append(max_val)
            else:
                min_texts_list.append("brak")
                min_nums_list.append(np.nan)
                max_texts_list.append("brak")
                max_nums_list.append(np.nan)

        # Tworzenie macierzy 3x3 w wybranym układzie
        grid_size = 3
        min_texts = np.array(min_texts_list).reshape(grid_size, grid_size)
        min_nums = np.array(min_nums_list).reshape(grid_size, grid_size)
        max_texts = np.array(max_texts_list).reshape(grid_size, grid_size)
        max_nums = np.array(max_nums_list).reshape(grid_size, grid_size)

        # Heatmapa MIN
        fig, ax = plt.subplots(figsize=(10, 9))
        _draw_heatmap(
            ax,
            min_nums,
            min_texts,
            title=f"Mapa cieplna (MIN) - {group_name}",
            xlabel="Kolumna PKT",
            ylabel="Wiersz PKT",
            vmin=-90,
            vmax=-50,
            colorbar=True,
            colorbar_label="Moc [dBm]",
            figure=fig,
        )
        fig.savefig(
            os.path.join(output_dir, f"heatmap_min_{group_name}.png"),
            bbox_inches="tight",
            dpi=PUBLICATION_DPI,
        )
        plt.close(fig)

        # Heatmapa MAX
        fig, ax = plt.subplots(figsize=(10, 9))
        _draw_heatmap(
            ax,
            max_nums,
            max_texts,
            title=f"Mapa cieplna (MAX) - {group_name}",
            xlabel="Kolumna PKT",
            ylabel="Wiersz PKT",
            vmin=-90,
            vmax=-50,
            colorbar=True,
            colorbar_label="Moc [dBm]",
            figure=fig,
        )
        fig.savefig(
            os.path.join(output_dir, f"heatmap_max_{group_name}.png"),
            bbox_inches="tight",
            dpi=PUBLICATION_DPI,
        )
        plt.close(fig)

        print(f"✅ Zapisano mapy cieplne dla {group_name}")


def _build_max_grid(group_files, point_label="PT"):
    """Build a 3x3 grid containing the maximum measured power per point."""
    values = []
    annotations = []

    for point in pkt_grid_order:
        matching_files = [path for path in group_files if f"PKT_{point}_" in path]
        if not matching_files:
            values.append(np.nan)
            annotations.append("missing")
            continue

        df = pd.read_csv(
            matching_files[0],
            sep=";",
            header=None,
            names=["col1", "pattern", "freq", "power"],
        )
        max_row = df.loc[df["power"].idxmax()]
        max_power = float(max_row["power"])
        pattern = int(max_row["pattern"])

        values.append(max_power)
        annotations.append(
            f"{max_power:.2f}\npat {pattern}\n{point_label} {point}"
        )

    return (
        np.asarray(values).reshape(3, 3),
        np.asarray(annotations).reshape(3, 3),
    )


def _build_average_grid(group_files, point_label="PT"):
    """Build a 3x3 grid containing the mean measured power per point."""
    values = []
    annotations = []

    for point in pkt_grid_order:
        matching_files = [path for path in group_files if f"PKT_{point}_" in path]
        if not matching_files:
            values.append(np.nan)
            annotations.append("missing")
            continue

        df = pd.read_csv(
            matching_files[0],
            sep=";",
            header=None,
            names=["col1", "pattern", "freq", "power"],
        )
        average_power = float(df["power"].mean())
        values.append(average_power)
        annotations.append(f"{average_power:.2f}\n{point_label} {point}")

    return (
        np.asarray(values).reshape(3, 3),
        np.asarray(annotations).reshape(3, 3),
    )


def generate_english_max_comparison(
    file_list,
    *,
    annotation_fontsize=ANNOTATION_FONTSIZE,
    filename_suffix="",
):
    """Generate a publication-ready English figure with both MAX heatmaps."""
    height_groups = [
        ("8.7", [path for path in file_list if "H_8_7" in path]),
        ("13.7", [path for path in file_list if "H_13_7" in path]),
    ]

    vmin, vmax = -90, -50
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.4))
    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        bottom=0.1,
        top=0.87,
        wspace=0.28,
    )

    for panel_index, (ax, (height, group_files)) in enumerate(
        zip(axes, height_groups)
    ):
        max_values, annotations = _build_max_grid(group_files, point_label="PT")

        image = _draw_heatmap(
            ax,
            max_values,
            vmin=vmin,
            vmax=vmax,
        )

        # Use light text on dark cells and dark text on bright cells.
        for row in range(3):
            for column in range(3):
                value = max_values[row, column]
                text_color = "white" if norm(value) < 0.55 else "#111111"
                ax.text(
                    column,
                    row,
                    annotations[row, column],
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=annotation_fontsize,
                    fontweight="semibold",
                )

        panel_label = chr(ord("a") + panel_index)
        ax.set_title(
            f"({panel_label}) Maximum received power, H = {height} m",
            fontsize=TITLE_FONTSIZE,
            pad=12,
        )
        ax.set_xlabel("PT column", fontsize=AXIS_LABEL_FONTSIZE)
        ax.set_ylabel(
            "PT row" if panel_index == 0 else "",
            fontsize=AXIS_LABEL_FONTSIZE,
        )
        ax.tick_params(axis="both", labelsize=TICK_LABEL_FONTSIZE)
        colorbar = fig.colorbar(image, ax=ax)
        colorbar.set_label(
            "Received power [dBm]",
            fontsize=AXIS_LABEL_FONTSIZE,
        )
        colorbar.ax.tick_params(labelsize=TICK_LABEL_FONTSIZE)

    output_path = os.path.join(
        output_dir,
        f"heatmap_max_comparison_EN{filename_suffix}.png",
    )
    fig.savefig(
        output_path,
        dpi=PUBLICATION_DPI,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)
    print(f"✅ Saved English comparison figure: {output_path}")


def generate_english_average_comparison(
    file_list,
    *,
    annotation_fontsize=ANNOTATION_FONTSIZE,
    filename_suffix="",
):
    """Generate a publication-ready English figure with both AVG heatmaps."""
    height_groups = [
        ("8.7", [path for path in file_list if "H_8_7" in path]),
        ("13.7", [path for path in file_list if "H_13_7" in path]),
    ]

    average_grids = []
    for height, group_files in height_groups:
        values, annotations = _build_average_grid(group_files, point_label="PT")
        average_grids.append((height, values, annotations))

    all_average_values = np.concatenate(
        [values.ravel() for _, values, _ in average_grids]
    )
    vmin = 5 * np.floor(np.nanmin(all_average_values) / 5)
    vmax = 5 * np.ceil(np.nanmax(all_average_values) / 5)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.4))
    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        bottom=0.1,
        top=0.87,
        wspace=0.28,
    )

    for panel_index, (ax, (height, average_values, annotations)) in enumerate(
        zip(axes, average_grids)
    ):
        image = _draw_heatmap(
            ax,
            average_values,
            annotations,
            vmin=vmin,
            vmax=vmax,
            annotation_fontsize=annotation_fontsize,
        )

        panel_label = chr(ord("a") + panel_index)
        ax.set_title(
            f"({panel_label}) Mean received power, H = {height} m",
            fontsize=TITLE_FONTSIZE,
            pad=12,
        )
        ax.set_xlabel("PT column", fontsize=AXIS_LABEL_FONTSIZE)
        ax.set_ylabel(
            "PT row" if panel_index == 0 else "",
            fontsize=AXIS_LABEL_FONTSIZE,
        )
        ax.tick_params(axis="both", labelsize=TICK_LABEL_FONTSIZE)
        colorbar = fig.colorbar(image, ax=ax)
        colorbar.set_label(
            "Mean received power [dBm]",
            fontsize=AXIS_LABEL_FONTSIZE,
        )
        colorbar.ax.tick_params(labelsize=TICK_LABEL_FONTSIZE)

    output_path = os.path.join(
        output_dir,
        f"heatmap_average_comparison_EN{filename_suffix}.png",
    )
    fig.savefig(
        output_path,
        dpi=PUBLICATION_DPI,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)
    print(f"✅ Saved English average comparison figure: {output_path}")


def generate_english_max_difference(
    file_list,
    *,
    annotation_fontsize=ANNOTATION_FONTSIZE,
    filename_suffix="",
):
    """Generate a heatmap of Pmax(13.7 m) minus Pmax(8.7 m)."""
    files_87 = [path for path in file_list if "H_8_7" in path]
    files_137 = [path for path in file_list if "H_13_7" in path]
    max_values_87, _ = _build_max_grid(files_87, point_label="PT")
    max_values_137, _ = _build_max_grid(files_137, point_label="PT")
    difference = max_values_137 - max_values_87

    point_grid = np.asarray(pkt_grid_order).reshape(3, 3)
    annotations = np.empty((3, 3), dtype=object)
    for row in range(3):
        for column in range(3):
            annotations[row, column] = (
                f"{difference[row, column]:+.2f} dB\n"
                f"PT {point_grid[row, column]}"
            )

    max_absolute_difference = np.nanmax(np.abs(difference))
    color_limit = 5 * np.ceil(max_absolute_difference / 5)
    norm = TwoSlopeNorm(
        vmin=-color_limit,
        vcenter=0,
        vmax=color_limit,
    )

    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    _draw_heatmap(
        ax,
        difference,
        annotations,
        title="Difference in maximum received power\nH = 13.7 m − H = 8.7 m",
        xlabel="PT column",
        ylabel="PT row",
        cmap="RdBu_r",
        norm=norm,
        colorbar=True,
        colorbar_label="Power difference [dB]",
        figure=fig,
        annotation_fontsize=annotation_fontsize,
    )
    ax.tick_params(axis="both", labelsize=TICK_LABEL_FONTSIZE)
    fig.tight_layout()

    output_path = os.path.join(
        output_dir,
        f"heatmap_max_difference_EN{filename_suffix}.png",
    )
    fig.savefig(
        output_path,
        dpi=PUBLICATION_DPI,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)
    print(f"✅ Saved English difference heatmap: {output_path}")


if __name__ == "__main__":
    process_heatmaps(file_list)
    generate_english_max_comparison(file_list)
    generate_english_average_comparison(file_list)
    generate_english_max_difference(file_list)
    generate_english_max_comparison(
        file_list,
        annotation_fontsize=13,
        filename_suffix="_font13",
    )
    generate_english_average_comparison(
        file_list,
        annotation_fontsize=13,
        filename_suffix="_font13",
    )
    generate_english_max_difference(
        file_list,
        annotation_fontsize=13,
        filename_suffix="_font13",
    )
