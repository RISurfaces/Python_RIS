"""
=============================================================================
ESWA - Complete RIS Performance Analysis (6 Figures)
=============================================================================

Script generates 6 figures for ESWA publication:

FIGURE 1: Scenario A - Basic Pattern Comparison
    Comparison of received power for:
    - Maximum (best pattern at each point)
    - Minimum (worst pattern at each point)
    - Pattern 10 (fixed pattern #10)
    - Pattern 20 (fixed pattern #20)

FIGURE 2: TOP-K by Average Selection
    Comparison of pattern selection strategies (average method):
    - Maximum (all 27 patterns)
    - Best of TOP-7 avg patterns (TOP-7 by average power)
    - Best of TOP-10 avg patterns (TOP-10 by average power)
    Simple method: rank patterns by average → select K best.

FIGURE 3: Degradation vs Pattern Count (Brute-Force)
    Performance degradation as a function of pattern count (N = 1..27).
    For each N, the optimal set maximizing total RSRP across all points
    is found via brute-force search.

FIGURE 4: Degradation vs Pattern Count (Greedy Heuristic)
    Performance degradation as a function of pattern count (N = 1..27).
    Uses greedy backward elimination heuristic: iteratively removes
    the pattern whose removal causes the smallest degradation in
    average best-case power (AvgBestCase). Ties broken randomly.

FIGURE 5: Optimal K Patterns Degradation
    Shows power degradation for optimal K-pattern sets:
    - Maximum (all 27 patterns)
    - Optimal K patterns for K ∈ {8, 5, 4, 3, 2, 1}
    K=8 is minimum without degradation, others show increasing degradation.

FIGURE 6: Degradation Comparison (Brute-Force vs Greedy)
    Direct comparison of both methods on the same plot:
    - Brute-force optimal (blue)
    - Greedy heuristic (orange)
    Shows how close the greedy heuristic approximates the optimal solution.

=============================================================================
Author: Marcel
Date: 2026-02-02
=============================================================================
"""

import os
import re
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import comb
from numba import njit
from tqdm import tqdm

# =============================================================================
# CONFIGURATION
# =============================================================================
INPUT_FOLDER = "jeden_ris_wyniki"
OUTPUT_FOLDER = "jeden_ris_wyniki"
RESULTS_JSON = os.path.join(OUTPUT_FOLDER, "degradation_results.json")

POINT_MIN = 4
POINT_MAX = 22
PATTERN_10 = 10
PATTERN_20 = 20
K_VALUES = [8, 7, 6, 5, 4]  # for Figure 2
DEGRADATION_THRESHOLD = 0.05  # dB - for Figure 4

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def extract_point_number(file_name):
    """Extracts measurement point number from filename (e.g., 'dane_5.csv' -> 5)."""
    m = re.search(r"_(\d+)\.csv$", file_name)
    return int(m.group(1)) if m else None


def load_all_points(folder):
    """Loads all CSV files and combines them into a DataFrame."""
    rows = []
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".csv"):
            continue
        pt = extract_point_number(f)
        if pt is None:
            continue
        df = pd.read_csv(
            os.path.join(folder, f),
            sep=";",
            header=None,
            names=["Pattern", "Timestamp", "Frequency", "Power"],
        )
        df["Point"] = pt
        rows.append(df)
    return pd.concat(rows, ignore_index=True)


def label_offset_max(y_prev, y_curr, y_next, offset=0.8):
    """Calculates offset for maximum label (avoids overlapping)."""
    if y_prev is not None and y_next is not None:
        if y_curr > y_prev and y_curr > y_next:
            return offset, "bottom"
    if y_prev is not None and y_curr < y_prev:
        return offset, "bottom"
    return -offset, "top"


def label_offset_min(y_prev, y_curr, y_next, offset=0.8):
    """Calculates offset for minimum label (avoids overlapping)."""
    if y_prev is not None and y_next is not None:
        if y_curr < y_prev and y_curr < y_next:
            return -offset, "top"
    if y_prev is not None and y_curr < y_prev:
        return -offset, "top"
    return offset, "bottom"


# =============================================================================
# NUMBA FUNCTIONS (Brute-force optimization)
# =============================================================================
@njit(cache=True)
def next_combination(indices, n):
    """Generates next combination in lexicographic order."""
    k = len(indices)
    for i in range(k - 1, -1, -1):
        if indices[i] < n - k + i:
            indices[i] += 1
            for j in range(i + 1, k):
                indices[j] = indices[j - 1] + 1
            return True
    return False


