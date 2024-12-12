import numpy as np
import pandas as pd

# Funkcja obliczająca F(θ, φ)
def calculate_F(theta_rad, phi_rad):
    """Oblicza F(θ, φ) zgodnie z podanym wzorem. Zakłada, że θ i φ są w radianach."""
    if 0 <= theta_rad <= np.pi / 2:
        return np.cos(theta_rad)**3
    elif np.pi / 2 < theta_rad <= np.pi:
        return 0
    else:
        raise ValueError("Theta poza zakresem dla funkcji F.")

# Funkcja obliczająca współrzędne elementów RIS
def get_ris_coordinates(M, N, dx, dy):
    x_coords = np.linspace(-(M // 2) * dx, (M // 2) * dx, M)
    y_coords = np.linspace(-(N // 2) * dy, (N // 2) * dy, N)
    return np.meshgrid(x_coords, y_coords)

# Funkcja obliczająca odległości r_t i r_r dla każdego elementu RIS
def calculate_distances(M, N, dx, dy, tx_pos, rx_pos):
    X, Y = get_ris_coordinates(M, N, dx, dy)
    # Odległości od nadajnika
    rt = np.sqrt((X - tx_pos[0])**2 + (Y - tx_pos[1])**2 + tx_pos[2]**2)
    # Odległości od odbiornika
    rr = np.sqrt((X - rx_pos[0])**2 + (Y - rx_pos[1])**2 + rx_pos[2]**2)
    return rt, rr

# Konwersja mW na dBm
def mW_to_dBm(mW):
    return 10 * np.log10(mW)

# Parametry
Pt_dBm = -10  # Moc nadawcza w dBm
Gt_dB = 14.0   # Zysk anteny nadawczej w dB
Gr_dB = 14.0   # Zysk anteny odbiorczej w dB
G_dB = 1.0    # Zysk RIS w dB
M = 16        # Liczba elementów w macierzy (wiersze)
N = 16        # Liczba elementów w macierzy (kolumny)
c = 3 * 10**8  # Prędkość światła [m/s]
f = 5.5 * 10**9  # Częstotliwość [Hz]
A = 0.8       # Współczynnik odbicia RIS
dx = 0.020    # Odstęp w poziomie [m]
dy = 0.013    # Odstęp w pionie [m]
wavelength = c / f  # Długość fali [m]

# Przeliczanie zysków na wartości liniowe
Pt_lin = 10**(Pt_dBm/10)  # Moc nadawcza w dBm
Gt_lin = 10**(Gt_dB / 10)
Gr_lin = 10**(Gr_dB / 10)
G_lin = 10**(G_dB / 10)

# Zakres kątów (w stopniach)
elevation_angles = np.arange(-27, 28, 9)  # Elewacja co 9 stopni
azimuth_angles = np.arange(0, 181, 1.8)   # Azymut co 1.8 stopnia

# Pozycje nadajnika i odbiornika
tx_pos = (1, 1.5, 0)  # Pozycja nadajnika 
rx_pos = (-1, 1.5, 0)   # Pozycja odbiornika 

# Oblicz odległości dla każdego elementu RIS
rt_nm, rr_nm = calculate_distances(M, N, dx, dy, tx_pos, rx_pos)

# Obliczenie stałej
constant = (Pt_lin * Gt_lin * Gr_lin * G_lin * dx * dy * wavelength**2 * A**2) / (64 * np.pi**3)

# Lista do przechowywania wyników
results = []

# Iteracja po kątach azymutu i elewacji
for elev_angle in elevation_angles:
    for azim_angle in azimuth_angles:
        # Konwersja kątów na radiany
        theta = np.deg2rad(elev_angle)
        phi = np.deg2rad(azim_angle)

        # Oblicz moc odbieraną dla danej pary kątów
        summation = 0
        for m in range(-M // 2, M // 2):  # -8 do 7
            for n in range(-N // 2, N // 2):  # -8 do 7
                # Mapowanie na indeksy NumPy
                m_idx = m + M // 2  # Przesunięcie do zakresu 0-15
                n_idx = n + N // 2  # Przesunięcie do zakresu 0-15

                rt = rt_nm[m_idx, n_idx]  # Odległość r_t
                rr = rr_nm[m_idx, n_idx]  # Odległość r_r

                # Kąt fazowy (uwzględniając odległości i fazę RIS)
                phi_m_n = 2 * np.pi * (rt + rr) / wavelength

                # Obliczenie funkcji F(θ, φ)
                F = calculate_F(theta, phi)

                # Człon wykładniczy
                exp_term = np.exp(-1j * phi_m_n)

                # Dodaj do sumy
                summation += np.sqrt(F) * exp_term / (rt * rr)

        # Obliczenie mocy sygnału odbieranego
        Pr_mW = constant * np.abs(summation)**2

        # Konwersja mocy na dBm
        Pr_dBm = mW_to_dBm(Pr_mW)

        # Zapisz wynik do listy
        results.append([azim_angle, elev_angle, Pr_dBm])

# Zapis wyników do pliku CSV
output_filepath = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Theoretical_model\received_signal_power.csv'
results_df = pd.DataFrame(results, columns=['Azimuth Angle (deg)', 'Elevation Angle (deg)', 'Received Power (Pr) [dBm]'])
results_df.to_csv(output_filepath, index=False)

print(f"Results saved to {output_filepath}")
