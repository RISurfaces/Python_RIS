import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# ================================
# 🔧 KONFIGURACJA
# ================================

# Ręcznie zdefiniowana lista plików CSV (możesz dodać lub zmienić)
FILES = [
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\10m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\20m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\30m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\40m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\50m.csv",
]

# Folder, do którego zapiszą się wykresy
OUTPUT_DIR = "wykresy"

# ================================
# 📊 GŁÓWNY KOD
# ================================

# Utwórz folder, jeśli nie istnieje
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Słownik: pattern -> dane
data = {}

print("📥 Wczytywanie danych z plików...")
for file in tqdm(FILES, desc="Pliki", ncols=80):
    if not os.path.exists(file):
        print(f"⚠️  Plik {file} nie istnieje – pomijam.")
        continue

    # Wyciągnięcie wysokości z nazwy pliku, np. 10m.csv -> 10
    try:
        height = int(os.path.basename(file).replace("m.csv", ""))
    except ValueError:
        print(f"⚠️  Nie można odczytać wysokości z nazwy: {file}")
        continue

    # Wczytaj dane CSV
    try:
        df = pd.read_csv(
            file, sep=";", header=None, names=["col1", "pattern", "freq", "power"]
        )
    except Exception as e:
        print(f"❌ Błąd wczytywania {file}: {e}")
        continue

    # Iteruj po wierszach i zapisuj dane do słownika
    for _, row in df.iterrows():
        pattern = int(row["pattern"])
        power = float(row["power"])

        if pattern not in data:
            data[pattern] = {"height": [], "power": []}

        data[pattern]["height"].append(height)
        data[pattern]["power"].append(power)

# ================================
# 📈 GENEROWANIE WYKRESÓW
# ================================

print("📊 Generowanie i zapisywanie wykresów...")
for pattern in tqdm(sorted(data.keys()), desc="Wykresy", ncols=80):
    plt.figure(figsize=(8, 5))
    plt.plot(data[pattern]["height"], data[pattern]["power"], marker="o", color="blue")
    plt.title(f"Pattern {pattern}")
    plt.xlabel("Wysokość [m]")
    plt.ylabel("Moc odebrana [dBm]")
    plt.grid(True)

    # Zapis wykresu
    out_path = os.path.join(OUTPUT_DIR, f"pattern_{pattern}.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

print(f"\n✅ Zapisano {len(data)} wykresów w folderze: '{OUTPUT_DIR}'")
