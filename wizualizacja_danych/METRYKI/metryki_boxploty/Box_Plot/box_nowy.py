import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"


def tworz_osobne_wykresy(plik_csv_lista, wybrane_patterny, folder_wynikowy):
    pattern_mapping = {1: 1, 20: 2, 17: 3, 8: 4, 23: 5, 26: 6}
    distance_label_map = {"1m": "1m", "1_5m": "1.5m", "2m": "2m"}

    min_moc = float("inf")
    max_moc = float("-inf")

    for plik_csv in plik_csv_lista:
        df = pd.read_csv(
            plik_csv,
            delimiter=";",
            names=["kąt1", "kąt2", "pattern", "częstotliwość", "moc"],
        )
        df_wybrane = df[df["pattern"].isin(wybrane_patterny)]
        min_moc = min(min_moc, df_wybrane["moc"].min())
        max_moc = max(max_moc, df_wybrane["moc"].max())

    for i, plik_csv in enumerate(plik_csv_lista):
        df = pd.read_csv(
            plik_csv,
            delimiter=";",
            names=["kąt1", "kąt2", "pattern", "częstotliwość", "moc"],
        )
        df_wybrane = df[df["pattern"].isin(wybrane_patterny)].copy()
        df_wybrane["pattern_custom"] = df_wybrane["pattern"].map(pattern_mapping)

        plt.figure(figsize=(15, 10))
        ax = df_wybrane.boxplot(
            column="moc",
            by="pattern_custom",
            grid=True,
            patch_artist=True,
            flierprops=dict(marker="o", markerfacecolor="red", markersize=8),
            medianprops=dict(color="red", linewidth=2),
            showfliers=False,
        )

        # Usunięcie automatycznego tytułu „Boxplot grouped by...”
        plt.suptitle("")

        for box in ax.artists:
            box.set_facecolor("blue")

        ax.set_ylim(-1, 30)
        ax.set_yticks(range(0, 31, 5))
        ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.9)
        ax.minorticks_on()
        ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.7)

        ax.tick_params(axis="x", labelsize=10)
        ax.tick_params(axis="y", labelsize=10)
        ax.set_xlabel("Pattern no.", fontsize=14)
        ax.set_ylabel("Absolute value of the power difference [dB]", fontsize=14)

        tytul = "Power Boxplot"
        for klucz, wartosc in distance_label_map.items():
            if klucz in plik_csv:
                if i < 3:
                    tytul = f"Comparison between METIS and A-INFO antennas\nat a distance of {wartosc}"
                else:
                    tytul = f"Comparison between laboratory and anechoic chamber\nat a distance of {wartosc}"
                break

        plt.title(tytul, fontsize=16)

        if i < 3:
            suffix = "nowe_stare"
        else:
            suffix = "stare_komora"

        if "1_5m" in plik_csv:
            nazwa = f"1_5m_{suffix}.png"
        elif "2m" in plik_csv:
            nazwa = f"2m_{suffix}.png"
        elif "1m" in plik_csv:
            nazwa = f"1m_{suffix}.png"
        else:
            nazwa = f"wykres_{i+1}_{suffix}.png"

        sciezka_zapisu = os.path.join(folder_wynikowy, nazwa)
        os.makedirs(folder_wynikowy, exist_ok=True)

        plt.tight_layout(rect=[0, 0, 1, 1])
        plt.savefig(sciezka_zapisu, dpi=300, bbox_inches="tight")
        plt.close()


# Ścieżki do plików CSV
plik_csv_lista = [
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_2m.csv",
]

# Folder wynikowy
folder_wynikowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/boxploty"

# Wybrane patterny
wybrane_patterny = [1, 20, 17, 8, 23, 26]

# Wywołanie
tworz_osobne_wykresy(plik_csv_lista, wybrane_patterny, folder_wynikowy)
