import pandas as pd
import os

# Definicja nazw kolumn (bez nagłówków w plikach)
column_names = ["vertical", "horizontal", "pattern", "freq", "power"]

# Definicja par plików do porównania
file_pairs = [
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\28_10_3D_5_5Ghz_1m_new_ant.csv",
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\13_08_3D_5_5Ghz_1m_chamber.csv",
    ),  # Para 1
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\24_10_3D_5_5Ghz_1_5m_new_ant_clear.csv",
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\13_08_3D_5_5Ghz_1_5m_chamber.csv",
    ),  # Para 2
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\27_10_3D_5_5Ghz_2m_new_ant.csv",
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\12_08_ch_ka_3D_horizontal_5_5Ghz_2m_komora.csv",
    ),
    # Dodaj kolejne pary plików, jeśli potrzeba
]

# Ścieżka do katalogu wyników
output_dir = (
    "./results/"  # Upewnij się, że katalog istnieje lub użyj os.makedirs(output_dir)
)

# Tworzenie katalogu, jeśli nie istnieje
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iteracja po parach plików
for i, (file1, file2) in enumerate(file_pairs, start=1):
    output_file = f"{output_dir}wynik_{i}.csv"  # Nazwa pliku wynikowego dla danej pary

    # Wczytaj dane z plików do DataFrame, używając zdefiniowanych nazw kolumn
    df1 = pd.read_csv(file1, delimiter=";", names=column_names, header=None)
    df2 = pd.read_csv(file2, delimiter=";", names=column_names, header=None)

    # Sprawdzanie kolumn w plikach
    print(f"Kolumny w {file1}: {df1.columns.tolist()}")
    print(f"Kolumny w {file2}: {df2.columns.tolist()}")

    # Dołącz 'power' do df2 jako 'power_2' (merge na wspólnych kolumnach)
    merged = pd.merge(
        df1, df2, on=["vertical", "horizontal", "pattern"], suffixes=("", "_2")
    )

    # Oblicz wartość bezwzględną różnicy w kolumnie 'power'
    merged["power"] = abs(merged["power"] - merged["power_2"])

    # Usuń dodatkową kolumnę 'power_2'
    final_df = merged[["vertical", "horizontal", "pattern", "freq", "power"]]

    # Zapisz wynik do nowego pliku CSV
    final_df.to_csv(output_file, index=False, sep=";")

    print(f"Wynik zapisano w pliku {output_file}")
