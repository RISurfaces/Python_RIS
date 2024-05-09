import pandas as pd
import matplotlib.pyplot as plt

def plot_multiple_patterns_from_csv(file_path, patterns):
    df = pd.read_csv(file_path, sep=';', names=['Degrees','Paterns', 'Frequency', 'Power'])


    # Ensure the DataFrame is sorted by 'Frequency' to connect points in ascending frequency order
    df = df.sort_values(by='Degrees')
    df = df[(df['Degrees'] >= 0) & (df['Degrees'] <= 180)]
    power_min = -85
    power_max = -50

    plt.figure(figsize=(12, 8))
    
    colors=['blue','red']
    
    for index, pattern in enumerate(patterns):
        specific_pattern_df = df[df['Paterns'] == pattern]
        print(pattern)
        if specific_pattern_df.empty:
            print(f"No entries found for pattern '{pattern}'.")
            continue

        color = colors[index % len(colors)]
        plt.plot(specific_pattern_df['Degrees']-90, specific_pattern_df['Power'], marker='o', linestyle='-', label=pattern, color=color)

    plt.xlabel('Degree [*]')
    plt.ylabel('Power [dBm]')
    plt.title('Degrees vs. Power for Multiple Configurations')
    plt.xlim(-95, 95)
    plt.ylim(power_min, power_max)
    plt.xticks([x *5 for x in range(-19, 19)], rotation=45)  
    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))])  
    plt.legend(loc='upper right', prop={'size': 10}, borderaxespad=2, title='Pattern')
    plt.grid(True)
    plt.show()

# Adjusted for demonstration; replace with your actual file path and patterns
file_path = open(r'C:\Users\Brzaki\Documents\Python_RIS\Python_RIS\wyniki\charakterystyka_2D\12_04\12_04_5_2GHz_1_5m_ch_ka.csv')
patterns = [12,26]#,"Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
plot_multiple_patterns_from_csv(file_path, patterns)#"All elements turn on","Only first element turn on","Only last element turn on","Left side on",