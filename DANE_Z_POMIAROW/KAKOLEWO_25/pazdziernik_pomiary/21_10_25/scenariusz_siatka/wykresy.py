import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# 🔧 Lista plików CSV do przetworzenia
file_list = [
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_1_H_8_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_1_H_13_7m_V_1_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_2_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_2_H_13_7m_V_2_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_3_H_8_7m_V_4_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_3_H_13_7m_V_3_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_4_H_8_7m_V_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_4_H_13_7m_V_2m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_5_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_5_H_13_7m_V_1_7m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_6_H_8_7m_V_3m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_6_H_13_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_7_H_8_7m_V_3_5m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_7_H_13_7m_V_1_9m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_8_H_8_7m_V_3m.csv.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_8_H_13_7m_V_2m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_9_H_8_7m_V_3_5m.csv",
    "DANE_Z_POMIAROW/KAKOLEWO_25/pazdziernik_pomiary/21_10_25/scenariusz_siatka/PKT_9_H_13_7m_V_3_2m.csv",
]


def process_files(file_list):
    # 🔹 Folder "wykresy" obok pliku .py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "wykresy")
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Folder na wykresy: {output_dir}\n")

    # 🔹 Pasek postępu
    for file_path in tqdm(file_list, desc="Przetwarzanie plików", unit="plik"):
        if not os.path.exists(file_path):
            print(f"\n❌ Plik {file_path} nie istnieje, pomijam.\n")
            continue

        try:
            # Wczytanie danych
            df = pd.read_csv(
                file_path,
                sep=";",
                header=None,
                names=["col1", "pattern", "freq", "power"],
            )
            avg_df = df.groupby("pattern", as_index=False)["power"].mean()

            # Zapis średnich do CSV
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            avg_file = os.path.join(output_dir, f"{base_name}_avg.csv")
            avg_df.to_csv(
                avg_file, sep=";", index=False, header=["pattern", "avg_power"]
            )

            # 🔹 Tworzenie wykresu punktowego (bez linii)
            plt.figure(figsize=(14, 8))

            # Kolory naprzemienne (np. niebieski i pomarańczowy)
            colors = [
                "royalblue" if i % 2 == 0 else "darkorange" for i in range(len(avg_df))
            ]

            plt.scatter(
                avg_df["pattern"],
                avg_df["power"],
                c=colors,
                s=60,
                edgecolor="black",
                linewidth=0.6,
            )

            plt.title(f"Średnia moc dla każdego patternu\n{base_name}", fontsize=14)
            plt.xlabel("Numer patternu", fontsize=12)
            plt.ylabel("Średnia moc [dBm]", fontsize=12)

            # 🔹 Skala jednakowa dla wszystkich wykresów
            plt.ylim(-85, -55)

            # 🔹 Pokazanie wszystkich numerów patternów na osi X
            plt.xticks(avg_df["pattern"], rotation=90)
            plt.grid(True, which="both", axis="both", linestyle="--", alpha=0.6)
            plt.minorticks_on()

            # 🔹 Pionowe linie dla każdego patternu
            for x in avg_df["pattern"]:
                plt.axvline(x=x, color="gray", linestyle=":", alpha=0.3)

            plt.tight_layout()

            # 🔹 Zapis wykresu
            plot_file = os.path.join(output_dir, f"{base_name}_avg.png")
            plt.savefig(plot_file, bbox_inches="tight", dpi=200)
            plt.close()

        except Exception as e:
            print(f"\n⚠️ Błąd przy przetwarzaniu {file_path}: {e}\n")
            continue

    print("\n✅ Wszystkie pliki zostały przetworzone.")


# 🔥 Uruchomienie
if __name__ == "__main__":
    process_files(file_list)
