import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import os

# Ścieżka do folderu zapisu
output_folder = "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/Suwnica/wykresy/112_90"  # <- ZMIEŃ TĘ ŚCIEŻKĘ
os.makedirs(output_folder, exist_ok=True)

# Wczytaj dane
df = pd.read_csv(
    "/Users/pawelplaczkiewicz/Documents/Dokumenty – Mac mini (Paweł)/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024/suwnica_LAB_28_05_25/28_05_25_suwnica_112_90cm.csv",
    sep=";",
    header=None,
    names=["Pattern", "Position", "Frequency", "Power"],
)

# ====== HEATMAPA ======
plt.figure(figsize=(10, 8))
pivot = df.pivot(index="Pattern", columns="Position", values="Power")
sns.heatmap(pivot, cmap="viridis", cbar_kws={"label": "Moc [dBm]"})
plt.title("Mapa mocy odebranej (Pattern vs Position)")
plt.xlabel("Pozycja")
plt.ylabel("Wzorzec")
plt.tight_layout()
heatmap_path = os.path.join(output_folder, "heatmapa_mocy.png")
plt.savefig(heatmap_path, dpi=300)
plt.close()

# ====== WYKRES 3D ======
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
x = df["Position"]
y = df["Pattern"]
z = df["Power"]
sc = ax.scatter(x, y, z, c=z, cmap="viridis", marker="o")
ax.set_title("Wykres 3D mocy odebranej")
ax.set_xlabel("Pozycja")
ax.set_ylabel("Wzorzec")
ax.set_zlabel("Moc [dBm]")
fig.colorbar(sc, label="Moc [dBm]")
plt.tight_layout()
scatter3d_path = os.path.join(output_folder, "wykres_3d_mocy.png")
plt.savefig(scatter3d_path, dpi=300)
plt.close()

print(f"Heatmapa zapisana jako: {heatmap_path}")
print(f"Wykres 3D zapisany jako: {scatter3d_path}")
