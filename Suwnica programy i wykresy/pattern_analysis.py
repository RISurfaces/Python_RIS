import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def analyze_patterns_combined(csv_files):
    """
    Analizuje wpływ każdego paternю na maksymalną moc w każdej pozycji.
    Uśrednia wyniki ze wszystkich plików.

    Args:
        csv_files: lista ścieżek do plików CSV
    """

    print(f"\n{'='*80}")
    print(f"Analiza połączonych plików (uśrednione wyniki):")
    print(f"{'='*80}\n")

    # Wczytaj wszystkie pliki
    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(
            csv_file,
            sep=";",
            header=None,
            names=["pattern", "position", "frequency", "power"],
        )
        dfs.append(df)
        print(f"  - {Path(csv_file).name}: {len(df)} pomiarów")

    print()

    # Funkcja do obliczenia maksymalnej mocy dla każdej pozycji przy danym zbiorze paternów
    def get_max_power_per_position_averaged(data_list, patterns_to_use):
        """Znajdź maksymalną (najbliższą 0) moc dla każdej pozycji, uśrednioną ze wszystkich plików"""
        max_powers = []
        for df in data_list:
            filtered = df[df["pattern"].isin(patterns_to_use)]
            max_power = filtered.groupby("position")[
                "power"
            ].max()  # max bo wartości są ujemne (-50 > -60)
            max_powers.append(max_power)
        # Uśrednij wyniki ze wszystkich plików dla każdej pozycji
        averaged = pd.concat(max_powers, axis=1).mean(axis=1)
        return averaged

    # Początkowy zbiór paternów (wszystkie 27)
    all_patterns = sorted(dfs[0]["pattern"].unique())

    # Przechowuj wyniki
    results = []
    max_power_baselines = get_max_power_per_position_averaged(dfs, all_patterns)
    baseline_avg = max_power_baselines.mean()

    print(f"Moc maksymalna dla każdej pozycji (wszystkie 27 paternów, uśredniona):")
    print(max_power_baselines)
    print(f"Średnia moc maksymalna: {baseline_avg:.2f} dB\n")

    results.append(
        {
            "num_patterns": 27,
            "patterns": all_patterns.copy(),
            "max_power_per_position": max_power_baselines.copy(),
            "avg_max_power": baseline_avg,
            "difference_from_baseline": 0.0,
        }
    )

    # Iteracyjnie usuwaj N najgorszych paternów (iteracja 1: usuwaj 1, iteracja 2: usuwaj 2, itd)
    print("--- Analiza wpływu liczby paternów na moc maksymalną ---\n")

    # Funkcja do oceny każdego paternю - jaka będzie moc po usunięciu
    def get_power_without_pattern(data_list, all_pats, pattern_idx):
        """Zwraca jaką moc będziesz mieć bez tego paternу"""
        patterns_without = [p for p in all_pats if p != pattern_idx]
        max_power_without = get_max_power_per_position_averaged(
            data_list, patterns_without
        )
        avg_without = max_power_without.mean()
        return avg_without

    # Ocena każdego paternю - cual będzie moc bez niego
    print("Ocenianie wpływu usunięcia każdego paternю...")
    pattern_qualities = {}
    for pattern in all_patterns:
        pattern_qualities[pattern] = get_power_without_pattern(
            dfs, all_patterns, pattern
        )

    # Sortuj paternów od najgorszych (gdzie bez nich moc jest najlepsza) do najlepszych
    # Najlepsze wartości (bliżej 0) to są te gdzie usunięcie paternю dało NAJLEPSZY wynik
    worst_patterns_sorted = sorted(
        pattern_qualities.items(), key=lambda x: x[1], reverse=True
    )
    print("Paternów posortowane - jak ich usuniesz, reszta będzie miała moc:")
    for i, (pattern, power) in enumerate(worst_patterns_sorted[:5]):
        print(f"  Bez paternю {pattern}: {power:.2f} dB")
    print()

    # Teraz iteracyjnie usuwaj N najgorszych
    print("Liczba pat | Pozostało | Moc [dB] | Różnica [dB] | Usunięte paternów")
    print("-----------|-----------|----------|--------------|------------------")

    for iteration in range(27):
        num_to_remove = iteration  # ile paternów usuwamy

        if num_to_remove == 0:
            # Iteracja 0: wszystkie paternы (już mamy w results)
            continue

        # Weź N najgorszych paternów (tych, gdzie usunięcie daje najlepszą moc)
        patterns_to_remove = [p for p, _ in worst_patterns_sorted[:num_to_remove]]
        remaining_patterns = [p for p in all_patterns if p not in patterns_to_remove]

        test_max_power = get_max_power_per_position_averaged(dfs, remaining_patterns)
        test_avg = test_max_power.mean()

        difference_from_baseline = test_avg - baseline_avg

        # Konwertuj numpy.int64 do int dla czytelności
        patterns_removed_str = ", ".join([str(int(p)) for p in patterns_to_remove])

        print(
            f"    {num_to_remove:2d}    |    {len(remaining_patterns):2d}    | {test_avg:8.2f} | {difference_from_baseline:10.4f} | {patterns_removed_str}"
        )

        # Zapisz wynik
        results.append(
            {
                "num_patterns": len(remaining_patterns),
                "patterns": remaining_patterns.copy(),
                "max_power_per_position": test_max_power.copy(),
                "avg_max_power": test_avg,
                "difference_from_baseline": difference_from_baseline,
            }
        )

    # Podsumowanie
    print(f"\n{'='*80}")
    print("PODSUMOWANIE ANALIZY")
    print(f"{'='*80}\n")

    print("| Liczba paternów | Średnia moc max | Różnica od baseline |")
    print("|-----------------|-----------------|---------------------|")
    for result in results:
        print(
            f"| {result['num_patterns']:15d} | {result['avg_max_power']:15.2f} | {result['difference_from_baseline']:19.4f} |"
        )

    # Rysowanie wykresu
    num_patterns_list = [r["num_patterns"] for r in results]
    differences_list = [r["difference_from_baseline"] for r in results]

    # Odwróć kolejność, aby była od 27 do 1
    num_patterns_list = num_patterns_list[::-1]
    differences_list = differences_list[::-1]

    plt.figure(figsize=(14, 8))
    plt.plot(
        num_patterns_list,
        differences_list,
        "o-",
        linewidth=2.5,
        markersize=8,
        color="#2E86AB",
    )

    plt.xlabel(
        "Number of patterns", fontsize=18, fontweight="bold", family="Times New Roman"
    )
    plt.ylabel(
        "Power difference [dB]",
        fontsize=18,
        fontweight="bold",
        family="Times New Roman",
    )
    plt.title(
        "Effect of number of patterns on maximum power",
        fontsize=20,
        fontweight="bold",
        family="Times New Roman",
    )

    plt.grid(True, alpha=0.3)
    plt.xlim(28, 0)  # Ustawiamy oś X od 28 (lewa) do 0 (prawa)
    plt.xticks(range(27, 0, -2), fontsize=14, family="Times New Roman")
    plt.yticks(fontsize=14, family="Times New Roman")

    # Zapisz wykres
    output_dir = Path(csv_files[0]).parent
    output_file = output_dir / "pattern_analysis_combined.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"\nWykres zapisany: {output_file}")

    plt.close()

    # Zapisz wyniki do pliku txt
    txt_output_file = output_dir / "pattern_analysis_results.txt"
    with open(txt_output_file, "w") as f:
        f.write("=" * 100 + "\n")
        f.write("ANALIZA WPŁYWU PATERNÓW NA MOKSYMALNĄ MOC\n")
        f.write("=" * 100 + "\n\n")

        f.write(
            f"Moc maksymalna dla każdej pozycji (wszystkie 27 paternów, uśredniona):\n"
        )
        f.write(str(max_power_baselines) + "\n")
        f.write(f"Średnia moc maksymalna: {baseline_avg:.2f} dB\n\n")

        f.write(
            "Liczba pat | Pozostało | Moc [dB] | Różnica [dB] | Usunięte paternów\n"
        )
        f.write("-" * 100 + "\n")

        for result in results[1:]:  # Pomijamy pierwszy (baseline)
            num_patterns = result["num_patterns"]
            avg_power = result["avg_max_power"]
            diff = result["difference_from_baseline"]
            patterns = result["patterns"]

            # Paternów usunięte to te które nie są w remaining_patterns
            removed = [p for p in all_patterns if p not in patterns]
            removed_str = ", ".join([str(int(p)) for p in sorted(removed)])

            num_removed = len(removed)
            f.write(
                f"    {num_removed:2d}    |    {num_patterns:2d}    | {avg_power:8.2f} | {diff:10.4f} | {removed_str}\n"
            )

        f.write("\n" + "=" * 100 + "\n")
        f.write("PODSUMOWANIE\n")
        f.write("=" * 100 + "\n")
        f.write("| Liczba paternów | Średnia moc max | Różnica od baseline |\n")
        f.write("|-----------------|-----------------|---------------------|\n")
        for result in results:
            f.write(
                f"| {result['num_patterns']:15d} | {result['avg_max_power']:15.2f} | {result['difference_from_baseline']:19.4f} |\n"
            )

    print(f"Wyniki zapisane: {txt_output_file}")

    return results


if __name__ == "__main__":
    # Analiza dla trzech plików
    csv_files = [
        "/Users/pawelplaczkiewicz/Documents/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024_KRIT2025_ESWA/suwnica_LAB_28_05_25/28_05_25_suwnica_112_90cm.csv",
        "/Users/pawelplaczkiewicz/Documents/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024_KRIT2025_ESWA/suwnica_LAB_28_05_25/28_05_25_suwnica_112cm_140cm.csv",
        "/Users/pawelplaczkiewicz/Documents/GitHub/Python_RIS/DANE_Z_POMIAROW/V2X_INFOCOM2024_KRIT2025_ESWA/suwnica_LAB_28_05_25/28_05_25_swunica_112_40cm.csv",
    ]

    valid_files = [f for f in csv_files if Path(f).exists()]
    if valid_files:
        analyze_patterns_combined(valid_files)
    else:
        print("Żaden plik nie znaleziony!")