@njit(cache=True)
def compute_combo_sum(rsrp_matrix, indices):
    """
    Computes RSRP sum for a pattern combination.
    For each measurement point, takes max RSRP among selected patterns.
    """
    n_points = rsrp_matrix.shape[1]
    total = 0.0
    for pt in range(n_points):
        max_val = -1e30
        for idx in indices:
            if rsrp_matrix[idx, pt] > max_val:
                max_val = rsrp_matrix[idx, pt]
        total += max_val
    return total


@njit(cache=True)
def find_best_combo(rsrp_matrix, n_patterns, k):
    """
    Finds optimal k-pattern set maximizing RSRP sum.
    Searches all C(n_patterns, k) combinations.

    Returns:
        (best_sum, best_combo): maximum sum and list of pattern indices
    """
    indices = np.arange(k, dtype=np.int64)
    best_sum = compute_combo_sum(rsrp_matrix, indices)
    best_combo = indices.copy()

    while next_combination(indices, n_patterns):
        current_sum = compute_combo_sum(rsrp_matrix, indices)
        if current_sum > best_sum:
            best_sum = current_sum
            best_combo = indices.copy()

    return best_sum, best_combo


# =============================================================================
# FIGURE 1: SCENARIO A - Basic Pattern Comparison
# =============================================================================
def generate_figure1(data, output_folder):
    """
    Plot comparing maximum, minimum, and fixed patterns 10 and 20.
    """
    print("\n" + "=" * 70)
    print("FIGURE 1: SCENARIO A - BASIC PATTERN COMPARISON")
    print("=" * 70)

    points = sorted(data["Point"].unique())

    # Compute values
    idx_max = data.groupby("Point")["Power"].idxmax()
    max_vals = data.loc[idx_max]
    maximum = max_vals.set_index("Point")["Power"].reindex(points)
    max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)

    idx_min = data.groupby("Point")["Power"].idxmin()
    min_vals = data.loc[idx_min]
    minimum = min_vals.set_index("Point")["Power"].reindex(points)
    min_patterns = min_vals.set_index("Point")["Pattern"].reindex(points)

    p10 = (
        data[data["Pattern"] == PATTERN_10].set_index("Point")["Power"].reindex(points)
    )
    p20 = (
        data[data["Pattern"] == PATTERN_20].set_index("Point")["Power"].reindex(points)
    )

    # Plot
    plt.figure(figsize=(16, 9))
    plt.xticks(points, fontsize=16)
    plt.yticks(fontsize=16)

    plt.plot(
        points, maximum, "o-", color="red", linewidth=2.5, markersize=7, label="Maximum"
    )
    plt.plot(
        points,
        minimum,
        "s-",
        color="blue",
        linewidth=2.5,
        markersize=7,
        label="Minimum",
    )
    plt.plot(
        points,
        p10,
        "^--",
        color="darkgreen",
        linewidth=2.5,
        markersize=7,
        label=f"Pattern {PATTERN_10}",
    )
    plt.plot(
        points,
        p20,
        "d:",
        color="black",
        linewidth=2.5,
        markersize=7,
        label=f"Pattern {PATTERN_20}",
    )

    # Labels for MAX and MIN
    for i, x in enumerate(points):
        # MAX (czerwony)
        y = maximum.loc[x]
        pat = int(max_patterns.loc[x])
        y_prev = maximum.loc[points[i - 1]] if i > 0 else None
        y_next = maximum.loc[points[i + 1]] if i < len(points) - 1 else None
        dy, va = label_offset_max(y_prev, y, y_next)
        plt.text(
            x,
            y + dy,
            f"{pat}",
            color="red",
            fontsize=13,
            ha="center",
            va=va,
            fontweight="bold",
        )

        # MIN (niebieski)
        y = minimum.loc[x]
        pat = int(min_patterns.loc[x])
        if x == 4:
            dy, va = -1.5, "top"
        elif x == 10:
            dy, va = -2.5, "top"
        elif x == 14:
            dy, va = 1.5, "bottom"
        else:
            y_prev = minimum.loc[points[i - 1]] if i > 0 else None
            y_next = minimum.loc[points[i + 1]] if i < len(points) - 1 else None
            dy, va = label_offset_min(y_prev, y, y_next)
        plt.text(x, y + dy, f"{pat}", color="blue", fontsize=13, ha="center", va=va)

    plt.xlabel("Measurement Point", fontsize=20)
    plt.ylabel("Received Power [dB]", fontsize=20)
    plt.title("Received Power vs Measurement Point (Scenario A)", fontsize=22)
    plt.ylim(-90, -35)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=16, loc="upper right")
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure1_Scenario_A.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Figure 1 saved: {out}")


