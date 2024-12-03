import numpy as np
import pandas as pd

# Funkcja odczytu danych z CSV
def read_rt_rr_from_csv(filepath):
    # Odczyt danych
    data = pd.read_csv(filepath)
    
    # Tworzenie macierzy odległości R i kątów Phi
    rt_matrix = data.pivot(index='M', columns='N', values='R')
    phi_matrix = data.pivot(index='M', columns='N', values='Phi')
    
    # Przesunięcie indeksów (-8 do 8) na zakres (0 do 16)
    rt_matrix.index += 8
    rt_matrix.columns += 8
    phi_matrix.index += 8
    phi_matrix.columns += 8
    
    # Konwersja do macierzy NumPy
    r_t = rt_matrix.values  # Macierz odległości r_t
    r_r = r_t  # Zakładamy, że r_r = r_t
    phi_nm = phi_matrix.values  # Macierz kątów phi_n,m
    
    return r_t, r_r, phi_nm

# Parametry
Pt = -10  # Moc nadawcza w dBm
Gt = 13.0  # Zysk anteny nadawczej
Gr = 13.0  # Zysk anteny odbiorczej
G = 1     # Zysk RIS
M = 16    # Liczba elementów w macierzy (wiersze)
N = 16    # Liczba elementów w macierzy (kolumny)
c = 10**8  # Prędkość światła [m/s]
f = 5.5 * 10**9  # Częstotliwość [Hz]
A = 0.8   # Współczynnik odbicia RIS
dx = 0.020  # Odstęp w poziomie [m]
dy = 0.013  # Odstęp w pionie [m]
wavelength = c / f  # Długość fali [m]

# Zakres kątów (w stopniach)
elevation_angles = np.arange(-27, 28, 9)  # Elewacja co 9 stopni
azimuth_angles = np.arange(0, 181, 1.8)   # Azymut co 1.8 stopnia

# Wczytaj dane z pliku CSV
filepath = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Theoretical_model\wektor_r_N_M.csv'
rt_nm, rr_nm, phi_nm = read_rt_rr_from_csv(filepath)

# Zainicjuj macierz dla F_combine (przykładowe wartości)
F_combine = np.ones((M, N))

# Obliczenie stałej
constant = (Pt * Gt * Gr * G * dx * dy * wavelength**2 * A**2) / (64 * np.pi**3)

# Lista do przechowywania wyników
results = []

# Iteracja po kątach azymutu i elewacji
for elev_angle in elevation_angles:
    for azim_angle in azimuth_angles:
        # Oblicz moc odbieraną dla danej pary kątów
        summation = 0
        for m in range(-M // 2, M // 2):  # -8 do 7
            for n in range(-N // 2, N // 2):  # -8 do 7
                # Mapowanie na indeksy NumPy
                m_idx = m + M // 2  # Przesunięcie do zakresu 0-15
                n_idx = n + N // 2  # Przesunięcie do zakresu 0-15

                rt = rt_nm[m_idx, n_idx]  # Odległość r_t
                rr = rr_nm[m_idx, n_idx]  # Odległość r_r
                phi = phi_nm[m_idx, n_idx]  # Kąt phi
                #F = 1*math.cos  # Współczynnik F

                # Człon wykładniczy
                exp_term = np.exp(-1j * 2 * np.pi * (rt + rr - wavelength * phi) / wavelength)

                # Dodaj do sumy
                summation += np.sqrt(F) * exp_term / (rt * rr)

        # Obliczenie mocy sygnału odbieranego
        Pr = constant * np.abs(summation)**2

        # Zapisz wynik do listy
        results.append([azim_angle, elev_angle, Pr])

# Zapis wyników do pliku CSV
output_filepath = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Theoretical_model\received_signal_power.csv'
results_df = pd.DataFrame(results, columns=['Azimuth Angle (deg)', 'Elevation Angle (deg)', 'Received Power (Pr)'])
results_df.to_csv(output_filepath, index=False)

print(f"Results saved to {output_filepath}")
