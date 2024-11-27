import math
import csv

# ILOŚĆ ELEMENTÓW
M = 16
N = 16

# Wymiary RIS-a
dx = 0.020
dy = 0.013

# Odległości anten od matrycy
d_y = 1.5  # odległość
d_x = 1    # od środka

# Inicjalizacja macierzy
fi = [[0 for _ in range(N)] for _ in range(M)]
r = [[0 for _ in range(N)] for _ in range(M)]

# Obliczenia dla każdej pozycji (m, n)
for m in range(-M//2, M//2):
    for n in range(-N//2, N//2):
        # Konwersja indeksów macierzy
        m_idx = m + M//2
        n_idx = n + N//2

        # Przyprostokątna i przeciwprostokątna
        a = math.sqrt(d_y**2 + (m * dy)**2)  # Pionowa przyprostokątna
        b = d_x + n * dx  # Pozioma przyprostokątna (nie używana w obliczeniach kąta)
        c = math.sqrt(a**2 + b**2)  # Przeciwprostokątna

        # Zapisanie odległości
        r[m_idx][n_idx] = c

        # Obliczenie kąta phi między przyprostokątną "a" a przeciwprostokątną "c"
        if c > 0:  # Unikamy dzielenia przez zero
            cos_phi = a / c
            fi[m_idx][n_idx] = math.acos(cos_phi)

# Zapis do pliku CSV
with open("wektor_r_N_M.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["M", "N", "R", "Phi"])  # Nagłówki kolumn
    for m in range(M):
        for n in range(N):
            writer.writerow([m - M//2, n - N//2, r[m][n], fi[m][n]])
