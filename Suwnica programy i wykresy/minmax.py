import pandas as pd
import matplotlib.pyplot as plt
import os

# Ścieżka folderu do zapisu wykresów
output_folder = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica/wykresy/112_140"  # <- ZMIEŃ TĘ ŚCIEŻKĘ

# Wczytaj dane z pliku CSV
filename = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112cm_140cm.csv"
df = pd.read_csv(
    filename, sep=";", header=None, names=["Pattern", "Position", "Frequency", "Power"]
)

# Upewnij się, że folder docelowy istnieje
os.makedirs(output_folder, exist_ok=True)

# Unikalne pozycje pomiarowe
positions = sorted(df["Position"].unique())

# Listy do wykresu
min_power = []
max_power = []
min_patterns = []
max_patterns = []

# Znajdź min i max dla każdej pozycji
for pos in positions:
    subset = df[df["Position"] == pos]

    # Wiersz z najmniejszą mocą
    min_row = subset.loc[subset["Power"].idxmin()]
    min_power.append(min_row["Power"])
    min_patterns.append(int(min_row["Pattern"]))

    # Wiersz z największą mocą
    max_row = subset.loc[subset["Power"].idxmax()]
    max_power.append(max_row["Power"])
    max_patterns.append(int(max_row["Pattern"]))

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(positions, min_power, marker="o", label="Moc minimalna")
plt.plot(positions, max_power, marker="o", label="Moc maksymalna")

# Dodaj opisy z numerami wzorców
for x, y, p in zip(positions, min_power, min_patterns):
    plt.text(x, y, str(p), ha="right", va="bottom", fontsize=8, color="blue")

for x, y, p in zip(positions, max_power, max_patterns):
    plt.text(x, y, str(p), ha="left", va="top", fontsize=8, color="red")

# Oznaczenia i zapis
plt.title("Minimalna i maksymalna moc dla każdej pozycji")
plt.xlabel("Numer pozycji pomiarowej")
plt.ylabel("Moc odebrana [dBm]")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Zapis wykresu
output_path = os.path.join(output_folder, "min_max_wykres.png")
plt.savefig(output_path)
plt.close()

print(f"Wykres zapisano jako: {output_path}")
