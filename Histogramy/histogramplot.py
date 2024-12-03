import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def przetworz_plik_csv(plik_csv):
    # Pobierz nazwę pliku bez ścieżki i rozszerzenia
    nazwa_pliku = os.path.splitext(os.path.basename(plik_csv))[0]

    # Utwórz folder dla wyników tego pliku
    output_folder = os.path.join("wyniki", nazwa_pliku)
    os.makedirs(output_folder, exist_ok=True)

    # Wczytaj dane z pliku CSV
    kolumny = ["kat1", "kat2", "numer_patternu", "czestotliwosc", "moc_odebrana"]
    dane = pd.read_csv(plik_csv, sep=";", names=kolumny)

    # Konwersja kolumny 'kat1' na typ numeryczny
    dane["kat1"] = pd.to_numeric(dane["kat1"], errors="coerce")

    # Usunięcie wierszy, gdzie 'kat1' jest NaN (nienumeryczne wartości)
    dane.dropna(subset=["kat1"], inplace=True)

    # Filtrowanie danych tylko dla kątów w zakresie od 45 do 135
    dane = dane[(dane["kat1"] >= 45) & (dane["kat1"] <= 135)]

    # Zastąpienie wartości nienumerycznych (NaN, inf) w kolumnie 'moc_odebrana' wartością domyślną 0
    dane["moc_odebrana"] = pd.to_numeric(dane["moc_odebrana"], errors="coerce")
    dane["moc_odebrana"].fillna(0, inplace=True)

    # Zaokrąglenie wartości mocy odebranej do wartości całkowitych
    dane["moc_odebrana_zaokraglona"] = dane["moc_odebrana"].round().astype(int)

    # Grupowanie danych po numerze patternu
    grupy = dane.groupby("numer_patternu")

    # Tworzenie histogramów dla każdej grupy
    for numer_patternu, grupa in grupy:
        plt.figure(figsize=(10, 6))

        # Ustawienie histogramu z dokładnymi wynikami (kwant=1)
        plt.hist(
            grupa["moc_odebrana_zaokraglona"],
            bins=range(-100, -30 + 2),
            color="blue",
            edgecolor="black",
            alpha=0.7,
        )
        plt.title(f"Histogram mocy odebranej dla patternu {numer_patternu}")
        plt.xlabel("Moc odebrana (zaokrąglona)")
        plt.ylabel("Liczba wystąpień")

        # Ustawienie stałej skali na osi Y
        plt.ylim(0, 150)

        # Ustawienie stałej skali na osi X
        plt.xlim(-100, -30)

        # Ustawienie osi X co 5 jednostek
        plt.xticks(range(-100, -30 + 1, 5))

        # Włączenie siatki na osi Y
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Zapisanie wykresu do pliku
        sciezka_wykresu = os.path.join(output_folder, f"{numer_patternu}.png")
        plt.savefig(sciezka_wykresu)
        plt.close()

    print(f'Wyniki dla pliku "{plik_csv}" zapisano w folderze "{output_folder}".')


# Lista plików CSV do przetworzenia
pliki_csv = [
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_nowe_anteny_AINFO/28_10_3D_5_5Ghz_1m_new_ant.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_nowe_anteny_AINFO/24_10_3D_5_5Ghz_1_5m_new_ant.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_nowe_anteny_AINFO/27_10_3D_5_5Ghz_2m_new_ant.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_komora_PIT/13_08_3D_5_5Ghz_1m_chamber.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_komora_PIT/13_08_3D_5_5Ghz_1_5m_chamber.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_komora_PIT/12_08_ch_ka_3D_horizontal_5_5Ghz_2m_komora.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/13_06_ch_ka_3D_5_5Ghz_1m.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_swap.csv",
    r"/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/06_06_ch_ka_3D_horizontal_5_5Ghz_2m.csv",
]
# Przetwarzanie każdego pliku z listy
for plik_csv in pliki_csv:
    przetworz_plik_csv(plik_csv)
