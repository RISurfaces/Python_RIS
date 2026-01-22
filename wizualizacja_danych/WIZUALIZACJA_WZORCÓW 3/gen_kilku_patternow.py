import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display_images(paths, save_path=None):
    num_images = len(paths)
    rows = 2  # Liczba wierszy
    cols = 3  # Liczba kolumn

    fig, axs = plt.subplots(rows, cols, figsize=(15, 10))

    for i in range(rows):
        for j in range(cols):
            img_index = i * cols + j
            if img_index < num_images:
                img = mpimg.imread(paths[img_index])
                axs[i, j].imshow(img)
                axs[i, j].axis('off')
                axs[i, j].set_title(f"Pattern {img_index + 1}", fontsize=12)  # Dodanie podpisu
            else:
                axs[i, j].axis('off')  # Ukrycie pustych osi

    # Dodanie legendy na dole
    legend_labels = {"ON": "blue", "OFF": "lightblue"}
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black', linewidth=1) for color in legend_labels.values()]
    legend_texts = list(legend_labels.keys())

    fig.legend(
        legend_handles,
        legend_texts,
        loc='lower center',
        ncol=2,
        fontsize='large',
        title='Legend'
    )

    # Dostosowanie odstępów między obrazami
    plt.subplots_adjust(wspace=0.01, hspace=0.01, bottom=0.01)

    # Zapis figury, jeśli podano ścieżkę
    if save_path:
        plt.savefig(save_path, format='png', bbox_inches='tight')

    plt.show()

# Przykładowe ścieżki do zdjęć
image_paths = [
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\1_pattern.png",
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\2_pattern.png",
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\3_pattern.png",
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\4_pattern.png",
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\5_pattern.png",
    r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\6_pattern.png"
]

# Wyświetlanie zdjęć i zapis figury
save_path = r"C:\Users\Paweł\Desktop\RIS\Ris\Python_RIS\wizualizacja_danych\patterny_artykuł\combined_patterns.png"
display_images(image_paths, save_path=save_path)