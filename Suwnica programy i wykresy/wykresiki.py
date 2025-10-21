import pandas as pd
import matplotlib.pyplot as plt
import os

# Ścieżka folderu do zapisu wykresów – wpisz ją tutaj
output_folder = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica/wykresy/bez_skrzynii"  # <- ZMIEŃ TĘ ŚCIEŻKĘ NA WŁAŚCIWĄ

# Wczytaj dane z pliku CSV
filename = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_suwnica_bez_skrzynii.csv"
df = pd.read_csv(
    filename, sep=";", header=None, names=["Pattern", "Position", "Frequency", "Power"]
)

# Grupuj dane po kolumnie "Pattern"
grouped = df.groupby("Pattern")

# Utwórz folder, jeśli nie istnieje
os.makedirs(output_folder, exist_ok=True)

# Twórz i zapisuj wykresy
for pattern, group in grouped:
    plt.figure()
    plt.plot(group["Position"], group["Power"], marker="o")
    plt.title(f"Moc odebrana dla wzorca {pattern}")
    plt.xlabel("Numer pozycji pomiarowej")
    plt.ylabel("Moc odebrana [dBm]")
    plt.grid(True)
    plt.tight_layout()

    filepath = os.path.join(output_folder, f"pattern_{pattern}.png")
    plt.savefig(filepath)
    plt.close()

print(f"Wykresy zostały zapisane w folderze: {output_folder}")
