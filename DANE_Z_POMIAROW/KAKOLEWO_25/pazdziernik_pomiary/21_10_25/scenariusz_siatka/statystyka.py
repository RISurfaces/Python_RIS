import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# 🔧 Lista plików CSV do przetworzenia
file_list = [
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_1_H_8_7m_V_3_5m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_1_H_13_7m_V_1_2m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_2_H_8_7m_V_3m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_2_H_13_7m_V_2_5m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_3_H_8_7m_V_4_2m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_3_H_13_7m_V_3_2m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_4_H_8_7m_V_2m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_4_H_13_7m_V_2m.csv.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_5_H_8_7m_V_3m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_5_H_13_7m_V_1_7m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_6_H_8_7m_V_3m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_6_H_13_7m_V_3_5m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_7_H_8_7m_V_3_5m.csv.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_7_H_13_7m_V_1_9m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_8_H_8_7m_V_3m.csv.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_8_H_13_7m_V_2m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_9_H_8_7m_V_3_5m.csv",
    "C:\\Users\\d0437921\\Documents\\GitHub\\Python_RIS\\DANE_Z_POMIAROW\\KAKOLEWO_25\\pazdziernik_pomiary\\21_10_25\\scenariusz_siatka\\PKT_9_H_13_7m_V_3_2m.csv",
]


def process_files(file_list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "wykresy_statystyczne")
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Folder na wykresy: {output_dir}\n")

    for file_path in tqdm(file_list, desc="Przetwarzanie plików", unit="plik"):
        if not os.path.exists(file_path):
            print(f"\n❌ Plik {file_path} nie istnieje, pomijam.\n")
            continue

        try:
            # Wczytaj dane
            df = pd.read_csv(
                file_path,
                sep=";",
                header=None,
                names=["col1", "pattern", "freq", "power"],
            )

            # Statystyki
            stats_df = (
                df.groupby("pattern")["power"]
                .agg(["mean", "std"])
                .reset_index()
                .sort_values("pattern")
            )

            base_name = os.path.splitext(os.path.basename(file_path))[0]

            # --- BOX PLOT ---
            plt.figure(figsize=(16, 8))  # 🔹 szerszy i nie za wysoki
            box = plt.boxplot(
                [df[df["pattern"] == p]["power"] for p in stats_df["pattern"]],
                patch_artist=True,
                widths=0.5,
            )

            # 🔹 kolory i estetyka
            colors = [
                "#4A90E2" if i % 2 == 0 else "#F5A623" for i in range(len(box["boxes"]))
            ]
            for patch, color in zip(box["boxes"], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
                patch.set_edgecolor("black")

            plt.title(
                f"Boxplot mocy dla każdego patternu\n{base_name}", fontsize=13, pad=10
            )
            plt.xlabel("Numer patternu", fontsize=11)
            plt.ylabel("Moc [dBm]", fontsize=11)
            plt.ylim(-85, -50)
            plt.xticks(
                range(1, len(stats_df["pattern"]) + 1),
                stats_df["pattern"],
                rotation=90,
                fontsize=9,
            )
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.tight_layout(pad=2.0)

            plt.savefig(os.path.join(output_dir, f"{base_name}_boxplot.png"), dpi=250)
            plt.close()

            # --- ŚREDNIA + ODCHYLENIE ---
            plt.figure(figsize=(16, 8))
            plt.errorbar(
                stats_df["pattern"],
                stats_df["mean"],
                yerr=stats_df["std"],
                fmt="-o",
                color="royalblue",
                ecolor="red",
                capsize=4,
                elinewidth=1.3,
                markersize=5,
            )

            plt.title(
                f"Średnia moc i odchylenie standardowe\n{base_name}",
                fontsize=13,
                pad=10,
            )
            plt.xlabel("Numer patternu", fontsize=11)
            plt.ylabel("Moc [dBm]", fontsize=11)
            plt.ylim(-85, -50)
            plt.xticks(stats_df["pattern"], rotation=90, fontsize=9)
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.tight_layout(pad=2.0)

            plt.savefig(os.path.join(output_dir, f"{base_name}_mean_std.png"), dpi=250)
            plt.close()

        except Exception as e:
            print(f"\n⚠️ Błąd przy przetwarzaniu {file_path}: {e}\n")
            continue

    print("\n✅ Wszystkie pliki zostały przetworzone.")


if __name__ == "__main__":
    process_files(file_list)
