import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv


def maximum_val(file_path):
    power_values = []
    # Patterny, które sprawdzamy
    filter_values = {1, 20, 17, 8, 23, 27}

    with open(file_path, mode="r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            # Sprawdź, czy wiersz nie jest pusty
            if row:
                # Sprawdź, czy wartość w 3 kolumnie (konwertując na int) jest w zbiorze filter_values
                if int(row[2]) in filter_values:
                    power_values.append(float(row[-1]))

    if power_values:
        max_value = max(power_values)
        print(
            "Maksymalna wartość w ostatniej kolumnie dla wybranych wierszy:", max_value
        )
    else:
        print("Brak wierszy spełniających kryteria.")


def plot_multiple_patterns_from_csv(file, patterns, horizontal_range=(45, 135)):
    df = pd.read_csv(
        file,
        sep=";",
        header=None,
        names=["horizontal", "vertical", "pattern", "freq", "power"],
    )
    vertical = []
    for pattern in patterns:
        df_pattern = df[
            (df["pattern"] == pattern[0])
            & (df["horizontal"] >= horizontal_range[0])
            & (df["horizontal"] <= horizontal_range[1])
        ]
        heatmap_data = df_pattern.pivot_table(
            index="vertical", columns="horizontal", values="power"
        )
        plt.figure(figsize=(11, 10))
        # sns.set(font_scale=1.2)  # Set the font scale for seaborn heatmap
        ax = sns.heatmap(
            heatmap_data,
            vmax=-30,
            vmin=-100,
            cbar_kws={"label": "Received power [dBm]"},
            cmap="coolwarm",  # viridis - oryginalna paleta kolorów
            annot=False,
            fmt=".2g",
        )
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(labelsize=14)  # Font size of colorbar numbers
        cbar.ax.yaxis.label.set_size(18)  # Font size of colorbar label cbar_kws
        ax.invert_yaxis()
        distance = "1.5"
        add = ""
        plt.title(f"Patern {pattern[1]} on {distance}m {add}", fontsize=22)
        # plt.title(f'Heatmap for pattern {pattern} on {distance}m', fontsize=22)
        plt.xlabel("Azimuth angle [°]", fontsize=18)
        plt.ylabel("Elevation angle [°]", fontsize=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(
            f"heatmap_pattern_{pattern[1]}_dist_{distance}m_{add}.jpg",
            format="jpg",
            bbox_inches="tight",
        )
        # plt.show()
        plt.close()


file_path = r"DANE_Z_POMIAROW/ComCom_01_2024/charakterystyka_3D_komora_PIT/12_08_ch_ka_3D_horizontal_5_5Ghz_2m_komora.csv"
patterns = [(1, 1), (20, 2), (17, 3), (8, 4), (23, 5), (26, 6)]
plot_multiple_patterns_from_csv(file_path, patterns)
