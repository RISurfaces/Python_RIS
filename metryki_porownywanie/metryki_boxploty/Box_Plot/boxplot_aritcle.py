import os
import pandas as pd
import matplotlib.pyplot as plt


# Funkcja do tworzenia subplotów wykresów pudełkowych
# Funkcja do tworzenia subplotów wykresów pudełkowych
def tworz_subploty_wykresow(plik_csv_lista, wybrane_patterny, folder_wynikowy):
    pattern_mapping = {1: 1, 20: 2, 17: 3, 8: 4, 23: 5, 26: 6}
    title = ["Distance 1 m", "Distance 1.5 m", "Distance 2 m"]
    grupy = [plik_csv_lista[i : i + 3] for i in range(0, len(plik_csv_lista), 3)]

    min_moc = float("inf")
    max_moc = float("-inf")

    for plik_csv in plik_csv_lista:
        kolumny = ["kąt1", "kąt2", "pattern", "częstotliwość", "moc"]
        df = pd.read_csv(plik_csv, delimiter=";", names=kolumny)
        df_wybrane = df[df["pattern"].isin(wybrane_patterny)]
        min_moc = min(min_moc, df_wybrane["moc"].min())
        max_moc = max(max_moc, df_wybrane["moc"].max())

    for indeks, grupa in enumerate(grupy):
        plt.figure(figsize=(18, 6))

        for i, plik_csv in enumerate(grupa):
            kolumny = ["kąt1", "kąt2", "pattern", "częstotliwość", "moc"]
            df = pd.read_csv(plik_csv, delimiter=";", names=kolumny)
            df_wybrane = df[df["pattern"].isin(wybrane_patterny)].copy()
            df_wybrane["pattern_custom"] = df_wybrane["pattern"].map(pattern_mapping)

            ax = plt.subplot(1, 3, i + 1)
            df_wybrane.boxplot(
                column="moc",
                by="pattern_custom",
                grid=True,
                patch_artist=True,
                ax=ax,
                flierprops=dict(marker="o", markerfacecolor="red", markersize=8),
                medianprops=dict(color="red", linewidth=2),
                showfliers=False,
            )

            for box in ax.artists:
                box.set_facecolor("blue")

            ax.set_ylim(-1, 30)
            ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.9)
            ax.minorticks_on()
            ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.7)

            ax.tick_params(axis="x", labelsize=18)
            ax.tick_params(axis="y", labelsize=18)

            ax.set_title(f"{title[i]}", fontsize=20)
            ax.set_xlabel("Pattern no.", fontsize=20)

            if i == 0:
                ax.set_ylabel(
                    "Absolute value of the power difference [dB]", fontsize=20
                )
            else:
                ax.set_ylabel("")

            plt.suptitle("", fontsize=16)

        nazwa_wykresu = f"group_{indeks + 1}.png"
        sciezka_zapisu = os.path.join(folder_wynikowy, nazwa_wykresu)
        os.makedirs(folder_wynikowy, exist_ok=True)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(sciezka_zapisu)
        plt.close()


# Ścieżki do plików CSV
plik_csv_lista = [
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_2m.csv",
]

# Folder wynikowy
folder_wynikowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/metryki_porownywanie/metryki_boxploty/box_plot_results_merge"

# Wybrane patterny
wybrane_patterny = [1, 20, 17, 8, 23, 26]

# Tworzenie subplotów wykresów dla grup plików CSV
tworz_subploty_wykresow(plik_csv_lista, wybrane_patterny, folder_wynikowy)
