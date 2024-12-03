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
            bins=range(0, 40 + 2),
            color="blue",
            edgecolor="black",
            alpha=0.7,
        )
        plt.title(f"Histogram różnicy mocy odebranej dla patternu {numer_patternu}")
        plt.xlabel("Moc odebrana (zaokrąglona)")
        plt.ylabel("Liczba wystąpień")

        # Ustawienie stałej skali na osi Y
        plt.ylim(0, 80)

        # Ustawienie stałej skali na osi X
        plt.xlim(0, 40)

        # Ustawienie osi X co 5 jednostek
        plt.xticks(range(0, 40 + 1, 5))

        # Włączenie siatki na osi Y
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Zapisanie wykresu do pliku
        sciezka_wykresu = os.path.join(output_folder, f"{numer_patternu}.png")
        plt.savefig(sciezka_wykresu)
        plt.close()

    print(f'Wyniki dla pliku "{plik_csv}" zapisano w folderze "{output_folder}".')


# Lista plików CSV do przetworzenia
pliki_csv = [
    r"D:\GitHub\Python_RIS\Dane_różnicowe\results_nowe_komora\wynik_1_5m.csv",
    r"D:\GitHub\Python_RIS\Dane_różnicowe\results_nowe_komora\wynik_1m.csv",
    r"D:\GitHub\Python_RIS\Dane_różnicowe\results_nowe_komora\wynik_2m.csv",
]
# Przetwarzanie każdego pliku z listy
for plik_csv in pliki_csv:
    przetworz_plik_csv(plik_csv)
