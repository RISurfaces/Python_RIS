import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import seaborn as sns
from tqdm import tqdm

# 🔧 Folder, w którym znajdują się pliki _avg.csv
input_dir = r"C:\Users\d0437921\Documents\GitHub\Python_RIS\DANE_Z_POMIAROW\KAKOLEWO_25\pazdziernik_pomiary\21_10_25\scenariusz_siatka\wykresy"

# 🔧 Folder na wykresy
output_dir = os.path.join(input_dir, "wykresy_final")
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

    # Podziel pliki na dwie grupy: H_8_7 i H_13_7
    files_87 = [f for f in files if "H_8_7" in f]
    files_137 = [f for f in files if "H_13_7" in f]

    for group_name, group_files in [("H_8_7m", files_87), ("H_13_7m", files_137)]:
        if not group_files:
            print(f"⚠️ Brak plików dla {group_name}")
            continue

        print(f"📊 Tworzenie mapy cieplnej dla: {group_name}")

        # Dane do heatmapy
        min_texts_list = []
        min_nums_list = []

        for pkt in tqdm(pkt_grid_order, desc=f"Wczytywanie {group_name}", unit="pkt"):
            f_match = [f for f in group_files if f"PKT_{pkt}_" in f]
            if f_match:
                df = pd.read_csv(os.path.join(input_dir, f_match[0]), sep=";")
                # min i max pattern
                min_idx = df["avg_power"].idxmin()
                min_val = df["avg_power"].iloc[min_idx]
                min_pattern = df["pattern"].iloc[min_idx]
                # Tekst: moc, pattern, pkt
                min_texts_list.append(f"{min_val:.2f}\npat {min_pattern}\nPKT {pkt}")
                min_nums_list.append(min_val)
            else:
                min_texts_list.append("brak")
                min_nums_list.append(np.nan)

        # Utwórz macierz 3x3
        grid_size = 3
        heatmap_data = np.array(min_nums_list).reshape(grid_size, grid_size)
        heatmap_texts = np.array(min_texts_list).reshape(grid_size, grid_size)

        # Tworzenie heatmapy
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
        )
        plt.title(f"Mapa cieplna - {group_name}")
        plt.xlabel("Kolumna PKT")
        plt.ylabel("Wiersz PKT")

        # Zapis wykresu
        plot_path = os.path.join(output_dir, f"heatmap_{group_name}.png")
        plt.savefig(plot_path, bbox_inches="tight", dpi=200)
        plt.close()
        print(f"✅ Zapisano mapę cieplną: {plot_path}\n")


# 🔥 Uruchomienie
if __name__ == "__main__":
    process_heatmaps(input_dir)
