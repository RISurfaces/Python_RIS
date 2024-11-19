import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_difference_between_patterns(file1, file2, patterns, horizontal_range=(45, 135)):
    # Wczytywanie danych z obu plików
    df1 = pd.read_csv(file1, sep=';', header=None, names=[ 'vertical','horizontal', 'pattern', 'freq', 'power'])
    df2 = pd.read_csv(file2, sep=';', header=None, names=['horizontal', 'vertical', 'pattern', 'freq', 'power'])
    
    # Iteracja po wzorcach
    for pattern in patterns:
        # Filtracja danych dla danego wzorca i zakresu horyzontalnego
        df1_pattern = df1[(df1['pattern'] == pattern) & (df1['horizontal'] >= horizontal_range[0]) & (df1['horizontal'] <= horizontal_range[1])]
        df2_pattern = df2[(df2['pattern'] == pattern) & (df2['horizontal'] >= horizontal_range[0]) & (df2['horizontal'] <= horizontal_range[1])]

        # Połączenie danych po 'horizontal' i 'vertical' w celu obliczenia różnicy
        merged = pd.merge(
            df1_pattern, 
            df2_pattern, 
            on=['horizontal', 'vertical'], 
            suffixes=('_file1', '_file2')
        )
        merged['power_diff'] =abs( merged['power_file1'] - merged['power_file2'])

        # Przygotowanie danych do heatmapy
        heatmap_data = merged.pivot_table(index='vertical', columns='horizontal', values='power_diff')
        
        # Rysowanie heatmapy
        plt.figure(figsize=(11, 10))
        ax = sns.heatmap(heatmap_data, vmax=20 , vmin=0, cbar_kws={'label': 'Power difference [dBm]'}, cmap='coolwarm', annot=False, fmt=".2g")
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(labelsize=14)  # Font size of colorbar numbers
        cbar.ax.yaxis.label.set_size(18)  # Font size of colorbar label
        distance = 1.5
        ax.invert_yaxis()
        plt.title(f'Difference for Pattern {pattern} on {distance}m - chamber vs LAB', fontsize=22)
        plt.xlabel('Azimuth angle [°]', fontsize=18)
        plt.ylabel('Elevation angle [°]', fontsize=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(f'diff_heatmap_pattern_{pattern}_dist_{distance}m_chamber_VS_LAB.jpg', format='jpg', bbox_inches='tight')
        plt.close()


# Ścieżki do plików
file1_path = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wyniki_surowe_dane\charakterystyka_3D\char_pozioma_3D\24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero.csv'
file2_path = r'C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_komora_PIT\13_08_3D_5_5Ghz_1_5m_chamber.csv'

# Lista wzorców
patterns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Wywołanie funkcji
plot_difference_between_patterns(file1_path, file2_path, patterns)
