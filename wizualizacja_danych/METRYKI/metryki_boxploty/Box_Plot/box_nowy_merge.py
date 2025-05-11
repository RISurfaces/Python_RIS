import os
import pandas as pd
import matplotlib.pyplot as plt


def tworz_wykresy_zbiorcze(grupy_plikow, wybrane_patterny, folder_wynikowy):
    pattern_mapping = {1: 1, 20: 2, 17: 3, 8: 4, 23: 5, 26: 6}
    label_map = ["Distance 1 m", "Distance 1.5 m", "Distance 2 m"]
    suffix_map = ["nowe_stare", "stare_komora"]
    suptitle_map = [
        "Comparison between METIS and A-INFO antennas",
        "Comparison between laboratory and anechoic\nchamber",
    ]

    for idx, grupa in enumerate(grupy_plikow):
        fig, axs = plt.subplots(3, 1, figsize=(4.2, 8), constrained_layout=False)

        # Zwiększamy lewy margines i odstępy
        fig.subplots_adjust(left=0.26, top=0.90, bottom=0.06, hspace=0.4)

        for i, (plik_csv, ax) in enumerate(zip(grupa, axs)):
            df = pd.read_csv(
                plik_csv,
                delimiter=";",
                names=["kąt1", "kąt2", "pattern", "częstotliwość", "moc"],
            )
            df_wybrane = df[df["pattern"].isin(wybrane_patterny)].copy()
            df_wybrane["pattern_custom"] = df_wybrane["pattern"].map(pattern_mapping)

            df_wybrane.boxplot(
                column="moc",
                by="pattern_custom",
                grid=True,
                patch_artist=True,
                ax=ax,
                flierprops=dict(marker="o", markerfacecolor="red", markersize=6),
                medianprops=dict(color="red", linewidth=1.5),
                showfliers=False,
            )

            for box in ax.artists:
                box.set_facecolor("blue")

            ax.set_ylim(-1, 30)
            ax.set_yticks(range(0, 31, 5))
            ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.8)
            ax.minorticks_on()
            ax.grid(which="minor", linestyle=":", linewidth=0.4, alpha=0.6)

            ax.tick_params(axis="x", labelsize=9)
            ax.tick_params(axis="y", labelsize=9)
            ax.set_xlabel("Pattern no.", fontsize=10)
            ax.set_title(label_map[i], fontsize=10)
            ax.set_ylabel("")

        # Wspólny opis osi Y — ekstremalnie po lewej
        fig.text(
            0.005,
            0.5,
            "Absolute value of the power difference [dB]",
            va="center",
            rotation="vertical",
            fontsize=11,
        )

        # Tytuł ogólny
        fig.suptitle(suptitle_map[idx], fontsize=11)
        os.makedirs(folder_wynikowy, exist_ok=True)
        sciezka_zapisu = os.path.join(
            folder_wynikowy, f"combined_{suffix_map[idx]}.png"
        )
        fig.savefig(sciezka_zapisu, dpi=300)
        plt.close(fig)


# Ścieżki do plików CSV – grupy po 3 (dla 1m, 1_5m, 2m)
grupa_1 = [
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_nowe_stare_anteny/wynik_2m.csv",
]

grupa_2 = [
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/RÓŻNICA_LAB_KOMORA/results_stare_komora/wynik_2m.csv",
]

# Folder wynikowy
folder_wynikowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/ComCom_IEEEAccess/boxploty"

# Wybrane patterny
wybrane_patterny = [1, 20, 17, 8, 23, 26]

# Wywołanie
tworz_wykresy_zbiorcze([grupa_1, grupa_2], wybrane_patterny, folder_wynikowy)
