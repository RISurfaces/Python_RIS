import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# ======= KONFIGURACJA =======
input_files = [
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

# Skala kolorów
vmin = -85
vmax = -45

# ======= PRZETWARZANIE =======
for input_file, output_folder in zip(input_files, output_folders):
    os.makedirs(output_folder, exist_ok=True)

    # Wczytaj dane
    df = pd.read_csv(
        input_file,
        sep=";",
        header=None,
        names=["Pattern", "Position", "Frequency", "Power"],
    )

    # Przekształć dane do siatki (meshgrid)
    pivot = df.pivot(index="Pattern", columns="Position", values="Power")
    X, Y = np.meshgrid(pivot.columns.values, pivot.index.values)
    Z = pivot.values

    # ======= WYKRES 3D Z POWIERZCHNIĄ =======
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", vmin=vmin, vmax=vmax)
    ax.set_title("Płaszczyzna mocy odebranej")
    ax.set_xlabel("Pozycja")
    ax.set_ylabel("Wzorzec")
    ax.set_zlabel("Moc [dBm]")
    fig.colorbar(surf, label="Moc [dBm]")
    plt.tight_layout()

    # Zapisz wykres
    filename = (
        os.path.splitext(os.path.basename(input_file))[0] + "_3d_powierzchnia.png"
    )
    save_path = os.path.join(output_folder, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Wykres 3D zapisany jako: {save_path}")
