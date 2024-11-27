import math
import csv

# ILOŚĆ ELEMENTÓW
M = 16
N = 16
fi=[[0 for _ in range(-N//2, N//2+1)] for _ in range(-M//2, M//2+1)]
# Wymiary RIS-a
dx = 0.020
dy = 0.013 


# ODLEGŁOŚCI ANTEN OD MATRYCY
d_y = 1.5  # odległość
d_x = 1    # od środka

r = [[0 for _ in range(-N//2, N//2+1)] for _ in range(-M//2, M//2+1)]

for m in range(-M//2, M//2+1):
    for n in range(-N//2, N//2+1):
        r[m][n + N//2] = math.sqrt((math.sqrt(d_y**2 + (abs(m) * dy/2)**2))**2 + (d_x + n * dx / 2)**2)
        a= math.sqrt(d_y**2 + (abs(m) * dy/2)**2)
        b=(d_x + n * dx / 2)
        c=r[m][n+N//2]
        fi[m][n+N//2]=math.acos( math.cos(a**2 + b**2 - c**2) / (2 * a * b))

with open("wektor r_N_M.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["M", "N", "R"])  # Nagłówki kolumn
    for m in range(-M//2, M//2+1):
        for n in range(-N//2, N//2+1):
            writer.writerow([m, n, r[m][n + N//2], fi[m][n+N//2]])