# =============================================================================
# FIGURE 2: TOP-K BY AVERAGE SELECTION
# =============================================================================
def generate_figure2(data, all_patterns, output_folder):
    """
    Plot comparing maximum with TOP-K patterns selected by average power.
    Simple method: rank patterns by average → select K best.
    """
    print("\n" + "=" * 70)
    print("FIGURE 2: TOP-K BY AVERAGE SELECTION")
    print("=" * 70)

    points = sorted(data["Point"].unique())
    n_points = len(points)
    total_patterns = len(all_patterns)

    # Global Maximum
    idx_max = data.groupby("Point")["Power"].idxmax()
    max_vals = data.loc[idx_max]
    global_max = max_vals.set_index("Point")["Power"].reindex(points)
    global_max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)

    # Rank patterns by average power
    pattern_mean = data.groupby("Pattern")["Power"].mean().sort_values(ascending=False)
    print(f"\nPattern ranking by average power (TOP-10):")
    print(pattern_mean.head(10))

    # TOP-7 by average
    top7_patterns = pattern_mean.head(7).index.tolist()
    print(f"\nTOP-7 patterns by average: {top7_patterns}")
    top7_data = data[data["Pattern"].isin(top7_patterns)]
    top7_per_point = top7_data.groupby("Point")["Power"].max().reindex(points)

    # TOP-10 by average
    top10_patterns = pattern_mean.head(10).index.tolist()
    print(f"TOP-10 patterns by average: {top10_patterns}")
    top10_data = data[data["Pattern"].isin(top10_patterns)]
    top10_per_point = top10_data.groupby("Point")["Power"].max().reindex(points)

    # Calculate degradation
    degradation_top7 = np.mean(global_max.values - top7_per_point.values)
    degradation_top10 = np.mean(global_max.values - top10_per_point.values)

    print(f"\nDegradation TOP-7: {degradation_top7:.3f} dB")
    print(f"Degradation TOP-10: {degradation_top10:.3f} dB")

    # Plot
    plt.figure(figsize=(16, 9))
    ax = plt.gca()

    # Y bounds
    all_values = [global_max.values, top7_per_point.values, top10_per_point.values]
    y_min = min([v.min() for v in all_values])
    y_max = max([v.max() for v in all_values])
    y_margin = (y_max - y_min) * 0.15

    # Global Maximum
    plt.plot(
        points,
        global_max,
        "o-",
        color="red",
        linewidth=3,
        markersize=8,
        label=f"Maximum ({total_patterns} patterns)",
        zorder=10,
    )

    # TOP-7
    plt.plot(
        points,
        top7_per_point,
        marker="s",
        linestyle="--",
        color="darkgreen",
        linewidth=2.5,
        markersize=7,
        label=f"TOP-7",
        zorder=5,
    )

    # TOP-10
    plt.plot(
        points,
        top10_per_point,
        marker="^",
        linestyle="-.",
        color="darkblue",
        linewidth=2.5,
        markersize=7,
        label=f"TOP-10",
        zorder=5,
    )

    # Labels for MAX
    for x in points:
        y_pos = min(global_max.loc[x] + 0.6, y_max + y_margin - 0.3)
        ax.annotate(
            f"{int(global_max_patterns.loc[x])}",
            xy=(x, global_max.loc[x]),
            xytext=(x, y_pos),
            color="red",
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="bottom",
            annotation_clip=True,
        )

    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.xticks(points, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel("Measurement Point", fontsize=20)
    plt.ylabel("Received Power [dB]", fontsize=20)
    plt.title(f"Received Power: Maximum vs TOP-K by Average", fontsize=22)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=14, loc="upper right", ncol=2)
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure2_TopK_Average.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[✓] Figure 2 saved: {out}")


