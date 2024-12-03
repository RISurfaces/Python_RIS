import csv


def swap_columns_in_csv(input_file, output_file):
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter=";")
        rows = [row for row in reader]

    # Zamiana kolumn 1 i 2
    for row in rows:
        if len(row) >= 2:  # Upewnij się, że są przynajmniej dwie kolumny
            row[0], row[1] = row[1], row[0]

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


# Użycie funkcji
input_csv = "/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero.csv"
output_csv = "/Users/pawelplaczkiewicz/Documents/RIS_GitHub/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_swap.csv"

swap_columns_in_csv(input_csv, output_csv)

print(f"Zamieniono kolumnę 1 z kolumną 2. Wynik zapisano w {output_csv}.")
