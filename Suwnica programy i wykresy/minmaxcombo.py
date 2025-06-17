import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams

# Czcionka: Times New Roman, bold
rcParams.update(
    {"font.family": "Times New Roman", "font.size": 14, "font.weight": "bold"}
)

# Lista plików CSV
file_list = [
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_dookolna.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112cm_140cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112_90cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_swunica_112_40cm.csv",
]

# Tytuły subplotów
subplot_titles = ["TX w P3 (antena dookólna)", "TX w P1", "TX w P2", "TX w P3"]

# Folder zapisu
output_folder = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy"
os.makedirs(output_folder, exist_ok=True)

# Przygotowanie figury
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
# fig.suptitle("Minimalna i maksymalna", fontsize=20, fontweight="bold")

# Iteracja po plikach i osiach
for idx, (filename, title) in enumerate(zip(file_list, subplot_titles)):
    df = pd.read_csv(
        filename,
        sep=";",
        header=None,
        names=["Pattern", "Position", "Frequency", "Power"],
    )
    positions = sorted(df["Position"].unique())

    min_power = []
    max_power = []
    min_patterns = []
    max_patterns = []

    for pos in positions:
        subset = df[df["Position"] == pos]
        min_row = subset.loc[subset["Power"].idxmin()]
        max_row = subset.loc[subset["Power"].idxmax()]
        min_power.append(min_row["Power"])
        max_power.append(max_row["Power"])
        min_patterns.append(int(min_row["Pattern"]))
        max_patterns.append(int(max_row["Pattern"]))

    ax = axs[idx // 2][idx % 2]
    ax.plot(positions, min_power, marker="o", label="Moc minimalna")
    ax.plot(positions, max_power, marker="o", label="Moc maksymalna")

    for x, y, p in zip(positions, min_power, min_patterns):
        ax.text(
            x,
            y,
            str(p),
            ha="right",
            va="bottom",
            fontsize=14,
            fontweight="bold",
            color="blue",
            fontname="Times New Roman",
        )

    for x, y, p in zip(positions, max_power, max_patterns):
        ax.text(
            x,
            y,
            str(p),
            ha="left",
            va="top",
            fontsize=14,
            fontweight="bold",
            color="red",
            fontname="Times New Roman",
        )

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Numer pozycji", fontweight="bold")
    ax.set_ylabel("Moc odebrana [dBm]", fontweight="bold")
    ax.grid(True)
    ax.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Dla miejsca na tytuł główny
output_path = os.path.join(output_folder, "min_max_wykres_zbiorczy.png")
plt.savefig(output_path)
plt.close()

print(f"Wykres zbiorczy zapisano jako: {output_path}")
