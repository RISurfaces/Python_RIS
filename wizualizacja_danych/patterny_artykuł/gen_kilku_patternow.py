import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display_images(paths):
    num_images = len(paths)
    
    fig, axs = plt.subplots(3, 2, figsize=(10, 10))
    
    for i in range(3):
        for j in range(2):
            if (i * 2 + j) < num_images:
                img = mpimg.imread(paths[i * 2 + j])
                axs[i, j].imshow(img)
                axs[i, j].axis('off')
                axs[i, j].set_title(f"Pattern {i * 2 + j + 1}")  # Dodanie podpisu
                
    legend_labels = {"ON": "green", "OFF": "#C0F6C7"}
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black', linewidth=1) for color in legend_labels.values()]
    legend_texts = list(legend_labels.keys())
    
    fig.legend(legend_handles, legend_texts, loc='lower center', ncol=2, fontsize='large', title='Legend')  # Dodanie legendy
    
    plt.subplots_adjust(wspace=0.05, hspace=0.3)  # Zmniejszenie odstępów między obrazami
    plt.show()

# Przykładowe ścieżki do zdjęć
image_paths = [
    "1_pattern.png",
    "2_pattern.png",
    "15_pattern.png",
    "19_pattern.png",
    "21_pattern.png",
    "26_pattern.png"
]

# Wyświetlanie zdjęć
display_images(image_paths)

