import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file, patterns, horizontal_range=(45, 135)):
    df = pd.read_csv(file, sep=';', header=None, names=['vertical', 'horizontal', 'pattern', 'freq', 'power'])
    for pattern in patterns:
        df_pattern = df[(df['pattern'] == pattern) & (df['horizontal'] >= horizontal_range[0]) & (df['horizontal'] <= horizontal_range[1])]
        heatmap_data = df_pattern.pivot_table(index='vertical', columns='horizontal', values='power')
        plt.figure(figsize=(10, 7))
        #sns.set(font_scale=1.2)  # Set the font scale for seaborn heatmap
        sns.heatmap(heatmap_data, vmax=-50, vmin=-100, cmap='viridis', annot=False, fmt=".2g")
        plt.gca().invert_yaxis()
        plt.title(f'Power Heatmap for Pattern {pattern}', fontsize=22)
        plt.xlabel('Horizontal Angle', fontsize=18)
        plt.ylabel('Vertical Angle', fontsize=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        
        plt.savefig(f'heatmap_pattern_{pattern}.jpg', format='jpg')
        plt.show()




file_path=r'wyniki/charakterystyka_3D/24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero.csv'
patterns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
plot_multiple_patterns_from_csv(file_path, patterns)
