import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import seaborn as sns
from tqdm import tqdm

# 🔧 Folder, w którym znajdują się pliki _avg.csv
input_dir = "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\wykresy"

# 🔧 Folder na wykresy
output_dir = os.path.join(input_dir, "wykresy")
os.makedirs(output_dir, exist_ok=True)


def extract_info(filename):
    """
    Wyciąga numer punktu i wysokość H_x_xm z nazwy pliku.
    Np. PKT_3_H_8_7m_V_3m_avg.csv → (3, "8_7")
    """
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

        data_points = []
        for f in tqdm(group_files, desc=f"Wczytywanie {group_name}", unit="plik"):
            pkt_num, _ = extract_info(f)
            if pkt_num is None:
                continue

            # Wczytaj dane z CSV
            df = pd.read_csv(os.path.join(input_dir, f), sep=";")

            # Wylicz średnią mocy z kolumny avg_power
            avg_power = df["avg_power"].mean()
            data_points.append((pkt_num, avg_power))

        # Posortuj po numerze punktu
        data_points.sort(key=lambda x: x[0])

        # Zakładamy układ 3x3 (9 punktów)
        grid_size = int(np.ceil(np.sqrt(len(data_points))))
        values = [p[1] for p in data_points]

        # Utwórz macierz 3x3 z wartości
        heatmap_data = np.array(values).reshape(grid_size, grid_size)

        # Tworzenie heatmapy
        plt.figure(figsize=(8, 7))
        sns.heatmap(
            heatmap_data,
            annot=True,
            cmap="viridis",
            fmt=".2f",
            cbar_kws={"label": "Średnia moc [dBm]"},
            square=True,
        )
        plt.title(f"Mapa cieplna - {group_name}")
        plt.xlabel("Pozycja X")
        plt.ylabel("Pozycja Y")

        # Zapis wykresu do pliku
        plot_path = os.path.join(output_dir, f"heatmap_{group_name}.png")
        plt.savefig(plot_path, bbox_inches="tight", dpi=200)
        plt.close()

        print(f"✅ Zapisano mapę cieplną: {plot_path}\n")


# 🔥 Uruchomienie
if __name__ == "__main__":
    process_heatmaps(input_dir)