# =============================================================================
# FIGURE 2B: OPTIMAL PATTERN SELECTION ANALYSIS (BRUTE-FORCE)
# =============================================================================
def generate_figure2b(data, rsrp_matrix, all_patterns, output_folder):
    """
    Plot comparing maximum with optimal K-pattern selection strategies.
    Uses brute-force optimization to find best K-pattern sets.
    """
    print("\n" + "=" * 70)
    print("FIGURE 2B: OPTIMAL PATTERN SELECTION ANALYSIS (BRUTE-FORCE)")
    print("=" * 70)

    points = sorted(data["Point"].unique())
    n_points = len(points)
    total_patterns = len(all_patterns)

    # Global Maximum
    idx_max = data.groupby("Point")["Power"].idxmax()
    max_vals = data.loc[idx_max]
    global_max = max_vals.set_index("Point")["Power"].reindex(points)
    global_max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)

    # Optimal sets for different K values
    results = {}
    for k in tqdm(K_VALUES, desc="Computing optimal K-sets"):
        best_sum, best_combo = find_best_combo(rsrp_matrix, total_patterns, k)
        best_patterns = [all_patterns[i] for i in best_combo]

        # Compute power for each point
        best_powers = np.zeros(n_points)
        patterns_per_point = np.zeros(n_points, dtype=int)

        for pt_idx in range(n_points):
            max_power = -np.inf
            best_pattern_idx = 0
            for combo_idx in best_combo:
                if rsrp_matrix[combo_idx, pt_idx] > max_power:
                    max_power = rsrp_matrix[combo_idx, pt_idx]
                    best_pattern_idx = combo_idx
            best_powers[pt_idx] = max_power
            patterns_per_point[pt_idx] = all_patterns[best_pattern_idx]

        results[k] = {
            "power": pd.Series(best_powers, index=range(1, n_points + 1)),
            "patterns": pd.Series(patterns_per_point, index=range(1, n_points + 1)),
            "combo": best_patterns,
        }
        print(f"  K={k}: {best_patterns}")

    # Plot
    colors = ["green", "orange", "purple", "brown", "pink"]
    markers = ["^", "v", "d", "p", "*"]
    linestyles = [":", "-.", "--", "-", ":"]

    plt.figure(figsize=(16, 9))
    ax = plt.gca()

    # Y bounds
    all_values = [global_max.values]
    for k in K_VALUES:
        all_values.append(results[k]["power"].values)
    y_min = min([v.min() for v in all_values])
    y_max = max([v.max() for v in all_values])
    y_margin = (y_max - y_min) * 0.15

    # Global Maximum
    plt.plot(
        points,
        global_max,
        "o-",
        color="red",
        linewidth=3,
        markersize=8,
        label=f"Maximum ({total_patterns} patterns)",
        zorder=10,
    )

    # Curves for different K values
    for idx, k in enumerate(K_VALUES):
        power = results[k]["power"]
        plt.plot(
            points,
            power,
            marker=markers[idx],
            linestyle=linestyles[idx],
            color=colors[idx],
            linewidth=2.5,
            markersize=7,
            label=f"Optimal {k} patterns",
            zorder=5,
        )

    # Etykiety dla MAX
    for x in points:
        y_pos = min(global_max.loc[x] + 0.6, y_max + y_margin - 0.3)
        ax.annotate(
            f"{int(global_max_patterns.loc[x])}",
            xy=(x, global_max.loc[x]),
            xytext=(x, y_pos),
            color="red",
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="bottom",
            annotation_clip=True,
        )

    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.xticks(points, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel("Measurement Point", fontsize=20)
    plt.ylabel("Received Power [dB]", fontsize=20)
    plt.title(f"Received Power: Maximum vs Optimal K Patterns", fontsize=22)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=14, loc="upper right", ncol=2)
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure2_Optimal_K_Patterns.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()

    # Summary
    print(f"[✓] Figure 2 saved: {out}")
    print("\n  Degradation summary:")
    for k in K_VALUES:
        degradation = np.mean(global_max.values - results[k]["power"].values)
        print(f"    K={k:2d}: {degradation:6.3f} dB")


