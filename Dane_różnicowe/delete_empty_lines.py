import csv


def remove_empty_lines(input_file, output_file, delimiter=";"):
    """Usuwanie pustych linii z pliku CSV."""
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter=delimiter)
        rows = [
            row for row in reader if any(cell.strip() for cell in row)
        ]  # Filtrujemy puste wiersze

    with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=delimiter)
        writer.writerows(rows)


# Ścieżki plików
input_file = r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\24_10_3D_5_5Ghz_1_5m_new_ant.csv"
output_file = r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\24_10_3D_5_5Ghz_1_5m_new_ant_clear.csv"

# Wywołanie funkcji
remove_empty_lines(input_file, output_file)
