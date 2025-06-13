import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib as mpl

# Ustaw Times New Roman jako domyślną czcionkę
mpl.rcParams["font.family"] = "Times New Roman"
mpl.rcParams["font.size"] = 14

# Lista ścieżek do plików wejściowych
input_files = [
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_dookolna.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112_90cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112cm_140cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_swunica_112_40cm.csv",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_suwnica_bez_skrzynii.csv",
]

# Lista folderów wyjściowych
output_folders = [
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/dookolna",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_90",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_140",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/112_40",
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica programy i wykresy/wykresy/bez_skrzynii",
]

# Ustawienia kolorów
vmin = -85
vmax = -45

# Przetwarzanie każdego pliku
for input_path, output_folder in zip(input_files, output_folders):
    # Upewnij się, że folder wyjściowy istnieje
    os.makedirs(output_folder, exist_ok=True)

    # Wczytaj dane
    df = pd.read_csv(
        input_path,
        sep=";",
        header=None,
        names=["Pattern", "Position", "Frequency", "Power"],
    )

    # Tworzenie heatmapy
    plt.figure(figsize=(10, 8))
    pivot = df.pivot(index="Pattern", columns="Position", values="Power")
    sns.heatmap(
        pivot, cmap="viridis", vmin=vmin, vmax=vmax, cbar_kws={"label": "Moc [dBm]"}
    )
    plt.title("Mapa cieplna mocy odebranej w zależności od wzorca i pozycji")
    plt.xlabel("Numer pozycji")
    plt.ylabel("Numer wzorca")
    plt.tight_layout()

    # Zapisz heatmapę
    heatmap_path = os.path.join(output_folder, "heatmapa_mocy.png")
    plt.savefig(heatmap_path, dpi=300)
    plt.close()

    print(f"Heatmapa zapisana jako: {heatmap_path}")
