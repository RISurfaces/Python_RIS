import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams

# Lista plików wejściowych i odpowiadających folderów wyjściowych
file_list = [
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_dookolna.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112_90cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112cm_140cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_swunica_112_40cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_suwnica_bez_skrzynii.csv",
]
output_folders = [
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/dookolna",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_90",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_140",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_40",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/bez_skrzynii",
]


# Parametry czcionki
font_properties = {
    "font.family": "Times New Roman",
    "font.size": 14,
    "font.weight": "bold",
}
rcParams.update(font_properties)

# Przetwarzanie każdego pliku
for filename, output_folder in zip(file_list, output_folders):
    # Upewnij się, że folder docelowy istnieje
    os.makedirs(output_folder, exist_ok=True)

    # Wczytaj dane
    df = pd.read_csv(
        filename,
        sep=";",
        header=None,
        names=["Pattern", "Position", "Frequency", "Power"],
    )

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

        min_row = subset.loc[subset["Power"].idxmin()]
        min_power.append(min_row["Power"])
        min_patterns.append(int(min_row["Pattern"]))

        max_row = subset.loc[subset["Power"].idxmax()]
        max_power.append(max_row["Power"])
        max_patterns.append(int(max_row["Pattern"]))

    # Tworzenie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(positions, min_power, marker="o", label="Moc minimalna")
    plt.plot(positions, max_power, marker="o", label="Moc maksymalna")

    # Opisy punktów
    for x, y, p in zip(positions, min_power, min_patterns):
        plt.text(
            x,
            y,
            str(p),
            ha="right",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="blue",
            fontname="Times New Roman",
        )

    for x, y, p in zip(positions, max_power, max_patterns):
        plt.text(
            x,
            y,
            str(p),
            ha="left",
            va="top",
            fontsize=10,
            fontweight="bold",
            color="red",
            fontname="Times New Roman",
        )

    # Oznaczenia i zapis
    plt.title("Minimalna i maksymalna moc", fontweight="bold")
    plt.xlabel("Numer pozycji", fontweight="bold")
    plt.ylabel("Moc odebrana [dBm]", fontweight="bold")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Zapis wykresu
    output_path = os.path.join(output_folder, "min_max_wykres.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Wykres zapisano jako: {output_path}")
