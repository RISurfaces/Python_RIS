import csv
from itertools import groupby


def custom_sort_key(row):
    """Funkcja generująca klucz głównego sortowania (pierwsze dwie kolumny)."""
    order = {-27: 0, -18: 1, -9: 2, 0: 3, 9: 4, 18: 5, 27: 6}
    # Konwertujemy wartości kolumn na liczby
    first_col = float(row[0])
    second_col = float(row[1])
    return (first_col, order.get(second_col, float("inf")))


def sort_csv(input_file, output_file, delimiter=";"):
    """Sortowanie pliku CSV zgodnie z trzema kryteriami"""
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter=delimiter)
        rows = list(reader)
        header = None
        if (
            not rows[0][0].replace(".", "", 1).isdigit()
        ):  # Jeśli pierwszy wiersz to nagłówek
            header = rows.pop(0)

        # Główne sortowanie według pierwszej i drugiej kolumny
        rows.sort(key=custom_sort_key)

        # Sortowanie trzeciej kolumny w grupach
        grouped_data = []
        for _, group in groupby(rows, key=custom_sort_key):
            group = list(group)
            # Sortowanie trzeciej kolumny jako cykliczne wartości
            group.sort(key=lambda row: int(row[2]))
            grouped_data.extend(group)

    # Zapis do pliku wyjściowego
    with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=delimiter)
        if header:  # Jeśli istnieje nagłówek, zapisz go
            writer.writerow(header)
        writer.writerows(grouped_data)


# Przykład użycia:
input_file = r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_swap.csv"  # Ścieżka do pliku wejściowego
output_file = r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_swap_sort.csv"  # Ścieżka do pliku wyjściowego

sort_csv(input_file, output_file)
