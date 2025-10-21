import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv


def maximum_val(file_path):
    power_values = []
    # Patterny, które sprawdzamy
    filter_values = {23,26}

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
    plt.rcParams["font.family"] = "Times New Roman"
    
    df = pd.read_csv(
        file,
        sep=";",
        header=None,
        names=["horizontal", "vertical", "pattern", "freq", "power"],
    )

    for pattern in patterns:
        df_pattern = df[
            (df["pattern"] == pattern)
            & (df["horizontal"] >= horizontal_range[0])
            & (df["horizontal"] <= horizontal_range[1])
        ]
        heatmap_data = df_pattern.pivot_table(
            index="vertical", columns="horizontal", values="power"
        )
        plt.figure(figsize=(11, 10))
        ax = sns.heatmap(
            heatmap_data,
            vmax=-50,
            vmin=-100,
            cbar_kws={"label": "Received power [dBm]"},
            cmap="coolwarm",
            annot=False,
            fmt=".2g",
        )
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(labelsize=14)  
        cbar.ax.yaxis.label.set_size(18)
        cbar.ax.yaxis.label.set_weight("bold")
        ax.invert_yaxis()


        # Pogrubione tytuły i etykiety
        plt.title(f"Heatmap for pattern 6 on 1m - anechoic chamber", fontsize=22, fontweight="bold")
        plt.xlabel("Azimuth angle [°]", fontsize=18, fontweight="bold")
        plt.ylabel("Elevation angle [°]", fontsize=18, fontweight="bold")
        plt.xticks(fontsize=14, fontweight="bold")
        plt.yticks(fontsize=14, fontweight="bold")
        

        # plt.savefig(
        #     f"heatmap_pattern_{pattern}_dist_{distance}m_.jpg",
        #     format="jpg",
        #     bbox_inches="tight",
        # )
        plt.show()
        plt.close()


file_path = r"C:\Users\brzak\Documents\GIT_Repository\Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\charakterystyka_3D_nowe_anteny_AINFO\28_10_3D_5_5Ghz_1m_new_ant.csv"
#patterns = [23] #pattern 5
patterns = [26] #pattern 6
plot_multiple_patterns_from_csv(file_path, patterns)
