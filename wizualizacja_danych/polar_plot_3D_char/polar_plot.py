import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_multiple_patterns_from_csv(file_path, patterns,vertical_val):
    df = pd.read_csv(file_path, delimiter=';', header=None)
    df.columns = ['horizontal', 'vertical', 'patern', 'freq', 'power']

    for patern in patterns:
        for vertical in vertical_val:
            # Wybieramy dane dla danego paterns i vertical
            data = df[(df['patern'] == patern) & (df['vertical'] == vertical)]
            
            # Wartości kątów i mocy
            theta = data['horizontal']
            powers = data['power']
            
            # Tworzenie wykresu polar plot
            plt.figure(figsize=(8, 6))
            ax = plt.subplot(111, projection='polar')
            ax.plot(np.deg2rad(theta), powers)  #
            ax.set_thetamin(0)
            ax.set_thetamax(180)
            # Dodanie tytułu
            plt.title(f'Wykres polar plot dla patern={patern}, vertical={vertical}')
            
            # Pokazanie wykresu
            plt.show()

file_path=r'C:\Users\Paweł\Desktop\Kliks\Ris\Python_RIS\wyniki\charakterystyka_3D\24_04_ch_ka_3D_5_5Ghz_1_5m.csv'
patterns=[1,2,3]
vertical=[-27,-18,-9]
plot_multiple_patterns_from_csv(file_path, patterns,vertical)
