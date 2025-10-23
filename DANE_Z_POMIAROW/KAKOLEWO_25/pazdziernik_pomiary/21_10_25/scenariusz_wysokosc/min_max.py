import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# ================================
# 🔧 KONFIGURACJA
# ================================

FILES = [
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\10m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\20m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\30m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\40m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_wysokosc\\50m.csv",
]

OUTPUT_DIR = "wykresy"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "moc_min_max.png")

# ================================
# 📊 GŁÓWNY KOD
# ================================

# Utwórz folder, jeśli nie istnieje
os.makedirs(OUTPUT_DIR, exist_ok=True)

heights = []
max_powers = []
min_powers = []
max_patterns = []
min_patterns = []

print("📥 Wczytywanie danych i obliczanie mocy min/max...")

for file in tqdm(FILES, desc="Pliki", ncols=80):
    if not os.path.exists(file):
        print(f"⚠️  Plik {file} nie istnieje – pomijam.")
        continue

    try:
        height = int(os.path.basename(file).replace("m.csv", ""))
    except ValueError:
        print(f"⚠️  Nie można odczytać wysokości z nazwy: {file}")
        continue

    df = pd.read_csv(
        file, sep=";", header=None, names=["col1", "pattern", "freq", "power"]
    )

    # Znajdź min i max
    max_row = df.loc[df["power"].idxmax()]
    min_row = df.loc[df["power"].idxmin()]

    heights.append(height)
    max_powers.append(max_row["power"])
    min_powers.append(min_row["power"])
    max_patterns.append(int(max_row["pattern"]))
    min_patterns.append(int(min_row["pattern"]))

# ================================
# 📈 TWORZENIE WYKRESU
# ================================

plt.figure(figsize=(9, 6))

# Wykres mocy maksymalnej
plt.plot(heights, max_powers, marker="o", color="blue", label="Moc maksymalna")
for x, y, p in zip(heights, max_powers, max_patterns):
    plt.text(x, y + 0.5, f"{p}", color="blue", fontsize=9, ha="center")

# Wykres mocy minimalnej
plt.plot(heights, min_powers, marker="o", color="red", label="Moc minimalna")
for x, y, p in zip(heights, min_powers, min_patterns):
    plt.text(x, y - 1.0, f"{p}", color="red", fontsize=9, ha="center")

plt.xlabel("Wysokość [m]")
plt.ylabel("Moc odebrana [dBm]")
plt.title("Moc minimalna i maksymalna dla różnych wysokości")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Zapis wykresu
plt.savefig(OUTPUT_FILE, dpi=300)
plt.close()

print(f"\n✅ Wykres zapisano jako: {OUTPUT_FILE}")
