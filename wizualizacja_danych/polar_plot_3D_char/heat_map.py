import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file, patterns, horizontal_range=(45, 135)):
    df = pd.read_csv(file, sep=';', header=None, names=['horizontal','vertical' , 'pattern', 'freq', 'power'])
    vertical = []
    for pattern in patterns:
        df_pattern = df[(df['pattern'] == pattern) & (df['horizontal'] >= horizontal_range[0]) & (df['horizontal'] <= horizontal_range[1])]
        heatmap_data = df_pattern.pivot_table(index='vertical', columns='horizontal', values='power')
        plt.figure(figsize=(11, 10))
        #sns.set(font_scale=1.2)  # Set the font scale for seaborn heatmap
        ax= sns.heatmap(heatmap_data, vmax=-30, vmin=-100,cbar_kws={'label': 'Received power [dBm]'}, cmap='viridis', annot=False, fmt=".2g")
        cbar= ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(labelsize=14) #Font size of colorbar numbers
        cbar.ax.yaxis.label.set_size(18) #Font size of colorbar label cbar_kws
        distance=1_5
        ax.invert_yaxis()
        plt.title(f'Patern {pattern} on {distance}m', fontsize=22)
        #plt.title(f'Heatmap for pattern {pattern} on {distance}m', fontsize=22)
        plt.xlabel('Azimuth angle [°]', fontsize=18)
        plt.ylabel('Elevation angle [°]', fontsize=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(f'heatmap_pattern_{pattern}_dist_{distance}m_.jpg', format='jpg', bbox_inches='tight')
        #plt.show()
        plt.close()




file_path=r'C:\Users\Brzaki\Documents\Python_RIS\wyniki_surowe_dane\charakterystyka_3D_nowe_anteny_AINFO\24_10_3D_5_5Ghz_1_5m_new_ant.csv'
patterns=[1, 20, 17, 8]
plot_multiple_patterns_from_csv(file_path, patterns)
