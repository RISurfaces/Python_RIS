from PIL import Image

# Nazwy plików (upewnij się, że znajdują się w tym samym katalogu co skrypt)
image_files = {
    "1m_LAB": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_1m_METIS.jpg",
    "1m_CHAMBER": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_1m_AINFO.jpg",
    "1.5m_LAB": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_1.5m_METIS.jpg",
    "1.5m_CHAMBER": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_1.5m_AINFO.jpg",
    "2m_LAB": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_2m_METIS.jpg",
    "2m_CHAMBER": r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmap_pattern_3_dist_2m_AINFO.jpg",
}

# Wczytanie i dopasowanie rozmiaru obrazów
base_img = Image.open(image_files["1m_LAB"])
standard_size = base_img.size
resized_images = {
    key: Image.open(path).resize(standard_size) for key, path in image_files.items()
}

# Stworzenie nowego obrazu: 2 kolumny (LAB, CHAMBER), 3 wiersze (1m, 1.5m, 2m)
combined_width = standard_size[0] * 2
combined_height = standard_size[1] * 3
combined_image = Image.new("RGB", (combined_width, combined_height))

# Kolejność obrazów w siatce
order = [
    ("1m_LAB", "1m_CHAMBER"),
    ("1.5m_LAB", "1.5m_CHAMBER"),
    ("2m_LAB", "2m_CHAMBER"),
]

# Wklejanie do obrazu zbiorczego
for i, (lab_key, chamber_key) in enumerate(order):
    combined_image.paste(resized_images[lab_key], (0, i * standard_size[1]))
    combined_image.paste(resized_images[chamber_key], (standard_size[0], i * standard_size[1]))

# Zapisz wynik
output_filename = "combined_heatmaps_LAB_vs_CHAMBER.jpg"
combined_image.save(output_filename)
print(f"Zapisano obraz: {output_filename}")
