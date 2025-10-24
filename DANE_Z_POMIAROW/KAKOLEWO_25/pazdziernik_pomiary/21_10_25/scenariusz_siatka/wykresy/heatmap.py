import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from tqdm import tqdm

# 🔧 Folder z plikami _avg.csv
input_dir = r"DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/wykresy/avg"

# 🔧 Folder na wykresy
output_dir = os.path.join(input_dir, "heatmaps_final")
os.makedirs(output_dir, exist_ok=True)

# Układ punktów w macierzy 3x3
pkt_grid_order = [7, 4, 1, 8, 5, 2, 9, 6, 3]  # od lewej do prawej, od góry do dołu


def extract_info(filename):
    """Wyciąga numer punktu i wysokość H_x_xm z nazwy pliku."""
    match = re.search(r"PKT_(\d+)_H_(\d+_\d+)m", filename)
    if match:
        pkt_num = int(match.group(1))
        height = match.group(2)
        return pkt_num, height
    return None, None


def process_heatmaps(input_dir):
    # Wczytaj wszystkie pliki _avg.csv
    files = [f for f in os.listdir(input_dir) if f.endswith("_avg.csv")]

    # Grupowanie plików wg wysokości
    height_groups = {}
    for f in files:
        pkt_num, height = extract_info(f)
        if height is None or pkt_num is None:
            continue
        if height not in height_groups:
            height_groups[height] = []
        height_groups[height].append((pkt_num, f))

    for height, file_list in height_groups.items():
        print(f"\n📊 Tworzenie heatmap dla wysokości H={height}")

        # Wczytaj dane z wszystkich punktów
        data = {}  # data[pattern][pkt_num] = avg_power
        for pkt_num, f in file_list:
            df = pd.read_csv(os.path.join(input_dir, f), sep=";")
            for _, row in df.iterrows():
                pat = int(row["pattern"])
                val = row["avg_power"]
                if pat not in data:
                    data[pat] = {}
                data[pat][pkt_num] = val

        # Tworzenie heatmap dla każdego patternu
        for pat in sorted(data.keys()):
            pkt_dict = data[pat]
            values_list = []
            texts_list = []
            for pkt in pkt_grid_order:
                if pkt in pkt_dict:
                    val = pkt_dict[pkt]
                    values_list.append(val)
                    texts_list.append(f"{val:.2f}\nPKT {pkt}")
                else:
                    values_list.append(np.nan)
                    texts_list.append("brak")

            # Macierz 3x3
            grid_size = 3
            heatmap_data = np.array(values_list).reshape(grid_size, grid_size)
            heatmap_texts = np.array(texts_list).reshape(grid_size, grid_size)

            # Tworzenie heatmapy z równą skalą kolorów
            plt.figure(figsize=(10, 9))
            sns.heatmap(
                heatmap_data,
                annot=heatmap_texts,
                fmt="",
                cmap="viridis",
                cbar_kws={"label": "Średnia moc [dBm]"},
                square=True,
                linewidths=0.5,
                linecolor="gray",
                xticklabels=[1, 2, 3],
                yticklabels=[1, 2, 3],
                vmin=-90,  # 🔹 Minimalna wartość skali
                vmax=-50,  # 🔹 Maksymalna wartość skali
            )
            plt.title(f"Pattern {pat} - H={height}")
            plt.xlabel("Kolumna PKT")
            plt.ylabel("Wiersz PKT")

            # Zapis wykresu
            safe_name = f"heatmap_pat{pat}_H{height}.png"
            plot_path = os.path.join(output_dir, safe_name)
            plt.savefig(plot_path, bbox_inches="tight", dpi=200)
            plt.close()

        print(f"✅ Zapisano heatmapy dla H={height}")


if __name__ == "__main__":
    process_heatmaps(input_dir)
