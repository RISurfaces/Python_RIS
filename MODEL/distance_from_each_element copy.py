import math
import csv
import numpy as np

# ILOŚĆ ELEMENTÓW
M = 16  # liczba wierszy
N = 16  # liczba kolumn

# Wymiary RIS-a
dx = 0.020  # odstęp w poziomie
dy = 0.013  # odstęp w pionie

# Pozycja nadajnika
d_y = 1.5  # odległość od matrycy (prostopadle)
d_x = 1.0  # odległość w lewo od środka matrycy

# Zakres kątów
elevation_angles = np.radians(np.arange(-27, 27 + 9, 9))  # Elewacja co 9 stopni w radianach
azimuth_angles = np.radians(np.arange(0, 180 + 1.8, 1.8))    # Azymut co 1.8 stopnia w radianach

# Wyniki będą przechowywane w macierzy dla każdego kąta
results = []

# Obliczenia dla każdego kąta
for theta in elevation_angles:  # Kąt elewacji
    for phi in azimuth_angles:  # Kąt azymutu
        fi = [[0 for _ in range(N+1)] for _ in range(M+1)]
        r = [[0 for _ in range(N+1)] for _ in range(M+1)]
        
        for m in range(-M//2, M//2+1):
            for n in range(-N//2, N//2+1):
                # Pozycja elementu w układzie matrycy
                x = n * dx
                y = m * dy
                z = 0  # Wszystkie elementy matrycy są w płaszczyźnie xy

                # Obrót w azymucie
                x_rot = x * math.cos(phi) - y * math.sin(phi)
                y_rot = x * math.sin(phi) + y * math.cos(phi)
                z_rot = z

                # Obrót w elewacji
                y_final = y_rot * math.cos(theta) - z_rot * math.sin(theta)
                z_final = y_rot * math.sin(theta) + z_rot * math.cos(theta)

                # Odległość od nadajnika (w nowym układzie współrzędnych)
                a = math.sqrt(d_y**2 + y_final**2)  # pionowa przyprostokątna
                b = d_x + x_rot  # pozioma przyprostokątna
                c = math.sqrt(a**2 + b**2)  # przeciwprostokątna

                # Zapisanie odległości
                m_idx = m + M//2
                n_idx = n + N//2
                r[m_idx][n_idx] = c

                # Obliczenie kąta phi między "a" a "c"
                if c > 0:
                    cos_phi = a / c
                    fi[m_idx][n_idx] = math.acos(cos_phi)

        # Zapisanie wyników dla danego kąta
        results.append((theta, phi, r, fi))

# Zapis do pliku CSV dla ostatniej kombinacji kątów
with open("matryca_obrocona.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Theta", "Phi", "M", "N", "R", "Phi"])  # Nagłówki kolumn
    for theta, phi, r, fi in results:
        for m in range(M+1):
            for n in range(N+1):
                writer.writerow([math.degrees(theta), math.degrees(phi), m - M//2, n - N//2, r[m][n], fi[m][n]])
