import pandas as pd
import matplotlib.pyplot as plt
import os

# Ścieżki plików
plik_csv = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/wyniki_jeden_RIS/jeden_RIS_RSU/22_04_pomiar_RSU_MAXHold.csv"
folder_docelowy = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/wykresy"
nazwa_pliku = "RSU_MAXHold.png"
os.makedirs(folder_docelowy, exist_ok=True)
pelna_sciezka = os.path.join(folder_docelowy, nazwa_pliku)

# Wczytaj dane
df = pd.read_csv(
    plik_csv,
    sep=";",
    header=None,
    names=["pattern", "timestamp", "x", "y", "unknown", "power"],
)

# Dodaj kolumnę z numerem porządkowym
df["index"] = range(1, len(df) + 1)

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(df["index"], df["power"], color="blue", linestyle="-", marker="o")

# Dodaj etykiety patternów do każdego punktu
for idx, row in df.iterrows():
    plt.text(
        row["index"],
        row["power"],
        str(row["pattern"]),
        fontsize=8,
        ha="right",
        va="bottom",
    )


plt.xlabel("Numer porządkowy pomiaru")
plt.ylabel("Moc odebrana [dBm]")
plt.title("Moc odebrana względem kolejności pomiaru")
plt.grid(True)
plt.tight_layout()
plt.savefig(pelna_sciezka, dpi=300)
plt.close()

print(f"Wykres zapisano do: {pelna_sciezka}")