# =============================================================================
# FIGURE 3: DEGRADATION VS PATTERN COUNT
# =============================================================================
def generate_figure3(rsrp_matrix, all_patterns, baseline_sum, output_folder):
    """
    Plot of degradation as a function of pattern count (N = 1..27).
    """
    print("\n" + "=" * 70)
    print("FIGURE 3: DEGRADATION VS PATTERN COUNT")
    print("=" * 70)

    total_patterns = len(all_patterns)
    n_points = rsrp_matrix.shape[1]

    # Compute for each N value
    k_values = list(range(1, total_patterns + 1))
    degradations = []
    best_sets = []
    best_sums = []

    print(f"Computing optimal sets for N=1..{total_patterns}...")
    for k in tqdm(k_values, desc="Brute-force search"):
        total_combos = comb(total_patterns, k)
        best_sum, best_combo = find_best_combo(rsrp_matrix, total_patterns, k)
        best_set = sorted([all_patterns[i] for i in best_combo])

        degradation = (best_sum - baseline_sum) / n_points
        degradations.append(degradation)
        best_sets.append(best_set)
        best_sums.append(float(best_sum))

    # Save to JSON (convert numpy int64 to Python int)
    results = {
        "total_patterns": int(total_patterns),
        "n_points": int(n_points),
        "baseline_sum": float(baseline_sum),
        "k_values": [int(k) for k in k_values],
        "degradations": [float(d) for d in degradations],
        "best_sets": [[int(p) for p in s] for s in best_sets],
        "best_sums": [float(s) for s in best_sums],
        "all_patterns": [int(p) for p in all_patterns],
    }

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[✓] Results saved: {RESULTS_JSON}")

    # Plot
    plt.figure(figsize=(12, 8))
    plt.plot(
        k_values,
        degradations,
        "o--",
        color="steelblue",
        linewidth=2.5,
        markersize=8,
        markerfacecolor="white",
        markeredgecolor="steelblue",
        markeredgewidth=2,
    )

    plt.xlim(total_patterns + 1, 0)
    plt.xticks(fontsize=16)
    
    # Set Y-axis ticks every 1 dB
    y_min = min(degradations)
    y_max = max(degradations)
    y_ticks = np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1.0)
    plt.yticks(y_ticks, fontsize=16)
    
    plt.xlabel("Pattern count", fontsize=20)
    plt.ylabel("Degradation [dB]", fontsize=20)
    plt.title("Degradation vs Pattern Count", fontsize=22)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure3_Degradation_vs_Count.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Figure 3 saved: {out}")

    return k_values, degradations, best_sets


# =============================================================================
# FIGURE 4: DEGRADATION VS PATTERN COUNT (GREEDY HEURISTIC)
# =============================================================================
def avg_best_case(rsrp_matrix, pattern_indices):
    """
    Computes the average best-case power J̄(S) for a given pattern subset.
    J̄(S) = (1/(K+1)) * Σ_{i=0}^{K} max_{a∈S} RSRP_i(a)

    Args:
        rsrp_matrix: Full RSRP matrix (n_patterns x n_points)
        pattern_indices: List/array of pattern indices currently in S

    Returns:
        Average best-case power (float)
    """
    n_points = rsrp_matrix.shape[1]
    total = 0.0
    for pt in range(n_points):
        max_val = -np.inf
        for idx in pattern_indices:
            if rsrp_matrix[idx, pt] > max_val:
                max_val = rsrp_matrix[idx, pt]
        total += max_val
    return total / n_points


def greedy_heuristic_reduction(rsrp_matrix, target_n):
    """
    Greeedy backward elimination heuristic for RIS pattern set reduction
    (Algorithm 1 from the paper).

    Starting from the full pattern set S = {0, ..., M-1}, iteratively
    removes the pattern whose removal causes the smallest decrease in
    AvgBestCase(S). Ties are broken uniformly at random.

    Args:
        rsrp_matrix: RSRP matrix (n_patterns x n_points)
        target_n: Target subset size N

    Returns:
        history: list of dicts with keys 'S' (pattern set), 'avg_best' (J̄),
                 'removed' (pattern removed at this step, None for initial)
    """
    n_patterns = rsrp_matrix.shape[0]
    S = list(range(n_patterns))  # S ← {1, ..., M}
    history = []

    # Record initial state
    j_initial = avg_best_case(rsrp_matrix, S)
    history.append({"S": list(S), "avg_best": j_initial, "removed": None})

    while len(S) > target_n:
        j_cur = avg_best_case(rsrp_matrix, S)  # Line 9
        delta_min = np.inf  # Line 10
        candidates = []  # C ← ∅

        for a in S:  # Line 11
            S_minus_a = [x for x in S if x != a]
            j_rem = avg_best_case(rsrp_matrix, S_minus_a)  # Line 12
            delta = j_cur - j_rem  # Line 13

            if delta < delta_min:  # Line 14
                delta_min = delta  # Line 15
                candidates = [a]  # Line 16: C ← {a}
            elif delta == delta_min:  # Line 17
                candidates.append(a)  # Line 18: C ← C ∪ {a}

        # Select a* uniformly at random from C (Line 21)
        a_star = random.choice(candidates)
        S.remove(a_star)  # Line 22: S ← S \ {a*}

        j_new = avg_best_case(rsrp_matrix, S)
        history.append({"S": list(S), "avg_best": j_new, "removed": a_star})

    return history


