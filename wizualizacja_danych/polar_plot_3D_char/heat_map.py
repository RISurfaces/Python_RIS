import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file, patterns, horizontal_range=(45, 135)):
    df = pd.read_csv(file, sep=';', header=None, names=['vertical', 'horizontal', 'pattern', 'freq', 'power'])
    for pattern in patterns:
        df_pattern = df[(df['pattern'] == pattern) & (df['horizontal'] >= horizontal_range[0]) & (df['horizontal'] <= horizontal_range[1])]
        heatmap_data = df_pattern.pivot_table(index='horizontal', columns='vertical', values='power')
        plt.figure(figsize=(10, 7))
        sns.heatmap(heatmap_data, vmax=-50, vmin=-100, cmap='viridis', fmt=".2g")
        plt.gca().invert_yaxis()
        plt.title(f'Power Heatmap for Pattern {pattern}')
        plt.xlabel('Horizontal Angle')
        plt.ylabel('Vertical Angle')
        plt.savefig(f'heatmap_pattern_{pattern}.jpg', format='jpg')
        plt.show()



file_path=r'/Users/dawidbrzakala/Python_RIS/wyniki/charakterystyka_3D/09_05_ch_ka_3D_5_5Ghz_1_5m_blacha_miedz.csv'
patterns=[-1]
plot_multiple_patterns_from_csv(file_path, patterns)
