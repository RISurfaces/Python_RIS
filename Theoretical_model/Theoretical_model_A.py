import numpy as np
import math
import pandas as pd 

def read_rt_rr_from_csv(filepath):
    data = pd.read_csv(filepath)
    
    # Przekształć dane w tabelę przestawną, aby wygenerować siatkę (macierz wartości)
    rt_matrix = data.pivot(index='M', columns='N', values='R')
    
    # Konwersja do macierzy NumPy
    r_t = rt_matrix.values
    r_r = r_t  # W tym przypadku zakładamy, że r_r = r_t, ale można zmodyfikować w razie potrzeby
    
    return r_t, r_r

Pt = -10 
Gt = 14.0  
Gr = 14.0  
G = 1 
M = 16
N = 16
c=10^8
f=5.5*10^9
# Wymiary RIS-a
dx = 0.020
dy = 0.013 
lammbda = c/f  
fi= 1

F_combine = math.cos(fi)^3
Gamma = 1
r_t, r_r = read_rt_rr_from_csv(r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\Theoretical_model\wektor r_N_M.csv')


# Compute the received power
factor = (Gt * Gr * G * dx * dy * lammbda**2) / (64 * np.pi**3)
summation = 0

for m in range(1-M//2, M // 2 + 1):
    for n in range(1-N//2, N // 2 + 1):
        F = F_combine[m-1, n-1]
        gamma = Gamma[m-1, n-1]
        rt = r_t[m-1, n-1]
        rr = r_r[m-1, n-1]
        
        term = np.sqrt(F * gamma) * (rt * rr) / (rt + rr) * np.exp(-1j * 2 * np.pi * (rt + rr) / lammbda)
        summation += term

Pr = Pt * factor * np.abs(summation)**2

print(f"Received Power Pr: {Pr}")