def generate_figure4(rsrp_matrix, all_patterns, baseline_sum, output_folder):
    """
    Plot of degradation as a function of pattern count (N = 1..M)
    using the greedy backward elimination heuristic.
    """
    print("\n" + "=" * 70)
    print("FIGURE 4: DEGRADATION VS PATTERN COUNT (GREEDY HEURISTIC)")
    print("=" * 70)

    total_patterns = len(all_patterns)
    n_points = rsrp_matrix.shape[1]
    baseline_avg = baseline_sum / n_points

    # Run greedy heuristic down to N=1
    print(f"Running greedy heuristic from {total_patterns} down to 1 pattern...")
    history = greedy_heuristic_reduction(rsrp_matrix, target_n=1)

    # Build degradation curve: for each N from 1..total_patterns
    # history[0] = full set (N=total_patterns), history[-1] = 1 pattern
    k_values = []
    degradations = []
    greedy_sets = []

    for entry in history:
        n = len(entry["S"])
        deg = entry["avg_best"] - baseline_avg  # Will be <= 0
        k_values.append(n)
        degradations.append(deg)
        greedy_sets.append([all_patterns[i] for i in entry["S"]])

    # Reverse so k_values goes from 1 to total_patterns
    k_values = k_values[::-1]
    degradations = degradations[::-1]
    greedy_sets = greedy_sets[::-1]

    # Save greedy results to JSON
    greedy_json = os.path.join(output_folder, "degradation_greedy_results.json")
    greedy_results = {
        "method": "greedy_heuristic",
        "total_patterns": int(total_patterns),
        "n_points": int(n_points),
        "baseline_avg": float(baseline_avg),
        "k_values": [int(k) for k in k_values],
        "degradations": [float(d) for d in degradations],
        "greedy_sets": [[int(p) for p in s] for s in greedy_sets],
    }
    with open(greedy_json, "w", encoding="utf-8") as f:
        json.dump(greedy_results, f, indent=2, ensure_ascii=False)
    print(f"[✓] Greedy results saved: {greedy_json}")

    # Print removal order
    print("\n  Removal order (greedy):")
    for entry in history[1:]:
        removed_pattern = all_patterns[entry["removed"]]
        n_remaining = len(entry["S"])
        deg = entry["avg_best"] - baseline_avg
        print(f"    Removed pattern {removed_pattern:2d} → {n_remaining} remaining, degradation: {deg:.3f} dB")

    # Plot
    plt.figure(figsize=(12, 8))
    plt.plot(
        k_values,
        degradations,
        "s--",
        color="darkorange",
        linewidth=2.5,
        markersize=8,
        markerfacecolor="white",
        markeredgecolor="darkorange",
        markeredgewidth=2,
        label="Greedy heuristic",
    )

    plt.xlim(total_patterns + 1, 0)
    plt.xticks(fontsize=16)
    
    # Set Y-axis ticks every 1 dB
    y_min = min(degradations)
    y_max = max(degradations)
    y_ticks = np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1.0)
    plt.yticks(y_ticks, fontsize=16)
    
    plt.xlabel("Pattern count", fontsize=20)
    plt.ylabel("Degradation [dB]", fontsize=20)
    plt.title("Degradation vs Pattern Count (Greedy Heuristic)", fontsize=22)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=16, loc="lower left")
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure4_Degradation_Greedy.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Figure 4 saved: {out}")

    return k_values, degradations, greedy_sets


