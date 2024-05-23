import pandas as pd
import matplotlib.pyplot as plt

def plot_multiple_patterns_from_csv(file_path, patterns):
    df = pd.read_csv(file_path, sep=';', names=['Degrees','Paterns', 'Frequency', 'Power'])


    # Ensure the DataFrame is sorted by 'Frequency' to connect points in ascending frequency order
    df = df.sort_values(by='Degrees')
    df = df[(df['Degrees'] >= 45) & (df['Degrees'] <= 135)]
    power_min = -90
    power_max = -45

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

    plt.xlabel('Kąt azymutu [°]', fontsize=18)
    plt.ylabel('Moc odebrana [dBm]', fontsize=18)
    plt.title('Moc odebrana w fukcji kąta azymutu RMA', fontsize=18)
    plt.xlim(45, 135)
    plt.ylim(power_min, power_max)
    plt.xticks([x *5 for x in range(9, 27)], rotation=45, fontsize=14)  
    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))], fontsize=14)  
    plt.legend(["1", "2","3","4","5","6"], loc="upper right", prop={'size': 15}, borderaxespad=2, title='Wzorzec')
    plt.grid(True)
    plt.savefig(f'2D_pattern.jpg', format='jpg')
    plt.show()
    

# Adjusted for demonstration; replace with your actual file path and patterns
file_path = open(r'C:\Users\Marcel\Python_RIS\Python_RIS\wyniki\charakterystyka_2D\9_04_5_5GHz_1.5m_ch_ka.csv')
patterns = [1,2, 17, 19, 21, 26]#,"Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
plot_multiple_patterns_from_csv(file_path, patterns)#"All elements turn on","Only first element turn on","Only last element turn on","Left side on",