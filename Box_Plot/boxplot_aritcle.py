import os
import pandas as pd
import matplotlib.pyplot as plt


# Funkcja do tworzenia subplotów wykresów pudełkowych
def tworz_subploty_wykresow(plik_csv_lista, wybrane_patterny, folder_wynikowy):
    # Mapa, która przypisuje oryginalnym patternom (np. 1, 20, 17, 8, 22, 19)
    # nowe wartości w zakresie 1–6 (lub według potrzeb)
    pattern_mapping = {1: 1, 20: 2, 17: 3, 8: 4, 22: 5, 26: 6}

    # Podziel pliki na grupy po 3
    title = ["Distance 1 m", "Distance 1.5 m", "Distance 2 m"]
    grupy = [plik_csv_lista[i : i + 3] for i in range(0, len(plik_csv_lista), 3)]

    # Zmienna do przechowywania zakresu Y
    min_moc = float("inf")
    max_moc = float("-inf")

    # Najpierw obliczamy minimalną i maksymalną wartość dla mocy we wszystkich plikach
    for plik_csv in plik_csv_lista:
        kolumny = ["kąt1", "kąt2", "pattern", "częstotliwość", "moc"]
        df = pd.read_csv(plik_csv, delimiter=";", names=kolumny)

        # Wybierz tylko interesujące nas patterny
        df_wybrane = df[df["pattern"].isin(wybrane_patterny)]

        # Zaktualizuj zakres mocy
        min_moc = min(min_moc, df_wybrane["moc"].min())
        max_moc = max(max_moc, df_wybrane["moc"].max())

    # Teraz, gdy mamy zakres Y, możemy utworzyć wykresy
    for indeks, grupa in enumerate(grupy):
        plt.figure(figsize=(18, 6))

        for i, plik_csv in enumerate(grupa):
            # Wczytaj dane z pliku CSV
            kolumny = ["kąt1", "kąt2", "pattern", "częstotliwość", "moc"]
            df = pd.read_csv(plik_csv, delimiter=";", names=kolumny)

            # Wybierz tylko interesujące nas patterny
            df_wybrane = df[df["pattern"].isin(wybrane_patterny)].copy()

            # Dodaj kolumnę z "nową" numeracją patternów 1–6 (zamiast oryginalnych)
            df_wybrane["pattern_custom"] = df_wybrane["pattern"].map(pattern_mapping)

            # Dodaj wykres do odpowiedniego subplota
            ax = plt.subplot(1, 3, i + 1)
            df_wybrane.boxplot(
                column="moc",
                by="pattern_custom",  # klucz: korzystamy z nowo utworzonej kolumny
                grid=False,
                patch_artist=True,
                ax=ax,
                flierprops=dict(marker="o", markerfacecolor="red", markersize=8),
                medianprops=dict(color="red", linewidth=2),
                showfliers=False,
            )

            # Wypełnienie pudełek kolorem niebieskim
            for box in ax.artists:
                box.set_facecolor("blue")

            # Ustaw stałą skalę osi Y (dostosuj wg potrzeb)
            ax.set_ylim(-1, 30)

            # Dostosowanie czcionek
            ax.tick_params(axis="x", labelsize=18)  # Czcionka dla osi X
            ax.tick_params(axis="y", labelsize=18)  # Czcionka dla osi Y

            # Dostosowanie tytułów
            ax.set_title(f"{title[i]}", fontsize=18)
            ax.set_xlabel("Pattern no.", fontsize=18)  # Etykieta osi X

            # Dodaj opis osi Y tylko do pierwszego subplota
            if i == 0:
                ax.set_ylabel(
                    "Absolute value of the power difference [dB]", fontsize=18
                )
            else:
                ax.set_ylabel("")  # Usuń opis osi Y dla pozostałych subplotów

            # Usuwamy domyślny tytuł, który boxplot sam dodaje
            plt.suptitle("", fontsize=16)

        # Przygotowanie ścieżki zapisu
        nazwa_wykresu = f"group_{indeks + 1}.png"
        sciezka_zapisu = os.path.join(folder_wynikowy, nazwa_wykresu)

        # Zapisanie wykresu
        os.makedirs(folder_wynikowy, exist_ok=True)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(sciezka_zapisu)
        plt.close()


# Ścieżki do plików CSV
plik_csv_lista = [
    # r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_1m.csv",
    # r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_1_5m.csv",
    # r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_2m.csv",
    # Dodaj więcej ścieżek do plików CSV tutaj
]

# Folder wynikowy
folder_wynikowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/box_plot_results_merge"

# Wybrane patterny
wybrane_patterny = [1, 20, 17, 8, 22, 26]

# Tworzenie subplotów wykresów dla grup plików CSV
tworz_subploty_wykresow(plik_csv_lista, wybrane_patterny, folder_wynikowy)