# =============================================================================
# FIGURE 6: DEGRADATION COMPARISON (BRUTE-FORCE VS GREEDY)
# =============================================================================
def generate_figure6(
    k_values_bf, degradations_bf, k_values_greedy, degradations_greedy, output_folder
):
    """
    Plot comparing brute-force and greedy heuristic on the same graph.
    """
    print("\n" + "=" * 70)
    print("FIGURE 6: DEGRADATION COMPARISON (BRUTE-FORCE VS GREEDY)")
    print("=" * 70)

    plt.figure(figsize=(12, 8))

    # Brute-force curve
    plt.plot(
        k_values_bf,
        degradations_bf,
        "o--",
        color="steelblue",
        linewidth=2.5,
        markersize=8,
        markerfacecolor="white",
        markeredgecolor="steelblue",
        markeredgewidth=2,
        label="Brute-force (optimal)",
    )

    # Greedy heuristic curve
    plt.plot(
        k_values_greedy,
        degradations_greedy,
        "s--",
        color="darkorange",
        linewidth=2.5,
        markersize=8,
        markerfacecolor="white",
        markeredgecolor="darkorange",
        markeredgewidth=2,
        label="Greedy heuristic",
    )

    total_patterns = max(k_values_bf)
    plt.xlim(total_patterns + 1, 0)
    plt.xticks(fontsize=16)

    # Set Y-axis ticks every 1 dB
    all_degs = degradations_bf + degradations_greedy
    y_min = min(all_degs)
    y_max = max(all_degs)
    y_ticks = np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1.0)
    plt.yticks(y_ticks, fontsize=16)

    plt.xlabel("Pattern count", fontsize=20)
    plt.ylabel("Degradation [dB]", fontsize=20)
    plt.title("Degradation vs Pattern Count: Brute-Force vs Greedy", fontsize=22)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=16, loc="lower left")
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure6_Degradation_Comparison.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Figure 6 saved: {out}")

    # Calculate and print differences
    print("\n  Comparison summary:")
    for k in [1, 5, 10, 15, 20, 27]:
        if k in k_values_bf and k in k_values_greedy:
            idx_bf = k_values_bf.index(k)
            idx_greedy = k_values_greedy.index(k)
            deg_bf = degradations_bf[idx_bf]
            deg_greedy = degradations_greedy[idx_greedy]
            diff = deg_greedy - deg_bf
            print(
                f"    K={k:2d}: BF={deg_bf:6.3f} dB, Greedy={deg_greedy:6.3f} dB, diff={diff:6.3f} dB"
            )


