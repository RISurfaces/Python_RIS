import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
        plt.figure(figsize=(10, 9))
        sns.heatmap(
            min_nums,
            annot=min_texts,
            fmt="",
            cmap="viridis",
            cbar_kws={"label": "Moc [dBm]"},
            xticklabels=[1, 2, 3],
            yticklabels=[1, 2, 3],
            square=True,
            linewidths=0.5,
            linecolor="gray",
            vmin=-90,  # 🔹 Minimalna wartość skali
            vmax=-50,
        )
        plt.title(f"Mapa cieplna (MIN) - {group_name}")
        plt.xlabel("Kolumna PKT")
        plt.ylabel("Wiersz PKT")
        plt.savefig(
            os.path.join(output_dir, f"heatmap_min_{group_name}.png"),
            bbox_inches="tight",
            dpi=200,
        )
        plt.close()

        # Heatmapa MAX
        plt.figure(figsize=(10, 9))
        sns.heatmap(
            max_nums,
            annot=max_texts,
            fmt="",
            cmap="viridis",
            cbar_kws={"label": "Moc [dBm]"},
            xticklabels=[1, 2, 3],
            yticklabels=[1, 2, 3],
            square=True,
            linewidths=0.5,
            linecolor="gray",
            vmin=-90,  # 🔹 Minimalna wartość skali
            vmax=-50,
        )
        plt.title(f"Mapa cieplna (MAX) - {group_name}")
        plt.xlabel("Kolumna PKT")
        plt.ylabel("Wiersz PKT")
        plt.savefig(
            os.path.join(output_dir, f"heatmap_max_{group_name}.png"),
            bbox_inches="tight",
            dpi=200,
        )
        plt.close()

        print(f"✅ Zapisano mapy cieplne dla {group_name}")


if __name__ == "__main__":
    process_heatmaps(file_list)
