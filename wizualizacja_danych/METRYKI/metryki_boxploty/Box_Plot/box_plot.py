import os
import pandas as pd
import matplotlib.pyplot as plt


# Funkcja do tworzenia wykresów pudełkowych z plików CSV
def tworz_wykres_pudelkowy(plik_csv, wybrane_patterny, folder_wynikowy):
    # Wczytaj dane z pliku CSV
    kolumny = ["kąt1", "kąt2", "pattern", "częstotliwość", "moc"]
    df = pd.read_csv(plik_csv, delimiter=";", names=kolumny)

    # Wybierz tylko interesujące nas patterny
    df_wybrane = df[df["pattern"].isin(wybrane_patterny)]

    # Tworzymy wykres pudełkowy dla wybranych patternów
    plt.figure(figsize=(10, 6))
    ax = df_wybrane.boxplot(
        column="moc",
        by="pattern",
        grid=False,
        patch_artist=True,
        flierprops=dict(marker="o", markerfacecolor="red", markersize=8),
        medianprops=dict(color="red", linewidth=2),
    )

    # Wypełnienie pudełek kolorem niebieskim
    for box in ax.artists:
        box.set_facecolor("blue")

    ax.set_ylim(-5, 50)

    # Dostosowanie osi i tytułu
    plt.title("Box plot for patterns", fontsize=14)
    plt.xlabel("Pattern")
    plt.ylabel("absolute value of the power difference")
    plt.xticks(rotation=45)

    # Przygotowanie ścieżki zapisu
    nazwa_pliku = os.path.basename(plik_csv).replace(".csv", "")
    folder = os.path.basename(os.path.dirname(plik_csv))
    nazwa_wykresu = f"{folder}_{nazwa_pliku}.png"
    sciezka_zapisu = os.path.join(folder_wynikowy, nazwa_wykresu)

    # Zapisanie wykresu
    os.makedirs(folder_wynikowy, exist_ok=True)
    plt.tight_layout()
    plt.savefig(sciezka_zapisu)
    plt.close()


# Ścieżki do plików CSV
plik_csv_lista = [
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_komora/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_nowe_stare_anteny/wynik_2m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_1_5m.csv",
    r"/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Dane_różnicowe/results_stare_komora/wynik_2m.csv",
    # Dodaj więcej ścieżek do plików CSV tutaj
]

# Folder wynikowy
folder_wynikowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/box_plot_results"

# Wybrane patterny
wybrane_patterny = [1, 20, 17, 8, 22, 25]

# Tworzenie wykresów dla każdego pliku CSV
for plik_csv in plik_csv_lista:
    tworz_wykres_pudelkowy(plik_csv, wybrane_patterny, folder_wynikowy)