# =============================================================================
# FIGURE 5: OPTIMAL K PATTERNS DEGRADATION
# =============================================================================
def generate_figure5(data, rsrp_matrix, all_patterns, output_folder):
    """
    Plot showing power for optimal K-pattern sets.
    K = 8 (minimum bez degradacji), 5, 4, 3, 2, 1
    """
    print("\n" + "=" * 70)
    print("FIGURE 5: OPTIMAL K PATTERNS DEGRADATION")
    print("=" * 70)

    K_VALUES = [8, 5, 4, 3, 2, 1]
    points = sorted(data["Point"].unique())
    n_points = len(points)
    total_patterns = len(all_patterns)

    # Global Maximum
    idx_max = data.groupby("Point")["Power"].idxmax()
    max_vals = data.loc[idx_max]
    global_max = max_vals.set_index("Point")["Power"].reindex(points)
    global_max_patterns = max_vals.set_index("Point")["Pattern"].reindex(points)

    # Compute optimal sets for different K values
    results = {}
    for k in tqdm(K_VALUES, desc="Computing optimal K-sets for Fig 5"):
        best_sum, best_combo = find_best_combo(rsrp_matrix, total_patterns, k)
        best_patterns = [all_patterns[i] for i in best_combo]

        # Compute power for each point
        best_powers = np.zeros(n_points)
        for pt_idx in range(n_points):
            max_power = -np.inf
            for combo_idx in best_combo:
                if rsrp_matrix[combo_idx, pt_idx] > max_power:
                    max_power = rsrp_matrix[combo_idx, pt_idx]
            best_powers[pt_idx] = max_power

        results[k] = {
            "power": pd.Series(best_powers, index=range(1, n_points + 1)),
            "combo": best_patterns,
        }
        print(f"  K={k}: {best_patterns}")

    # Plot - more contrasting colors
    colors = {
        8: "darkgreen",
        5: "blue",
        4: "orange",
        3: "purple",
        2: "brown",
        1: "gray",
    }
    markers = {8: "o", 5: "s", 4: "^", 3: "v", 2: "d", 1: "p"}
    linestyles = {8: "-", 5: "--", 4: "-.", 3: ":", 2: "--", 1: ":"}

    plt.figure(figsize=(16, 9))
    ax = plt.gca()

    # Y bounds
    all_values = [global_max.values]
    for k in K_VALUES:
        all_values.append(results[k]["power"].values)
    y_min = min([v.min() for v in all_values])
    y_max = max([v.max() for v in all_values])
    y_margin = (y_max - y_min) * 0.15

    # Curves for different K values
    for k in K_VALUES:
        power = results[k]["power"]
        label_text = "Maximum (8 patterns)" if k == 8 else f"Optimal {k} patterns"
        plt.plot(
            points,
            power,
            marker=markers[k],
            linestyle=linestyles[k],
            color=colors[k],
            linewidth=2.5,
            markersize=7,
            label=label_text,
            zorder=5,
        )

    # Labels only for MAX
    for x in points:
        y_pos = min(global_max.loc[x] + 0.6, y_max + y_margin - 0.3)
        ax.annotate(
            f"{int(global_max_patterns.loc[x])}",
            xy=(x, global_max.loc[x]),
            xytext=(x, y_pos),
            color="red",
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="bottom",
            annotation_clip=True,
        )

    plt.ylim(y_min - y_margin, -40)
    plt.xticks(points, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel("Measurement Point", fontsize=20)
    plt.ylabel("Received Power [dB]", fontsize=20)
    plt.title(
        f"Received Power: Maximum vs Optimal S Patterns (S = 5, 4, 3, 2, 1)",
        fontsize=22,
    )
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=14, loc="upper right", ncol=2)
    plt.tight_layout()

    out = os.path.join(output_folder, "Figure5_Optimal_K_Degradation.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Figure 5 saved: {out}")

    # Summary
    print("\n  Degradation summary:")
    for k in K_VALUES:
        degradation = np.mean(global_max.values - results[k]["power"].values)
        print(f"    K={k:2d}: {degradation:6.3f} dB")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("\n" + "=" * 70)
    print("ESWA - COMPLETE RIS PERFORMANCE ANALYSIS")
    print("Generating 6 figures for publication")
    print("=" * 70)

    # Load data
    print("\n[1/5] Loading data...")
    data = load_all_points(INPUT_FOLDER)
    data = data[data["Point"].between(POINT_MIN, POINT_MAX)]

    # Map points to 1..N
    mapping = {
        old: new for new, old in enumerate(sorted(data["Point"].unique()), start=1)
    }
    data["Point"] = data["Point"].map(mapping)

    points = sorted(data["Point"].unique())
    n_points = len(points)
    all_patterns = sorted(data["Pattern"].unique())
    total_patterns = len(all_patterns)

    print(f"  Patterns: {total_patterns}, Points: {n_points}")

    # Prepare RSRP matrix
    print("\n[2/5] Preparing RSRP matrix...")
    pattern_to_idx = {p: i for i, p in enumerate(all_patterns)}
    rsrp_matrix = np.full((total_patterns, n_points), -np.inf)
    for _, row in data.iterrows():
        i = pattern_to_idx[row["Pattern"]]
        j = row["Point"] - 1
        rsrp_matrix[i, j] = row["Power"]
    rsrp_matrix = np.ascontiguousarray(rsrp_matrix, dtype=np.float64)

    # Baseline (all patterns)
    baseline_sum = 0.0
    for pt_idx in range(n_points):
        baseline_sum += np.max(rsrp_matrix[:, pt_idx])

    # Generate figures
    print("\n[3/7] Generating figures...")
    generate_figure1(data, OUTPUT_FOLDER)
    generate_figure2(data, all_patterns, OUTPUT_FOLDER)
    k_values, degradations, best_sets = generate_figure3(
        rsrp_matrix, all_patterns, baseline_sum, OUTPUT_FOLDER
    )
    k_values_g, degradations_g, greedy_sets = generate_figure4(
        rsrp_matrix, all_patterns, baseline_sum, OUTPUT_FOLDER
    )
    generate_figure5(data, rsrp_matrix, all_patterns, OUTPUT_FOLDER)
    generate_figure6(k_values, degradations, k_values_g, degradations_g, OUTPUT_FOLDER)

    print("\n" + "=" * 70)
    print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
    print("=" * 70)
    print(f"\nOutput folder: {OUTPUT_FOLDER}")
    print("Files generated:")
    print("  - Figure1_Scenario_A.png")
    print("  - Figure2_TopK_Average.png")
    print("  - Figure3_Degradation_vs_Count.png")
    print("  - Figure4_Degradation_Greedy.png")
    print("  - Figure5_Optimal_K_Degradation.png")
    print("  - Figure6_Degradation_Comparison.png")
    print("  - degradation_results.json")
    print("  - degradation_greedy_results.json")


if __name__ == "__main__":
    main()
