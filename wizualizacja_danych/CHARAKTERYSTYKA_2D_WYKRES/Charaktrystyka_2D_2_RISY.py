import pandas as pd
import matplotlib.pyplot as plt

def plot_multiple_patterns_from_csv(file_path, patterns):
    df = pd.read_csv(file_path, sep=';', names=['Degrees','Paterns', 'Frequency', 'Power'])
    # Ensure the DataFrame is sorted by 'Frequency' to connect points in ascending frequency order
    df[['Degrees']] = df[['Degrees']].apply(pd.to_numeric)
    df = df.sort_values(by='Degrees')
    df = df[(df['Degrees'] >= 45) & (df['Degrees'] <= 135)]
    power_min = -92
    power_max = -44
    plt.figure(figsize=(15, 10))
    colors=['blue','red', 'green', 'black', 'orange', 'purple']
    markers = ['o','s', 'd', '^', 'v', 'p' ]
    for index, pattern in enumerate(patterns):
        specific_pattern_df = df[df['Paterns'] == pattern]
        print(pattern)
        if specific_pattern_df.empty:
            print(f"No entries found for pattern '{pattern}'.")
            continue
        color = colors[index % len(colors)]
        marker = markers[index % len(markers)]
        plt.plot(specific_pattern_df['Degrees'], specific_pattern_df['Power'], marker=marker, linestyle='-', label=pattern, color=color)
    plt.xlabel('Azimuth angle [°]', fontsize=28)
    plt.ylabel('Recived power [dBm]', fontsize=28)
    plt.title('Recived power over RIS azimuth angle - with second RIS', fontsize=24)
    plt.xlim(45, 135)
    plt.ylim(power_min, power_max)
    plt.xticks([x *5 for x in range(9, 27)], rotation=45, fontsize=16)  
    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))], fontsize=16)  
    plt.legend(["1", "2","3","4","5","6"], loc="upper right", prop={'size': 18}, borderaxespad=0.5, title_fontsize=18, title='')
    plt.grid(True)
    plt.savefig(f'2D_pattern.jpg', format='jpg',  bbox_inches='tight')
    plt.show()
    

# Adjusted for demonstration; replace with your actual file path and patterns
file_path = open(r'C:\Users\Marcel\Python_RIS\Python_RIS\wyniki_surowe_dane\charakterystyka_2D\char_2_RIS_2D\2D_2RIS_1_5m_16_06.csv')
patterns = [1,2,17,8,20,19]#,"Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
plot_multiple_patterns_from_csv(file_path, patterns)#"All elements turn on","Only first element turn on","Only last element turn on","Left side on",