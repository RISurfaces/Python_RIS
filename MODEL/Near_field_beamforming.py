import numpy as np
import pandas as pd


def read_rt_rr_from_csv(filepath):
    data = pd.read_csv(filepath)
    
    rt_matrix = data.pivot(index='M', columns='N', values='R')
    
    # Konwersja do macierzy NumPy
    r_t = rt_matrix.values
    r_r = r_t  # W tym przypadku zakładamy, że r_r = r_t, ale można zmodyfikować w razie potrzeby
    
    return r_t, r_r
Pt = -10 
Gt = 1.0  
Gr = 1.0  
G = 1 
M = 16
N = 16
c=10^8
f=5.5*10^9
A=0.8
A1=0.6
A2=0.8
dx = 0.020
dy = 0.013 
wavelength = c/f  
fi= 1


# Define arrays (example values, replace with actual data)
F_combine = np.ones((M, N))  # Array for F_combine (all ones as example)
rt_nm, rr_nm = read_rt_rr_from_csv(r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Theoretical_model\wektor r_N_M.csv')

phi_nm = np.random.uniform(0, 2*np.pi, (M, N))  # Array for phi_n,m

# Precompute constant
constant = (Pt * Gt * Gr * G * dx * dy * wavelength**2 * A**2) / (64 * np.pi**3)

# Compute double summation
summation = 0
for m in range(1-M//2, M // 2 + 1):
    for n in range(1-N//2, N // 2 + 1):
        rt = rt_nm[m, n]
        rr = rr_nm[m, n]
        phi = phi_nm[m, n]
        F = F_combine[m, n]
        
        # Exponential term
        exp_term = np.exp(-1j * 2 * np.pi * (rt + rr - wavelength * phi) / wavelength)
        
        # Add to summation
        summation += np.sqrt(F) * exp_term / (rt * rr)

# Compute received signal power
Pr = constant * np.abs(summation)**2

print("Received Signal Power (Pr):", Pr)
