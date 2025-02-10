import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_multiple_patterns_from_csv(file):
    df = pd.read_csv(file, sep=';', header=None, names=['vertical', 'horizontal', 'freq', 'power'])
        df_patern = df[df[''] == 0]
        heatmap_data = df_.pivot_table(index='vertical', columns='horizontal', values='power')
        plt.figure(figsize=(10, 7))
        sns.heatmap(heatmap_data,vmax=-50,vmin=-100, cmap='viridis', fmt=".2g",)
        plt.gca().invert_yaxis()
        plt.title(f'Heatmapa mocy dla paternu blacha')
        plt.xlabel('Kąt horizontal')
        plt.ylabel('Vertical')
        plt.savefig('heatmapa_patern_blacha.jpg', format='jpg')
        plt.show()




file_path=r'/Users/dawidbrzakala/Python_RIS/wyniki/charakterystyka_3D/09_05_ch_ka_3D_5_5Ghz_1_5m_blacha_miedz.csv'
plot_multiple_patterns_from_csv(file_path)
