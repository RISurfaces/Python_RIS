import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file,patterns):
    df = pd.read_csv(file, sep=';', header=None, names=['vertical', 'horizontal', 'patern', 'freq', 'power'])
    for patern in patterns:
        df_patern = df[df['patern'] == patern]
        heatmap_data = df_patern.pivot_table(index='vertical', columns='horizontal', values='power')
        plt.figure(figsize=(10, 7))
        sns.heatmap(heatmap_data,vmax=-50,vmin=-100, cmap='viridis', fmt=".2g",)
        plt.gca().invert_yaxis()
        plt.title(f'Heatmapa mocy dla paternu {patern}')
        plt.xlabel('Kąt horizontal')
        plt.ylabel('Vertical')
        plt.savefig(f'heatmapa_patern_{patern}.jpg', format='jpg')
        plt.show()




file_path=r'..\..\wyniki\charakterystyka_3D\24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero.csv'
patterns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
plot_multiple_patterns_from_csv(file_path, patterns)
