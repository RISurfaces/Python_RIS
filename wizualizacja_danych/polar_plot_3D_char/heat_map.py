import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file, patterns, horizontal_range=(45, 135)):
    df = pd.read_csv(file, sep=';', header=None, names=['vertical', 'horizontal', 'pattern', 'freq', 'power'])
    for pattern in patterns:
        df_pattern = df[(df['pattern'] == pattern) & (df['horizontal'] >= horizontal_range[0]) & (df['horizontal'] <= horizontal_range[1])]
        heatmap_data = df_pattern.pivot_table(index='vertical', columns='horizontal', values='power')
        plt.figure(figsize=(11, 10))
        #sns.set(font_scale=1.2)  # Set the font scale for seaborn heatmap
        ax= sns.heatmap(heatmap_data, vmax=-50, vmin=-100,cbar_kws={'label': 'Moc odebrana [dBm]'}, cmap='viridis', annot=False, fmt=".2g")
        cbar= ax.collections[0].colorbar

        cbar.ax.yaxis.set_tick_params(labelsize=14) #Font size of colorbar numbers
        cbar.ax.yaxis.label.set_size(18) #Font size of colorbar label cbar_kws

        ax.invert_yaxis()
        plt.title(f'Heatmapa dla wzorca 1', fontsize=22)
        plt.xlabel('Kąty azymutu [°]', fontsize=18)
        plt.ylabel('Kąty elewacji [°]', fontsize=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        
        plt.savefig(f'heatmap_pattern_{pattern}.jpg', format='jpg')
        plt.show()




file_path=r'wyniki/charakterystyka_3D/24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero.csv'
patterns=[1]
plot_multiple_patterns_from_csv(file_path, patterns)
