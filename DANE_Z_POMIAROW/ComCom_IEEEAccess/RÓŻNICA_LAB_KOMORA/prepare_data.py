import pandas as pd
import os

file_pairs = [
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\13_06_ch_ka_3D_5_5Ghz_1m.csv",
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\13_08_3D_5_5Ghz_1m_chamber.csv",
    ),  # Para 1
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_swap_sort.csv",
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\13_08_3D_5_5Ghz_1_5m_chamber.csv",
    ),  # Para 2
    (
        r"D:\GitHub\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\06_06_ch_ka_3D_horizontal_5_5Ghz_2m.csv",
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

    # Wczytaj dane z plików do DataFrame, traktując je jako dane surowe (brak nagłówków)
    df1 = pd.read_csv(file1, delimiter=";", header=None)
    df2 = pd.read_csv(file2, delimiter=";", header=None)

    # Sprawdzanie kolumn w plikach (możesz to usunąć, jeśli nie chcesz wyświetlać)
    print(f"Kolumny w {file1}: {df1.columns.tolist()}")
    print(f"Kolumny w {file2}: {df2.columns.tolist()}")

    # Zakładamy, że kolumny w obu DataFrame'ach są takie same (w tej samej kolejności)
    # Dołącz 'power' do df2 jako 'power_2' (merge na wspólnych kolumnach)
    merged = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=("", "_2"))

    # Oblicz wartość bezwzględną różnicy w kolumnie 'power' (przyjmujemy, że 'power' jest w ostatniej kolumnie)
    merged[merged.columns[-1]] = abs(
        merged[merged.columns[-1]] - merged[merged.columns[-2]]
    )

    # Usuń dodatkową kolumnę 'power_2' (druga kopia kolumny 'power')
    final_df = merged.iloc[:, [0, 1, 2, 3, -1]]

    # Zapisz wynik do nowego pliku CSV
    final_df.to_csv(output_file, index=False, header=False, sep=";")

    print(f"Wynik zapisano w pliku {output_file}")
