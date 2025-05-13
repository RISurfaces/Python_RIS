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
    colors=['orange','brown', 'black', 'green', 'blue', 'purple']
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
    plt.title('Recived power over RIS azimuth angle - with single RIS', fontsize=24)
    plt.xlim(45, 135)
    plt.ylim(power_min, power_max)
    plt.xticks([x *5 for x in range(9, 27)], rotation=45, fontsize=16)  
    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))], fontsize=16)  
    plt.legend(["1", "2","5","6"], loc="upper right", prop={'size': 18}, borderaxespad=0.5, title_fontsize=18, title='')
    plt.grid(True)
    #plt.savefig(f'2D_pattern.jpg', format='jpg',  bbox_inches='tight')
    plt.show()
    

# Adjusted for demonstration; replace with your actual file path and patterns
file_path = open(r'DANE_Z_POMIAROW/KRIT2023_WiMOB2023/charakterystyka_2D/9_04_5_5GHz_1.5m_ch_ka.csv')
patterns = [1,2,23,26]
plot_multiple_patterns_from_csv(file_path, patterns)#"All elements turn on","Only first element turn on","Only last element turn on","Left side on",