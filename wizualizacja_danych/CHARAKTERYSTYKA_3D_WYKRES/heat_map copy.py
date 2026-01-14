import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file):
    df = pd.read_csv(
        file, sep=";", header=None, names=["vertical", "horizontal", "freq", "power"]
    )
    df_patern = df[df[""] == 0]
    heatmap_data = df_.pivot_table(
        index="vertical", columns="horizontal", values="power"
    )
    plt.figure(figsize=(10, 7))
    sns.heatmap(
        heatmap_data,
        vmax=-50,
        vmin=-100,
        cmap="viridis",
        fmt=".2g",
    )
    plt.gca().invert_yaxis()
    plt.title(f"Heatmapa mocy dla paternu blacha")
    plt.xlabel("Kąt horizontal")
    plt.ylabel("Vertical")
    plt.savefig("heatmapa_patern_blacha.jpg", format="jpg")
    plt.show()


file_path = r"C:\Users\d0437922\Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\charakterystyka_3D_nowe_anteny_AINFO\27_10_3D_5_5Ghz_2m_new_ant.csv"
plot_multiple_patterns_from_csv(file_path)
